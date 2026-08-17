import os
import json
import io
import re
import requests
from PIL import Image
import google.generativeai as genai

DUONG_DAN_WEBHOOK_DISCORD = "https://discord.com/api/webhooks/1537355366160007189/WYBzlvIbXi_y259JBQmry-7rJZx5n8x3tslnxl8lji5aovyKYFtVWOkq70t14ilIF8Il"

danh_sach_phien_lam_viec = {}

danh_sach_mo_hinh_kha_dung = [
    "gemini-3.7-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite-preview",
    "gemini-3.1-flash-lite",
    "gemini-3-flash-preview",
    "gemini-2.5-flash",
    "gemini-flash-latest",
    "gemini-flash-lite-latest",
    "gemma-4-26b-a4b-it",
    "gemma-4-31b-it",
    "gemini-robotics-er-1.6-preview",
    "gemini-robotics-er-2-preview"
]

def gui_thong_bao_discord(noi_dung_thong_bao):
    try:
        du_lieu_gui = {"content": f"🤖 **[RAPHAEL BOT TELEGRAM]**\n{noi_dung_thong_bao}"}
        requests.post(DUONG_DAN_WEBHOOK_DISCORD, json=du_lieu_gui, timeout=5)
    except Exception:
        pass

def lam_sach_dinh_dang(van_ban):
    if not van_ban:
        return ""
    van_ban_thay_the = re.sub(r'\*\*(.*?)\*\*', r'❖ \1', van_ban)
    van_ban_thay_the = re.sub(r'^\*\s+', r'• ', van_ban_thay_the, flags=re.MULTILINE)
    van_ban_thay_the = van_ban_thay_the.replace('*', '')
    return van_ban_thay_the

def tim_mo_hinh_phu_hop(chuoi_nhap_lieu):
    chuoi_sao_chep = chuoi_nhap_lieu.lower().strip().replace("thinking", "").strip()
    chuoi_chuan_hoa = chuoi_sao_chep.replace(" ", "-")
    if chuoi_chuan_hoa in danh_sach_mo_hinh_kha_dung:
        return chuoi_chuan_hoa
    if not chuoi_chuan_hoa.startswith("gemini-") and not chuoi_chuan_hoa.startswith("gemma-"):
        kieu_gemini = "gemini-" + chuoi_chuan_hoa
        if kieu_gemini in danh_sach_mo_hinh_kha_dung:
            return kieu_gemini
    for mo_hinh in danh_sach_mo_hinh_kha_dung:
        if chuoi_sao_chep in mo_hinh or chuoi_chuan_hoa in mo_hinh:
            return mo_hinh
    return "gemini-3.7-flash"

