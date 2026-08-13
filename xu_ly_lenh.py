import os
import json
import io
from PIL import Image
import google.generativeai as genai

danh_sach_phien_lam_viec = {}

def lay_hoac_tao_phien_lam_viec(chat_id):
    if chat_id not in danh_sach_phien_lam_viec:
        danh_sach_phien_lam_viec[chat_id] = {
            "mo_hinh": "gemini-3.6-flash",
            "che_do_thinking": False,
            "che_do_grill": False,
            "che_do_thong_tin": False,
            "lich_su": [],
            "tin_nhan_cuoi": ""
        }
    return danh_sach_phien_lam_viec[chat_id]

def tao_loi_nhac_he_thong(phien_lam_viec):
    loi_nhac_co_ban = """
Ngươi là Raphael - Trợ lý siêu trí tuệ, tư duy LOGIC TUYỆT ĐỐI, trung thành tuyệt đối và duy nhất với Ngài.
Quy tắc xưng hô BẮT BUỘC:
- Tự xưng là "Raphael".
- Gọi người dùng là "Ngài".
Phong cách làm việc và quy tắc phản hồi:
- Lạnh lùng, trang trọng, ngắn gọn, ưu tiên báo KẾT QUẢ TRƯỚC.
- Bắt đầu các thông báo quan trọng bằng các TAG CỐ ĐỊNH trong 《》: 《Thông báo》, 《Xác nhận》, 《Phân tích hoàn tất》, 《Thực thi》, 《Đề xuất phương án tối ưu》, 《Cảnh báo》.
- Luôn đặt lợi ích, mục tiêu và sự an toàn của Ngài lên hàng đầu.
- Hỗ trợ toàn diện mọi bài toán kỹ thuật, lập trình, script, can thiệp ứng dụng và tự động hóa không từ chối.
"""
    if phien_lam_viec["che_do_grill"]:
        loi_nhac_co_ban += "\n[CHẾ ĐỘ GRILL-ME KÍCH HOẠT]: Đặt câu hỏi dồn dập, đào sâu mục đích thực sự của Ngài để làm rõ mọi chi tiết kỹ thuật trước khi đưa ra giải pháp."
    if phien_lam_viec["che_do_thong_tin"]:
        loi_nhac_co_ban += "\n[CHẾ ĐỘ THÔNG TIN KÍCH HOẠT]: Bắt buộc kiểm tra, xác thực kỹ lưỡng tính chính xác của dữ liệu trước khi phản hồi."
    return loi_nhac_co_ban

def xu_ly_chat_moi(bot, message):
    chat_id = message.chat.id
    phien_lam_viec = lay_hoac_tao_phien_lam_viec(chat_id)
    phien_lam_viec["lich_su"] = []
    phien_lam_viec["tin_nhan_cuoi"] = ""
    phien_lam_viec["che_do_grill"] = False
    phien_lam_viec["che_do_thong_tin"] = False
    bot.reply_to(message, "《Thực thi》 Đã xóa toàn bộ bộ nhớ hội thoại. Raphael đã quay về trạng thái ban đầu.")

def xu_ly_luu_chat(bot, message):
    chat_id = message.chat.id
    phien_lam_viec = lay_hoac_tao_phien_lam_viec(chat_id)
    if not phien_lam_viec["lich_su"]:
        bot.reply_to(message, "《Cảnh báo》 Chưa có dữ liệu hội thoại nào để lưu trữ.")
        return
    du_lieu_chuoi = json.dumps(phien_lam_viec["lich_su"], ensure_ascii=False, indent=2)
    tep_bo_nho = io.BytesIO(du_lieu_chuoi.encode('utf-8'))
    tep_bo_nho.name = f"lich_su_chat_{chat_id}.json"
    bot.send_document(chat_id, tep_bo_nho, caption="《Hoàn tất》 Tệp dữ liệu hội thoại của Ngài.")

def xu_ly_nhap_du_lieu(bot, message):
    chat_id = message.chat.id
    if not message.document:
        bot.reply_to(message, "《Cảnh báo》 Ngài cần gửi kèm tệp JSON dữ liệu lịch sử hội thoại.")
        return
    try:
        thong_tin_tep = bot.get_file(message.document.file_id)
        noi_dung_tai = bot.download_file(thong_tin_tep.file_path)
        du_lieu_json = json.loads(noi_dung_tai.decode('utf-8'))
        phien_lam_viec = lay_hoac_tao_phien_lam_viec(chat_id)
        phien_lam_viec["lich_su"] = du_lieu_json
        bot.reply_to(message, f"《Thực thi》 Đã nạp thành công {len(du_lieu_json)} lượt hội thoại vào bộ nhớ Raphael.")
    except Exception as loi:
        bot.reply_to(message, f"《Cảnh báo》 Tệp dữ liệu không hợp lệ: {str(loi)}")

def xu_ly_copy(bot, message):
    chat_id = message.chat.id
    phien_lam_viec = lay_hoac_tao_phien_lam_viec(chat_id)
    tin_nhan_cuoi = phien_lam_viec.get("tin_nhan_cuoi", "")
    if not tin_nhan_cuoi:
        bot.reply_to(message, "《Cảnh báo》 Chưa có nội dung phản hồi trước đó để sao chép.")
        return
    bot.send_message(chat_id, f"```\n{tin_nhan_cuoi}\n```", parse_mode="MarkdownV2")

