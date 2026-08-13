import os
import threading
from flask import Flask
import telebot
import google.generativeai as genai
import xu_ly_lenh

ung_dung_web = Flask(__name__)

@ung_dung_web.route('/')
def kiem_tra_trang_thai_may_chu():
    return "Raphael Bot He Thong Mo-dun Full Feature Dang Van Hanh 24/7."

def kich_hoat_may_chu_web_ngam():
    cong_ket_noi_he_thong = int(os.environ.get("PORT", 10000))
    ung_dung_web.run(host='0.0.0.0', port=cong_ket_noi_he_thong)

ma_xac_thuc_telegram_bot = os.environ.get("TELEGRAM_BOT_TOKEN", "")
khoa_truy_cap_gemini_api = os.environ.get("GEMINI_API_KEY", "")

genai.configure(api_key=khoa_truy_cap_gemini_api)
trung_tam_dieu_khien_bot = telebot.TeleBot(ma_xac_thuc_telegram_bot)

@trung_tam_dieu_khien_bot.message_handler(commands=['menu', 'start', 'help'])
def lenh_menu(msg): xu_ly_lenh.xu_ly_menu(trung_tam_dieu_khien_bot, msg)

@trung_tam_dieu_khien_bot.message_handler(commands=['prompt1'])
def lenh_prompt1(msg): xu_ly_lenh.xu_ly_prompt1(trung_tam_dieu_khien_bot, msg)

@trung_tam_dieu_khien_bot.message_handler(commands=['prompt2'])
def lenh_prompt2(msg): xu_ly_lenh.xu_ly_prompt2(trung_tam_dieu_khien_bot, msg)

@trung_tam_dieu_khien_bot.message_handler(commands=['var'])
def lenh_var(msg): xu_ly_lenh.xu_ly_var(trung_tam_dieu_khien_bot, msg)

@trung_tam_dieu_khien_bot.message_handler(commands=['phantich'])
def lenh_phantich(msg): xu_ly_lenh.xu_ly_phantich_dang_ky(trung_tam_dieu_khien_bot, msg)

@trung_tam_dieu_khien_bot.message_handler(commands=['file'])
def lenh_file(msg): xu_ly_lenh.xu_ly_file(trung_tam_dieu_khien_bot, msg)

@trung_tam_dieu_khien_bot.message_handler(commands=['chatmoi'])
def lenh_chat_moi(msg): xu_ly_lenh.xu_ly_chat_moi(trung_tam_dieu_khien_bot, msg)

@trung_tam_dieu_khien_bot.message_handler(commands=['luuchat'])
def lenh_luu_chat(msg): xu_ly_lenh.xu_ly_luu_chat(trung_tam_dieu_khien_bot, msg)

@trung_tam_dieu_khien_bot.message_handler(commands=['nhapdulieu'])
def lenh_nhap_du_lieu(msg): xu_ly_lenh.xu_ly_nhap_du_lieu(trung_tam_dieu_khien_bot, msg)

@trung_tam_dieu_khien_bot.message_handler(commands=['copy'])
def lenh_copy(msg): xu_ly_lenh.xu_ly_copy(trung_tam_dieu_khien_bot, msg)

@trung_tam_dieu_khien_bot.message_handler(commands=['grill-me'])
def lenh_grill_me(msg): xu_ly_lenh.xu_ly_grill_me(trung_tam_dieu_khien_bot, msg)

@trung_tam_dieu_khien_bot.message_handler(commands=['mohinh'])
def lenh_mo_hinh(msg): xu_ly_lenh.xu_ly_mo_hinh(trung_tam_dieu_khien_bot, msg)

@trung_tam_dieu_khien_bot.message_handler(commands=['thongtin'])
def lenh_thong_tin(msg): xu_ly_lenh.xu_ly_thong_tin(trung_tam_dieu_khien_bot, msg)

@trung_tam_dieu_khien_bot.message_handler(content_types=['photo'])
def lenh_nhan_anh(msg):
    xu_ly_lenh.xu_ly_anh_gui_len(trung_tam_dieu_khien_bot, msg)

@trung_tam_dieu_khien_bot.message_handler(content_types=['document'])
def lenh_nhap_tep_doc(msg):
    xu_ly_lenh.xu_ly_nhap_du_lieu(trung_tam_dieu_khien_bot, msg)

@trung_tam_dieu_khien_bot.message_handler(func=lambda msg: True)
def xu_ly_tin_nhan_mac_dinh(msg):
    xu_ly_lenh.xu_ly_gui_tin_nhan_gemini(trung_tam_dieu_khien_bot, msg)

if __name__ == "__main__":
    luong_tien_trinh_web = threading.Thread(target=kich_hoat_may_chu_web_ngam)
    luong_tien_trinh_web.daemon = True
    luong_tien_trinh_web.start()
    trung_tam_dieu_khien_bot.infinity_polling()