
import os
import telebot # تأكد من تثبيت pyTelegramBotAPI
from groq import Groq

bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))
@bot.message_handler(commands=['start'])
def start(m): bot.reply_to(m, "👑 OrbitX Global AI: Active & Sovereign.")

print("OrbitX Engine Started...")
bot.polling()