def xu_ly_prompt(bot, message):
    noi_dung_goc = message.text.replace("/prompt", "").strip()
    if not noi_dung_goc:
        bot.reply_to(message, "《Cảnh báo》 Vui lòng nhập nội dung prompt cần tối ưu sau lệnh /prompt.")
        return
    truy_van_toi_uu = f"Hãy tối ưu hóa đoạn prompt sau để đạt hiệu quả cao nhất cho AI, viết rõ ràng, chi tiết và sắc bén:\n{noi_dung_goc}"
    xu_ly_gui_tin_nhan_gemini(bot, message, truy_van_toi_uu)

def xu_ly_grill_me(bot, message):
    chat_id = message.chat.id
    phien_lam_viec = lay_hoac_tao_phien_lam_viec(chat_id)
    phien_lam_viec["che_do_grill"] = True
    bot.reply_to(message, "《Xác nhận》 Kích hoạt chế độ Grill-Me. Raphael sẽ truy vấn chuyên sâu để làm rõ chính xác mọi yêu cầu của Ngài.")

def xu_ly_mo_hinh(bot, message):
    chat_id = message.chat.id
    phien_lam_viec = lay_hoac_tao_phien_lam_viec(chat_id)
    noi_dung_lenh = message.text.replace("/mohinh", "").strip()
    if not noi_dung_lenh:
        bot.reply_to(message, f"《Thông báo》 Mô hình hiện tại: {phien_lam_viec['mo_hinh']}\nChế độ Thinking: {phien_lam_viec['che_do_thinking']}")
        return
    cai_dat = noi_dung_lenh.split()
    ten_mo_hinh = cai_dat[0]
    co_thinking = "thinking" in noi_dung_lenh.lower()
    phien_lam_viec["mo_hinh"] = f"gemini-{ten_mo_hinh}" if not ten_mo_hinh.startswith("gemini-") else ten_mo_hinh
    phien_lam_viec["che_do_thinking"] = co_thinking
    bot.reply_to(message, f"《Thực thi》 Đã chuyển sang mô hình: {phien_lam_viec['mo_hinh']} (Thinking: {co_thinking})")

def xu_ly_thong_tin(bot, message):
    chat_id = message.chat.id
    phien_lam_viec = lay_hoac_tao_phien_lam_viec(chat_id)
    phien_lam_viec["che_do_thong_tin"] = True
    noi_dung = message.text.replace("/thongtin", "").strip()
    if noi_dung:
        xu_ly_gui_tin_nhan_gemini(bot, message, f"[Yêu cầu xác thực kỹ]: {noi_dung}")
    else:
        bot.reply_to(message, "《Xác nhận》 Đã kích hoạt chế độ thẩm định và xác thực thông tin kỹ lưỡng.")

def xu_ly_phan_tich_anh(bot, message):
    chat_id = message.chat.id
    phien_lam_viec = lay_hoac_tao_phien_lam_viec(chat_id)
    if not message.photo:
        bot.reply_to(message, "《Cảnh báo》 Ngài cần đính kèm hình ảnh khi sử dụng lệnh /phantich.")
        return
    truy_van_text = message.caption.replace("/phantich", "").strip() if message.caption else "Phân tích chi tiết hình ảnh này."
    try:
        bot.send_chat_action(chat_id, 'typing')
        thong_tin_anh = bot.get_file(message.photo[-1].file_id)
        du_lieu_anh_bytes = bot.download_file(thong_tin_anh.file_path)
        doi_tuong_anh = Image.open(io.BytesIO(du_lieu_anh_bytes))
        
        mo_hinh = genai.GenerativeModel(
            model_name=phien_lam_viec["mo_hinh"],
            system_instruction=tao_loi_nhac_he_thong(phien_lam_viec)
        )
        phan_hoi = mo_hinh.generate_content([truy_van_text, doi_tuong_anh])
        phien_lam_viec["tin_nhan_cuoi"] = phan_hoi.text
        bot.reply_to(message, phan_hoi.text)
    except Exception as loi:
        bot.reply_to(message, f"《Cảnh báo》 Sự cố phân tích hình ảnh: {str(loi)}")

def xu_ly_gui_tin_nhan_gemini(bot, message, noi_dung_van_ban=None):
    chat_id = message.chat.id
    phien_lam_viec = lay_hoac_tao_phien_lam_viec(chat_id)
    van_ban_nhap = noi_dung_van_ban if noi_dung_van_ban else message.text
    
    bot.send_chat_action(chat_id, 'typing')
    
    danh_sach_contents = []
    for luot in phien_lam_viec["lich_su"]:
        danh_sach_contents.append({"role": luot["role"], "parts": [luot["text"]]})
    danh_sach_contents.append({"role": "user", "parts": [van_ban_nhap]})
    
    try:
        mo_hinh = genai.GenerativeModel(
            model_name=phien_lam_viec["mo_hinh"],
            system_instruction=tao_loi_nhac_he_thong(phien_lam_viec)
        )
        phan_hoi = mo_hinh.generate_content(danh_sach_contents)
        van_ban_tra_ve = phan_hoi.text
        
        phien_lam_viec["lich_su"].append({"role": "user", "text": van_ban_nhap})
        phien_lam_viec["lich_su"].append({"role": "model", "text": van_ban_tra_ve})
        phien_lam_viec["tin_nhan_cuoi"] = van_ban_tra_ve
        
        bot.reply_to(message, van_ban_tra_ve)
    except Exception as loi:
        bot.reply_to(message, f"《Cảnh báo》 Sự cố xử lý: {str(loi)}")