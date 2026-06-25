import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

PIX_KEY = "63533394379"

WELCOME_TEXT = "🌸 Bem vindo ao nosso grupo de Doramas!\n\nEscolha seu plano abaixo:"

def get_menu():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("1 Dorama - R$ 7", callback_data="plano_1"))
    markup.add(InlineKeyboardButton("3 Doramas - R$ 10", callback_data="plano_3"))
    markup.add(InlineKeyboardButton("Grupo Semanal - R$ 10", callback_data="plano_semanal"))
    markup.add(InlineKeyboardButton("Vitalício - R$ 40", callback_data="plano_vitalicio"))
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, WELCOME_TEXT, reply_markup=get_menu())

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "plano_1":
        text = f"1 Dorama - R$ 7\n\nChave Pix (CPF):\n`{PIX_KEY}`\n\nEnvie o comprovante aqui que eu libero seu dorama!"
    elif call.data == "plano_3":
        text = f"3 Doramas - R$ 10\n\nChave Pix (CPF):\n`{PIX_KEY}`\n\nEnvie o comprovante aqui que eu libero seus doramas!"
    elif call.data == "plano_semanal":
        text = f"Grupo Semanal - R$ 10\n\nChave Pix (CPF):\n`{PIX_KEY}`\n\nApós pagar, envie o comprovante aqui que eu libero seu acesso!"
    elif call.data == "plano_vitalicio":
        text = f"Vitalício - R$ 40\n\nChave Pix (CPF):\n`{PIX_KEY}`\n\nApós pagar, envie o comprovante aqui que eu libero seu acesso!"
    else:
        return
    
    bot.send_message(call.message.chat.id, text, parse_mode="Markdown")
    bot.answer_callback_query(call.id)

print("Doramabot rodando...")
bot.infinity_polling()
