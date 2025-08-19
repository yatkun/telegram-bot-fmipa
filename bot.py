from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, filters, Application, ContextTypes
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

TOKEN = os.getenv('TELEGRAM_TOKEN', "8446128745:AAGRBVniJe6PGWjSBrZvyZpHJnDLmqrjPrc")
USER_BOT = os.getenv('BOT_USERNAME', "@fmipausb_bot")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Selamat datang di bot ini! Gunakan /bantuan untuk melihat daftar perintah yang tersedia."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Daftar perintah yang tersedia:\n"
        "/mulai - Memulai bot\n"
        "/bantuan - Menampilkan daftar perintah\n"
        "/chatid - Menampilkan chat ID Anda\n"
    )

async def chatid_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    await update.message.reply_text(
        f"Chat ID: {chat_id}\n"
        f"User ID: {user_id}"
    )

async def text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    response = f"Anda mengirim pesan: {user_message}"
    await update.message.reply_text(response)

async def error_handler(update: Update, context: CallbackContext):
    error_message = f"Terjadi kesalahan: {context.error}"
    if update:
        await update.message.reply_text(error_message)
    else:
        print(error_message)


if __name__ == "__main__":
    print("Starting bot...")
    app = Application.builder().token(TOKEN).build()

    #command
    app.add_handler(CommandHandler("mulai", start_command))
    app.add_handler(CommandHandler("bantuan", help_command))
    app.add_handler(CommandHandler("chatid", chatid_command))

    #text message
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_message))

    #error handler
    app.add_error_handler(error_handler)

    #pooling
    print("Pooling...")
    app.run_polling(poll_interval=1)