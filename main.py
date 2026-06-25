import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
INVITE_LINK = "https://t.me/+Ll9Js3HxCYk4ZjAx"

known_users = set()

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Oi! Sou o Doramabot do Clube de Doramas.")

async def anuncio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Use: /anuncio sua mensagem")
        return
    msg = " ".join(context.args)
    if known_users:
        mentions = " ".join([f"<a href='tg://user?id={uid}'>\u2060</a>" for uid in known_users])
        text = f"{msg}\n\n{mentions}"
    else:
        text = msg
    await update.message.reply_html(text)

async def divulgar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = (
        "✨ Clube de Doramas Catálogo ✨\n\n"
        "Vem comentar dorama com a gente no Telegram!\n"
        "Lançamentos, indicações e surto coletivo 💜\n\n"
        f"Entra aqui: {INVITE_LINK}"
    )
    await update.message.reply_text(texto)

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        known_users.add(member.id)
        nome = member.first_name
        await update.message.reply_text(
            f"Bem-vinda, {nome}! 💜\n"
            "Se apresenta e conta qual dorama tá maratonando."
        )

async def track_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.from_user:
        known_users.add(update.message.from_user.id)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("anuncio", anuncio))
    app.add_handler(CommandHandler("divulgar", divulgar))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, track_users))
    app.run_polling()

if __name__ == "__main__":
    main()
