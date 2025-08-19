from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
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
    """Handle /chatid command"""
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    
    # Buat inline keyboard dengan tombol copy
    keyboard = [
        [InlineKeyboardButton("📋 Tampilkan Chat ID", callback_data="show_chat_{}".format(chat_id))],
        [InlineKeyboardButton("👤 Tampilkan User ID", callback_data="show_user_{}".format(user_id))],
        [InlineKeyboardButton("🔄 Tampilkan Semua", callback_data="show_all_{}_{}".format(chat_id, user_id))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text(
        "📊 *Informasi ID Anda*\n\n"
        "Klik tombol di bawah untuk menampilkan ID dalam format yang mudah di-copy:",
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

def button_callback(bot, update):
    """Handle button callback"""
    query = update.callback_query
    
    if query.data.startswith("show_chat_"):
        chat_id = query.data.replace("show_chat_", "")
        query.answer("💬 Chat ID dikirim!")
        
        # Kirim dalam beberapa format untuk kemudahan copy
        bot.send_message(
            chat_id=query.message.chat_id,
            text="📋 **CHAT ID:**"
        )
        bot.send_message(
            chat_id=query.message.chat_id,
            text=chat_id,
            reply_to_message_id=query.message.message_id
        )
        bot.send_message(
            chat_id=query.message.chat_id,
            text="`{}`".format(chat_id),
            parse_mode='Markdown'
        )
        
    elif query.data.startswith("show_user_"):
        user_id = query.data.replace("show_user_", "")
        query.answer("👤 User ID dikirim!")
        
        bot.send_message(
            chat_id=query.message.chat_id,
            text="👤 **USER ID:**"
        )
        bot.send_message(
            chat_id=query.message.chat_id,
            text=user_id,
            reply_to_message_id=query.message.message_id
        )
        bot.send_message(
            chat_id=query.message.chat_id,
            text="`{}`".format(user_id),
            parse_mode='Markdown'
        )
        
    elif query.data.startswith("show_all_"):
        data_parts = query.data.replace("show_all_", "").split("_")
        chat_id = data_parts[0]
        user_id = data_parts[1]
        query.answer("📋 Semua ID dikirim!")
        
        bot.send_message(
            chat_id=query.message.chat_id,
            text="📊 **SEMUA ID ANDA:**"
        )
        bot.send_message(
            chat_id=query.message.chat_id,
            text="💬 Chat ID: {}".format(chat_id)
        )
        bot.send_message(
            chat_id=query.message.chat_id,
            text="👤 User ID: {}".format(user_id)
        )
        # Format monospace untuk copy mudah
        bot.send_message(
            chat_id=query.message.chat_id,
            text="```\nChat ID: {}\nUser ID: {}\n```".format(chat_id, user_id),
            parse_mode='Markdown'
        )

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
    print("Starting bot with better copy buttons...")
    
    # Buat Updater dengan token (tanpa use_context untuk versi lama)
    updater = Updater(TOKEN)
    
    # Dapatkan dispatcher
    dp = updater.dispatcher
    
    # Command handlers
    dp.add_handler(CommandHandler("mulai", start_command))
    dp.add_handler(CommandHandler("bantuan", help_command))
    dp.add_handler(CommandHandler("chatid", chatid_command))
    
    # Callback query handler untuk tombol
    dp.add_handler(CallbackQueryHandler(button_callback))
    
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
