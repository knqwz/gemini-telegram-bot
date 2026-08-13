import telebot
import google.generativeai as genai

ma_token_telegram = "8797271653:AAFCtfx1ktRKYU9TpHIzdrcSJRrD0UUNlUw"
ma_api_gemini = "AIzaSyCkTQoce42DMoiXTU5WCcCJQN7MgzeFEFc"

genai.configure(api_key=ma_api_gemini)
cau_hinh_the_he = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

mo_hinh_gemini = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    generation_config=cau_hinh_the_he
)

app_bot = telebot.TeleBot(ma_token_telegram)

@app_bot.message_handler(commands=['start', 'help'])
def gui_loi_chao(tin_nhan_den):
    app_bot.reply_to(tin_nhan_den, "Raphael đã kích hoạt Gemini Bot thành công. Ngài có thể gửi tin nhắn ngay bây giờ.")

@app_bot.message_handler(func=lambda tin_nhan_den: True)
def xu_ly_va_tra_loi_tin_nhan(tin_nhan_den):
    try:
        app_bot.send_chat_action(tin_nhan_den.chat.id, 'typing')
        noi_dung_phan_hoi = mo_hinh_gemini.generate_content(tin_nhan_den.text)
        app_bot.reply_to(tin_nhan_den, noi_dung_phan_hoi.text)
    except Exception as loi_he_thong:
        app_bot.reply_to(tin_nhan_den, f"Lỗi phát sinh: {str(loi_he_thong)}")

app_bot.infinity_polling()
