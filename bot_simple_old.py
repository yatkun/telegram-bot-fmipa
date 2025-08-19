import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os

# Token bot
TOKEN = "8446128745:AAGRBVniJe6PGWjSBrZvyZpHJnDLmqrjPrc"

def start(bot, update):
    update.message.reply_text("Selamat datang di bot ini! Gunakan /bantuan untuk melihat daftar perintah.")

def bantuan(bot, update):
    update.message.reply_text(
        "Daftar perintah:\n"
        "/mulai - Memulai bot\n"
        "/bantuan - Bantuan\n"
        "/chatid - Chat ID Anda"
    )

def chatid(bot, update):
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    update.message.reply_text("Chat ID: {}\nUser ID: {}".format(chat_id, user_id))

def echo(bot, update):
    update.message.reply_text("Anda menulis: {}".format(update.message.text))

def error(bot, update, error):
    print("Error: {}".format(error))

def main():
    print("Starting simple bot...")
    
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("mulai", start))
    dp.add_handler(CommandHandler("bantuan", bantuan))
    dp.add_handler(CommandHandler("chatid", chatid))
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_error_handler(error)
    
    print("Bot polling...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
