import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
import time

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

PIX_KEY = "63533394379"
ADMIN_IDS = [8513977991] # Pamela

WELCOME_TEXT = "🌸 Bem vindo ao nosso grupo de Doramas!\n\nEscolha seu plano abaixo:"

# salva quem fala no grupo
DB_FILE = "users.json"
try:
    with open(DB_FILE) as f:
        known_users = json.load(f)
except:
    known_users = {}

last_tag_time = {}

def save_users():
    with open(DB_FILE, "w") as f:
        json.dump(known_users, f)

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

# Boas-vindas no grupo - com marcação
@bot.message_handler(content_types=['new_chat_members'])
def welcome_new(message):
    for new_user in message.new_chat_members:
        # ignora o próprio bot entrando
        if new_user.id == bot.get_me().id:
            continue
        nome = new_user.first_name
        uid = new_user.id
        texto = f"🌸 Bem-vindo(a), <a href='tg://user?id={uid}'>{nome}</a>!\n\nEscolha seu plano abaixo:"
        bot.send_message(message.chat.id, texto, parse_mode="HTML", reply_markup=get_menu())

# Marca todo mundo - só a Pamela pode usar
def do_tag(chat_id, aviso, message):
    now = time.time()
    if now - last_tag_time.get(chat_id, 0) < 300:
        bot.reply_to(message, "Calma, espera 5 min pra marcar de novo.")
        return False
    last_tag_time[chat_id] = now

    mentions = []
    for uid, nome in list(known_users.items())[:50]:
        mentions.append(f"<a href='tg://user?id={uid}'>{nome}</a>")

    if mentions:
        bot.send_message(chat_id, f"{aviso}\n\n{' '.join(mentions)}", parse_mode="HTML")
    return True

@bot.message_handler(content_types=['text'], func=lambda m: m.chat.type in ['group', 'supergroup'])
def track_and_tag(message):
    uid = str(message.from_user.id)
    known_users[uid] = message.from_user.first_name
    save_users()

    # /marcar e /anuncio fazem a mesma coisa, só muda o nome
    if message.text.startswith('/marcar') or message.text.startswith('/anuncio'):
        if message.from_user.id not in ADMIN_IDS:
            return
        chat_id = message.chat.id
        aviso = message.text.replace('/marcar', '').replace('/anuncio', '').strip() or "Atenção pessoal!"
        do_tag(chat_id, aviso, message)

print("Doramabot rodando...")
bot.infinity_polling()
