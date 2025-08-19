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

def start_command(bot, update):
    """Handle /mulai command"""
    update.message.reply_text(
        "Selamat datang di bot ini! Gunakan /bantuan untuk melihat daftar perintah yang tersedia."
    )

def help_command(bot, update):
    """Handle /bantuan command"""
    update.message.reply_text(
        "Daftar perintah yang tersedia:\n"
        "/mulai - Memulai bot\n"
        "/bantuan - Menampilkan daftar perintah\n"
        "/chatid - Menampilkan chat ID Anda\n"
    )

def chatid_command(bot, update):
    """Handle /chatid command dengan format yang mudah di-copy"""
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    
    # Format dengan monospace agar mudah di-copy
    update.message.reply_text(
        "📊 *Informasi ID Anda:*\n\n"
        "💬 Chat ID:\n`{}`\n\n"
        "👤 User ID:\n`{}`\n\n"
        "_Tekan dan tahan pada ID di atas untuk copy_".format(chat_id, user_id),
        parse_mode='Markdown'
    )
    
    # Kirim pesan terpisah untuk kemudahan copy
    update.message.reply_text("Chat ID: {}".format(chat_id))
    update.message.reply_text("User ID: {}".format(user_id))

def text_message(bot, update):
    """Handle text messages"""
    user_message = update.message.text
    response = "Anda mengirim pesan: {}".format(user_message)
    update.message.reply_text(response)

def error_handler(bot, update, error):
    """Handle errors"""
    error_message = "Terjadi kesalahan: {}".format(error)
    logger.error(error_message)
    if update:
        update.message.reply_text(error_message)

def main():
    """Main function"""
    print("Starting bot...")
    
    # Buat Updater dengan token (tanpa use_context untuk versi lama)
    updater = Updater(TOKEN)
    
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
