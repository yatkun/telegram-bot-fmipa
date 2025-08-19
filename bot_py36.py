from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import logging

# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Token bot
TOKEN = os.getenv('TELEGRAM_TOKEN', "8446128745:AAGRBVniJe6PGWjSBrZvyZpHJnDLmqrjPrc")
USER_BOT = os.getenv('BOT_USERNAME', "@fmipausb_bot")

def start_command(update, context):
    """Handle /mulai command"""
    update.message.reply_text(
        "Selamat datang di bot ini! Gunakan /bantuan untuk melihat daftar perintah yang tersedia."
    )

def help_command(update, context):
    """Handle /bantuan command"""
    update.message.reply_text(
        "Daftar perintah yang tersedia:\n"
        "/mulai - Memulai bot\n"
        "/bantuan - Menampilkan daftar perintah\n"
        "/chatid - Menampilkan chat ID Anda\n"
    )

def chatid_command(update, context):
    """Handle /chatid command"""
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    update.message.reply_text(
        "Chat ID: {}\nUser ID: {}".format(chat_id, user_id)
    )

def text_message(update, context):
    """Handle text messages"""
    user_message = update.message.text
    response = "Anda mengirim pesan: {}".format(user_message)
    update.message.reply_text(response)

def error_handler(update, context):
    """Handle errors"""
    error_message = "Terjadi kesalahan: {}".format(context.error)
    logger.error(error_message)
    if update:
        update.message.reply_text(error_message)

def main():
    """Main function"""
    print("Starting bot...")
    
    # Buat Updater dengan token
    updater = Updater(TOKEN, use_context=True)
    
    # Dapatkan dispatcher
    dp = updater.dispatcher
    
    # Command handlers
    dp.add_handler(CommandHandler("mulai", start_command))
    dp.add_handler(CommandHandler("bantuan", help_command))
    dp.add_handler(CommandHandler("chatid", chatid_command))
    
    # Text message handler
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, text_message))
    
    # Error handler
    dp.add_error_handler(error_handler)
    
    # Start polling
    print("Pooling...")
    updater.start_polling(poll_interval=1)
    
    # Run until Ctrl+C
    updater.idle()

if __name__ == "__main__":
    main()
