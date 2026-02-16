
import os
import telebot
from groq import Groq

# جلب المفاتيح من بيئة GitHub الآمنة
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
GROQ_KEY = os.getenv('GROQ_API_KEY')
BINANCE_UID = "717654739"

bot = telebot.TeleBot(BOT_TOKEN)
client = Groq(api_key=GROQ_KEY)

@bot.message_handler(commands=['start'])
def welcome(message):
    msg = (
        "🚀 **OrbitX Global AI**\n\n"
        "✨ CV Pro: $1 | 🔗 LinkedIn: $3\n"
        "🎨 Content: $5 | 🤖 AI Agents: $10+\n\n"
        "💳 Pay to Binance UID: `" + BINANCE_UID + "`\n"
        "Then type **PAID** to receive your file!"
    )
    bot.reply_to(message, msg, parse_mode='Markdown')

@bot.message_handler(func=lambda m: True)
def handle(m):
    if m.text.lower() == "paid":
        bot.reply_to(m, "🔍 Verifying payment... OrbitX AI is generating your high-end file now.")
    else:
        bot.reply_to(m, "🎯 Request Saved! Please pay to UID: `" + BINANCE_UID + "` and type PAID.")

print("OrbitX Engine is Active...")
bot.polling()
