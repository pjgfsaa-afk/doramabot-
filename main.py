import os
import telebot
from telebot import types

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(msg):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("1 DORAMA", callback_data="dorama1")
    btn2 = types.InlineKeyboardButton("3 DORAMAS", callback_data="dorama3")
    btn3 = types.InlineKeyboardButton("GRUPO SEMANAL", callback_data="semanal")
    markup.add(btn1, btn2, btn3)
    bot.send_message(msg.chat.id, "🌸 Bem-vinda ao Doramabot!", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "dorama1":
        texto = "✅ 1 DORAMA\n\nColoque seu texto aqui"
    elif call.data == "dorama3":
        texto = "✅ 3 DORAMAS\n\nColoque seu texto aqui"
    elif call.data == "semanal":
        texto = "✅ GRUPO SEMANAL\n\nColoque seu texto aqui"
    else:
        texto = "Opção não encontrada"
    bot.send_message(call.message.chat.id, texto)
    bot.answer_callback_query(call.id)

bot.infinity_polling()
