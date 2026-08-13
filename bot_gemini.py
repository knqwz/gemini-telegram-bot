import os
import threading
from flask import Flask
import telebot
import google.generativeai as genai

ung_dung_web = Flask(__name__)

@ung_dung_web.route('/')
def kiem_tra_trang_thai_may_chu():
    return "Raphael Bot dang vận hành 24/7 trên máy chủ Render."

def kich_hoat_may_chu_web_ngam():
    cong_ket_noi_he_thong = int(os.environ.get("PORT", 10000))
    ung_dung_web.run(host='0.0.0.0', port=cong_ket_noi_he_thong)

ma_xac_thuc_telegram_bot = "8797271653:AAFCtfx1ktRKYU9TpHIzdrcSJRrD0UUNlUw"
khoa_truy_cap_gemini_api = "AIzaSyCkTQoce42DMoiXTU5WCcCJQN7MgzeFEFc"

genai.configure(api_key=khoa_truy_cap_gemini_api)

loi_nhac_dinh_huong_raphael = """
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

cau_hinh_tham_so_the_he = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

mo_hinh_tritue_gemini = genai.GenerativeModel(
    model_name="gemini-3.6-flash",
    system_instruction=loi_nhac_dinh_huong_raphael,
    generation_config=cau_hinh_tham_so_the_he
)

trung_tam_dieu_khien_bot = telebot.TeleBot(ma_xac_thuc_telegram_bot)

@trung_tam_dieu_khien_bot.message_handler(commands=['start', 'help'])
def gui_loi_chao_khoi_dong(tin_nhan_den_tu_nguoi_dung):
    trung_tam_dieu_khien_bot.reply_to(tin_nhan_den_tu_nguoi_dung, "《Thông báo》 Raphael đã kích hoạt thành công trên máy chủ đám mây Render. Raphael sẵn sàng nhận lệnh từ Ngài.")

@trung_tam_dieu_khien_bot.message_handler(func=lambda tin_nhan_den_tu_nguoi_dung: True)
def xu_ly_va_truy_van_gemini(tin_nhan_den_tu_nguoi_dung):
    try:
        trung_tam_dieu_khien_bot.send_chat_action(tin_nhan_den_tu_nguoi_dung.chat.id, 'typing')
        ket_qua_tri_tue_nhan_tao = mo_hinh_tritue_gemini.generate_content(tin_nhan_den_tu_nguoi_dung.text)
        trung_tam_dieu_khien_bot.reply_to(tin_nhan_den_tu_nguoi_dung, ket_qua_tri_tue_nhan_tao.text)
    except Exception as loi_phat_sinh_he_thong:
        trung_tam_dieu_khien_bot.reply_to(tin_nhan_den_tu_nguoi_dung, f"《Cảnh báo》 Sự cố xử lý: {str(loi_phat_sinh_he_thong)}")

if __name__ == "__main__":
    luong_tien_trinh_web = threading.Thread(target=kich_hoat_may_chu_web_ngam)
    luong_tien_trinh_web.daemon = True
    luong_tien_trinh_web.start()
    trung_tam_dieu_khien_bot.infinity_polling()