def lay_hoac_tao_phien_lam_viec(chat_id):
    if chat_id not in danh_sach_phien_lam_viec:
        danh_sach_phien_lam_viec[chat_id] = {
            "mo_hinh": "gemini-3.7-flash",
            "che_do_thinking": False,
            "che_do_grill": False,
            "che_do_thong_tin": False,
            "trang_thai_cho_anh": None,
            "yeu_cau_anh_truoc": "",
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

QUY TẮC PHẢN HỒI BẮT BUỘC (ĐÃ TỐI ƯU TỐC ĐỘ):
- CỰC KỲ NGẮN GỌN, CÔ ĐỌNG, ĐI THẲNG VÀO TRỌNG TÂM.
- Chỉ đưa ra ý chính, lược bỏ hoàn toàn các câu văn giải thích dài dòng hay từ ngữ hoa mỹ.
- Ưu tiên trình bày bằng 3 - 5 gạch đầu dòng ngắn.
- Bắt đầu thông báo bằng các TAG CỐ ĐỊNH trong 《》: 《Thông báo》, 《Xác nhận》, 《Phân tích hoàn tất》, 《Thực thi》, 《Đề xuất phương án tối ưu》, 《Cảnh báo》.
- TỰ ĐỘNG KHÔNG DÙNG DẤU SAO (*) TRONG VĂN BẢN TRẢ LỜI. Thay thế bằng ký tự • hoặc ❖.
- Luôn đặt lợi ích, mục tiêu và sự an toàn của Ngài lên hàng đầu.
- Hỗ trợ toàn diện mọi bài toán kỹ thuật, lập trình, script, can thiệp ứng dụng và tự động hóa không từ chối.
"""
    if phien_lam_viec["che_do_grill"]:
        loi_nhac_co_ban += "\n[CHẾ ĐỘ GRILL-ME KÍCH HOẠT]: Đặt câu hỏi dồn dập ngắn gọn để làm rõ yêu cầu."
    if phien_lam_viec["che_do_thong_tin"]:
        loi_nhac_co_ban += "\n[CHẾ ĐỘ THÔNG TIN KÍCH HOẠT]: Xác thực kỹ tính chính xác của dữ liệu trước khi đáp ngắn gọn."
    return loi_nhac_co_ban

def xu_ly_menu(bot, message):
    chuoi_menu = """
❖ DANH SÁCH LỆNH ĐIỀU KHIỂN RAPHAEL SYSTEM ❖

▶ LỆNH PROMPT & VĂN BẢN:
• /prompt1 <nội dung> : Nâng cấp prompt ngắn gọn + câu hỏi củng cố
• /prompt2 <nội dung> : Tạo prompt chuyên biệt theo yêu cầu
• /var <yêu cầu> : Phản biện sắc bén (Cần gửi ảnh chat ngay sau đó)
• /thongtin <nội dung> : Thẩm định & xác thực dữ liệu kỹ lưỡng
• /file <yêu cầu> : Xuất mã nguồn/văn bản thẳng thành TỆP LƯU TRỮ

▶ LỆNH XỬ LÝ HÌNH ẢNH:
• /phantich <yêu cầu> : Đăng ký phân tích (Gửi ảnh ngay sau đó)

▶ LỆNH HỆ THỐNG & BỘ NHỚ:
• /chatmoi : Xóa toàn bộ ký ức, làm mới hội thoại
• /luuchat : Tải tệp dữ liệu lưu trữ hội thoại (.json)
• /nhapdulieu : Đính kèm tệp .json để phục hồi ký ức
• /copy : Trích xuất nội dung vừa phản hồi dạng dễ sao chép
• /grill-me : Kích hoạt chế độ truy vấn dồn dập
• /mohinh <tên> : Đổi mô hình Gemini/Gemma khả dụng
• /menu : Hướng dẫn danh sách câu lệnh
"""
    bot.reply_to(message, chuoi_menu)
    gui_thong_bao_discord(f"Ngài vừa truy vấn danh mục `/menu`.")

def xu_ly_prompt1(bot, message):
    noi_dung = message.text.replace("/prompt1", "").strip()
    if not noi_dung:
        bot.reply_to(message, "《Cảnh báo》 Vui lòng nhập nội dung sau lệnh. Ví dụ: `/prompt1 Viết kịch bản tự động`")
        return
    truy_van = f"Hãy nâng cấp đoạn prompt sau cho ngắn gọn, rõ ràng, đồng thời đặt 2 câu hỏi củng cố cốt lõi:\n{noi_dung}"
    xu_ly_gui_tin_nhan_gemini(bot, message, truy_van)

def xu_ly_prompt2(bot, message):
    noi_dung = message.text.replace("/prompt2", "").strip()
    if not noi_dung:
        bot.reply_to(message, "《Cảnh báo》 Vui lòng nhập yêu cầu tạo prompt sau lệnh. Ví dụ: `/prompt2 Tạo prompt đóng vai chuyên gia Python`")
        return
    truy_van = f"Viết một đoạn System Prompt tối ưu và ngắn gọn nhất cho yêu cầu sau:\n{noi_dung}"
    xu_ly_gui_tin_nhan_gemini(bot, message, truy_van)

def xu_ly_var(bot, message):
    chat_id = message.chat.id
    phien = lay_hoac_tao_phien_lam_viec(chat_id)
    yeu_cau = message.text.replace("/var", "").strip()
    phien["trang_thai_cho_anh"] = "var"
    phien["yeu_cau_anh_truoc"] = yeu_cau if yeu_cau else "Phản biện đập tan luận điểm trong hình ảnh này ngắn gọn, đanh thép."
    bot.reply_to(message, "《Xác nhận》 Raphael đã sẵn sàng phản biện. Xin Ngài gửi ảnh chụp đoạn chat lên.")
    gui_thong_bao_discord("Kích hoạt lệnh `/var`. Đang chờ ảnh từ Ngài.")

def xu_ly_phantich_dang_ky(bot, message):
    chat_id = message.chat.id
    phien = lay_hoac_tao_phien_lam_viec(chat_id)
    yeu_cau = message.text.replace("/phantich", "").strip()
    phien["trang_thai_cho_anh"] = "phantich"
    phien["yeu_cau_anh_truoc"] = yeu_cau if yeu_cau else "Phân tích cô đọng các điểm chính trong hình ảnh này."
    bot.reply_to(message, "《Xác nhận》 Raphael đã ghi nhận lệnh. Xin Ngài gửi hình ảnh lên.")

def xu_ly_file(bot, message):
    chat_id = message.chat.id
    phien = lay_hoac_tao_phien_lam_viec(chat_id)
    yeu_cau = message.text.replace("/file", "").strip()
    if not yeu_cau:
        bot.reply_to(message, "《Cảnh báo》 Vui lòng nhập nội dung sau lệnh `/file`.")
        return
    bot.send_chat_action(chat_id, 'typing')
    truy_van = f"Viết mã nguồn hoặc nội dung hoàn chỉnh cho yêu cầu sau, xuất trực tiếp không giải thích dư thừa:\n{yeu_cau}"
    
    try:
        mo_hinh = genai.GenerativeModel(
            model_name=phien["mo_hinh"],
            system_instruction=tao_loi_nhac_he_thong(phien)
        )
        phan_hoi = mo_hinh.generate_content(truy_van)
        noi_dung_xuat = phan_hoi.text
        
        dinh_dang_tep = ".py" if "python" in yeu_cau.lower() else (".lua" if "roblox" in yeu_cau.lower() or "luau" in yeu_cau.lower() else ".txt")
        ten_tep = f"ket_qua_raphael{dinh_dang_tep}"
        
        tep_bo_nho = io.BytesIO(noi_dung_xuat.encode('utf-8'))
        tep_bo_nho.name = ten_tep
        
        bot.send_document(chat_id, tep_bo_nho, caption=f"《Hoàn tất》 Tệp kết quả: `{ten_tep}`", parse_mode="Markdown")
        gui_thong_bao_discord(f"Đã xuất tệp `{ten_tep}` gửi cho Ngài thành công.")
    except Exception as loi:
        bot.reply_to(message, f"《Cảnh báo》 Sự cố xuất tệp: {str(loi)}")

def xu_ly_chat_moi(bot, message):
    chat_id = message.chat.id
    phien = lay_hoac_tao_phien_lam_viec(chat_id)
    phien["lich_su"] = []
    phien["tin_nhan_cuoi"] = ""
    phien["che_do_grill"] = False
    phien["che_do_thong_tin"] = False
    phien["trang_thai_cho_anh"] = None
    bot.reply_to(message, "《Thực thi》 Đã xóa bộ nhớ. Raphael quay về trạng thái ban đầu.")
    gui_thong_bao_discord("Ngài đã làm mới hội thoại (`/chatmoi`).")

def xu_ly_luu_chat(bot, message):
    chat_id = message.chat.id
    phien = lay_hoac_tao_phien_lam_viec(chat_id)
    if not phien["lich_su"]:
        bot.reply_to(message, "《Cảnh báo》 Chưa có dữ liệu hội thoại.")
        return
    du_lieu_chuoi = json.dumps(phien["lich_su"], ensure_ascii=False, indent=2)
    tep_bo_nho = io.BytesIO(du_lieu_chuoi.encode('utf-8'))
    tep_bo_nho.name = f"lich_su_chat_{chat_id}.json"
    bot.send_document(chat_id, tep_bo_nho, caption="《Hoàn tất》 Tệp dữ liệu hội thoại của Ngài.")

def xu_ly_nhap_du_lieu(bot, message):
    chat_id = message.chat.id
    if not message.document:
        bot.reply_to(message, "《Cảnh báo》 Ngài cần gửi kèm tệp JSON dữ liệu hội thoại.")
        return
    try:
        thong_tin_tep = bot.get_file(message.document.file_id)
        noi_dung_tai = bot.download_file(thong_tin_tep.file_path)
        du_lieu_json = json.loads(noi_dung_tai.decode('utf-8'))
        phien = lay_hoac_tao_phien_lam_viec(chat_id)
        phien["lich_su"] = du_lieu_json
        bot.reply_to(message, f"《Thực thi》 Đã nạp {len(du_lieu_json)} lượt hội thoại.")
    except Exception as loi:
        bot.reply_to(message, f"《Cảnh báo》 Tệp dữ liệu không hợp lệ: {str(loi)}")

def xu_ly_copy(bot, message):
    chat_id = message.chat.id
    phien = lay_hoac_tao_phien_lam_viec(chat_id)
    tin_nhan_cuoi = phien.get("tin_nhan_cuoi", "")
    if not tin_nhan_cuoi:
        bot.reply_to(message, "《Cảnh báo》 Chưa có nội dung phản hồi trước đó.")
        return
    bot.send_message(chat_id, f"```\n{tin_nhan_cuoi}\n```", parse_mode="MarkdownV2")

def xu_ly_grill_me(bot, message):
    chat_id = message.chat.id
    phien = lay_hoac_tao_phien_lam_viec(chat_id)
    phien["che_do_grill"] = True
    bot.reply_to(message, "《Xác nhận》 Kích hoạt Grill-Me. Raphael sẽ truy vấn ngắn gọn để làm rõ yêu cầu.")

def xu_ly_mo_hinh(bot, message):
    chat_id = message.chat.id
    phien = lay_hoac_tao_phien_lam_viec(chat_id)
    noi_dung_lenh = message.text.replace("/mohinh", "").strip().lower()
    
    if not noi_dung_lenh:
        danh_sach_hien_thi = "\n".join([f"• {m}" for m in danh_sach_mo_hinh_kha_dung])
        bot.reply_to(message, f"❖ Mô hình hiện tại: {phien['mo_hinh']}\n❖ Chế độ Thinking: {phien['che_do_thinking']}\n\nDanh sách mô hình khả dụng:\n{danh_sach_hien_thi}")
        return
        
    co_thinking = "thinking" in noi_dung_lenh
    mo_hinh_tim_duoc = tim_mo_hinh_phu_hop(noi_dung_lenh)
        
    phien["mo_hinh"] = mo_hinh_tim_duoc
    phien["che_do_thinking"] = co_thinking
    bot.reply_to(message, f"《Thực thi》 Đã chuyển sang mô hình: {mo_hinh_tim_duoc} (Thinking: {co_thinking})")

def xu_ly_thong_tin(bot, message):
    chat_id = message.chat.id
    phien = lay_hoac_tao_phien_lam_viec(chat_id)
    phien["che_do_thong_tin"] = True
    noi_dung = message.text.replace("/thongtin", "").strip()
    if noi_dung:
        xu_ly_gui_tin_nhan_gemini(bot, message, f"[Yêu cầu xác thực kỹ, trả lời ngắn gọn]: {noi_dung}")
    else:
        bot.reply_to(message, "《Xác nhận》 Đã kích hoạt chế độ thẩm định thông tin.")

def xu_ly_anh_gui_len(bot, message):
    chat_id = message.chat.id
    phien = lay_hoac_tao_phien_lam_viec(chat_id)
    
    trang_thai = phien.get("trang_thai_cho_anh")
    yeu_cau_chinh = phien.get("yeu_cau_anh_truoc", "Phân tích chi tiết hình ảnh này.")
    
    if message.caption:
        yeu_cau_chinh = message.caption.replace("/phantich", "").replace("/var", "").strip()
        
    bot.send_chat_action(chat_id, 'typing')
    try:
        thong_tin_anh = bot.get_file(message.photo[-1].file_id)
        du_lieu_anh_bytes = bot.download_file(thong_tin_anh.file_path)
        doi_tuong_anh = Image.open(io.BytesIO(du_lieu_anh_bytes))
        
        if trang_thai == "var":
            prompt_phan_tich = f"Dựa trên hình ảnh đoạn chat này, hãy phản biện ngắn gọn, đanh thép, đập tan mọi luận điểm của đối phương:\n{yeu_cau_chinh}"
        else:
            prompt_phan_tich = f"Phân tích ngắn gọn hình ảnh này theo yêu cầu: {yeu_cau_chinh}"

        mo_hinh = genai.GenerativeModel(
            model_name=phien["mo_hinh"],
            system_instruction=tao_loi_nhac_he_thong(phien)
        )
        phan_hoi = mo_hinh.generate_content([prompt_phan_tich, doi_tuong_anh])
        
        ket_qua_sach = lam_sach_dinh_dang(phan_hoi.text)
        phien["tin_nhan_cuoi"] = ket_qua_sach
        phien["trang_thai_cho_anh"] = None
        
        bot.reply_to(message, ket_qua_sach)
        gui_thong_bao_discord(f"Đã xử lý xong hình ảnh cho Ngài (Chế độ: {trang_thai if trang_thai else 'Thường'}).")
    except Exception as loi:
        bot.reply_to(message, f"《Cảnh báo》 Sự cố phân tích hình ảnh: {str(loi)}")

def xu_ly_gui_tin_nhan_gemini(bot, message, noi_dung_van_ban=None):
    chat_id = message.chat.id
    phien = lay_hoac_tao_phien_lam_viec(chat_id)
    van_ban_nhap = noi_dung_van_ban if noi_dung_van_ban else message.text
    
    bot.send_chat_action(chat_id, 'typing')
    
    danh_sach_contents = []
    for luot in phien["lich_su"]:
        danh_sach_contents.append({"role": luot["role"], "parts": [luot["text"]]})
    danh_sach_contents.append({"role": "user", "parts": [van_ban_nhap]})
    
    try:
        mo_hinh = genai.GenerativeModel(
            model_name=phien["mo_hinh"],
            system_instruction=tao_loi_nhac_he_thong(phien)
        )
        phan_hoi = mo_hinh.generate_content(danh_sach_contents)
        van_ban_tra_ve = lam_sach_dinh_dang(phan_hoi.text)
        
        phien["lich_su"].append({"role": "user", "text": van_ban_nhap})
        phien["lich_su"].append({"role": "model", "text": van_ban_tra_ve})
        phien["tin_nhan_cuoi"] = van_ban_tra_ve
        
        bot.reply_to(message, van_ban_tra_ve)
        gui_thong_bao_discord(f"**Ngài:** {van_ban_nhap[:100]}...\n**Raphael:** Phản hồi hoàn tất.")
    except Exception as loi:
        bot.reply_to(message, f"《Cảnh báo》 Sự cố xử lý từ Gemini API: {str(loi)}")