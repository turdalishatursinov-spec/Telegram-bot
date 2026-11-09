import telebot
from google import genai

# Telegram Bot Tokeningiz
TELEGRAM_BOT_TOKEN = "9137032691:AAGE8jBaHpr9YeVSRMnV_NAwfNqqi4LmdHs"

# Google Gemini API Kalitingiz
GEMINI_API_KEY = "AQ.Ab8RN6KKFp-QKR2aDl04iGkZ_2M_HfGQPShrzWVhSMb2N3fKLg"

# Bot va Gemini mijozlarini ishga tushiramiz
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
ai_client = genai.Client(api_key=GEMINI_API_KEY)

# 1. /start buyrug'i
@bot.message_handler(commands=['start'])
def start_message(message):
    user_name = message.from_user.first_name
    welcome_text = (
        f"Salom, {user_name}! 👋\n\n"
        "Men Google Gemini sun'iy intellekti asosida ishlaydigan yordamchi botman.\n"
        "Menga istalgan mavzuda savol berishingiz, matn tarjima qildirishingiz yoki g'oyalar so'rashingiz mumkin.\n\n"
        "Buyruqlar ro'yxati:\n"
        "/start - Botni qayta ishga tushirish\n"
        "/help - Yordam va ko'rsatmalar"
    )
    bot.reply_to(message, welcome_text)

# 2. /help buyrug'i
@bot.message_handler(commands=['help'])
def help_message(message):
    help_text = (
        "🤖 Botdan foydalanish bo'yicha yo'riqnoma:\n\n"
        "• Shunchaki xabar yuboring — Gemini AI sizga tezkor javob qaytaradi.\n"
        "• Kod yozish, matn muharrirligi, darslar yoki har qanday savollaringiz bo'yicha yordam olmashingiz mumkin.\n"
        "• Agar bot javob bermasa, tokenlar yoki internet aloqasini tekshiring."
    )
    bot.reply_to(message, help_text, parse_mode="Markdown")

# 3. Barcha matnli xabarlarni tutib olish va AI ga yuborish
@bot.message_handler(func=lambda message: True)
def handle_ai_chat(message):
    user_text = message.text
    
    # Telegramda "yozmoqda..." statusini ko'rsatish
    bot.send_chat_action(message.chat.id, 'typing')
    
    try:
        # Gemini AI modeliga so'rov yuborish
        response = ai_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_text,
        )
        
        # Javobni Telegram chatiga yuboramiz
        bot.reply_to(message, response.text)
        
    except Exception as e:
        # Xatolik yuz berganda uni bildirish
        bot.reply_to(message, f"❌ Xatolik yuz berdi: {e}")

print("Bot Telegramda muvaffaqiyatli ishga tushdi va barcha buyruqlar tayyor! 🚀")
bot.infinity_polling()
