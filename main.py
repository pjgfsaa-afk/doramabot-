import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
import time

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

PIX_KEY = "63533394379"
ADMIN_IDS = [8513977991]

WELCOME_TEXT = "🌸 Bem vindo ao nosso grupo de Doramas!\n\nEscolha seu plano abaixo:"

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

@bot.message_handler(commands=['divulgar'])
def divulgar(message):
    texto = "✨ Clube de Doramas Catálogo ✨\n\nVem comentar dorama com a gente no Telegram!\nLançamentos, indicações e surto coletivo 💜\n\nEntra aqui: https://t.me/+Ll9Js3HxCYk4ZjAx"
    bot.reply_to(message, texto)

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

# NOVO: recebe comprovante em foto ou PDF e te encaminha
@bot.message_handler(content_types=['photo', 'document'])
def receber_comprovante(message):
    user = message.from_user
    nome = user.first_name
    username = f"@{user.username}" if user.username else nome
    legenda = f"Comprovante de {username}\nid: {user.id}"

    for admin_id in ADMIN_IDS:
        try:
            if message.content_type == 'photo':
                file_id = message.photo[-1].file_id
                bot.send_photo(admin_id, file_id, caption=legenda)
            else:
                bot.send_document(admin_id, message.document.file_id, caption=legenda)
        except Exception as e:
            print(f"Erro ao encaminhar pra {admin_id}: {e}")

    bot.reply_to(message, "Comprovante recebido! Vou conferir e liberar seu acesso em breve 💜")

@bot.message_handler(content_types=['new_chat_members'])
def welcome_new(message):
    for new_user in message.new_chat_members:
        nome = new_user.first_name
        texto = f"🌸 Bem-vindo(a), {nome}!\n\nAproveita nossos doramas! Se precisar de ajuda, chama no privado @Doramabot"
        bot.send_message(message.chat.id, texto)

@bot.message_handler(content_types=['text'], func=lambda m: m.chat.type in ['group', 'supergroup'])
def track_and_tag(message):
    uid = str(message.from_user.id)
    known_users[uid] = message.from_user.first_name
    save_users()
    if message.text.startswith('/marcar'):
        if message.from_user.id not in ADMIN_IDS:
            return
        chat_id = message.chat.id
        now = time.time()
        if now - last_tag_time.get(chat_id, 0) < 300:
            bot.reply_to(message, "Calma, espera 5 min pra marcar de novo.")
            return
        last_tag_time[chat_id] = now
        aviso = message.text.replace('/marcar', '').strip() or "Atenção pessoal!"
        mentions = []
        for uid, nome in list(known_users.items())[:50]:
            mentions.append(f"<a href='tg://user?id={uid}'>{nome}</a>")
        if mentions:
            bot.send_message(chat_id, f"{aviso}\n\n{' '.join(mentions)}", parse_mode="HTML")

print("Doramabot rodando...")
bot.infinity_polling()
