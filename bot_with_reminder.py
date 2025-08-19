from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import os
import logging
import datetime
import re

# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Token bot
TOKEN = os.getenv('TELEGRAM_TOKEN', "8446128745:AAGRBVniJe6PGWjSBrZvyZpHJnDLmqrjPrc")
USER_BOT = os.getenv('BOT_USERNAME', "@fmipausb_bot")

def start_command(bot, update):
    """Handle /mulai command"""
    keyboard = [
        [InlineKeyboardButton("📋 Chat ID", callback_data="show_chatid")],
        [InlineKeyboardButton("⏰ Set Reminder", callback_data="show_reminder_help")],
        [InlineKeyboardButton("❓ Bantuan", callback_data="show_help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text(
        "🤖 *Selamat datang di Bot FMIPA!*\n\n"
        "Bot ini dapat membantu Anda:\n"
        "• 📋 Mendapatkan Chat ID\n"
        "• ⏰ Mengatur Reminder/Alarm\n"
        "• 💬 Chat interaktif\n\n"
        "Pilih menu di bawah atau ketik /bantuan",
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

def help_command(bot, update):
    """Handle /bantuan command"""
    update.message.reply_text(
        "📚 *Daftar perintah yang tersedia:*\n\n"
        "🏠 `/mulai` - Menu utama\n"
        "❓ `/bantuan` - Daftar perintah\n"
        "📋 `/chatid` - Chat ID Anda\n"
        "⏰ `/reminder` - Set reminder/alarm\n"
        "📅 `/jadwal` - Lihat jadwal reminder\n"
        "🗑️ `/hapus` - Hapus reminder\n\n"
        "⏰ *Format Reminder:*\n"
        "`/reminder 5m Minum obat`\n"
        "`/reminder 2h Meeting dengan client`\n"
        "`/reminder 1d Deadline tugas`\n"
        "`/reminder 15:30 Rapat tim`\n"
        "`/reminder 2024-12-25 Hari Natal`",
        parse_mode='Markdown'
    )

def reminder_command(bot, update):
    """Handle /reminder command"""
    text = update.message.text
    args = text.split(' ', 2)  # Split menjadi max 3 bagian
    
    if len(args) < 3:
        keyboard = [
            [InlineKeyboardButton("📖 Panduan Reminder", callback_data="show_reminder_help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        update.message.reply_text(
            "❌ *Format salah!*\n\n"
            "*Cara penggunaan:*\n"
            "`/reminder [waktu] [pesan]`\n\n"
            "*Contoh:*\n"
            "• `/reminder 5m Minum obat`\n"
            "• `/reminder 2h Meeting client`\n"
            "• `/reminder 1d Deadline tugas`\n"
            "• `/reminder 15:30 Rapat tim`",
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
        return
    
    time_str = args[1]
    message = args[2]
    
    # Parse waktu
    delay_seconds = parse_time(time_str)
    
    if delay_seconds is None:
        update.message.reply_text(
            "❌ *Format waktu salah!*\n\n"
            "*Format yang didukung:*\n"
            "• `5m` = 5 menit\n"
            "• `2h` = 2 jam\n"
            "• `1d` = 1 hari\n"
            "• `15:30` = jam 15:30 hari ini\n"
            "• `2024-12-25` = tanggal tertentu",
            parse_mode='Markdown'
        )
        return
    
    if delay_seconds < 0:
        update.message.reply_text(
            "❌ *Waktu sudah berlalu!*\n\n"
            "Silakan masukkan waktu yang akan datang.",
            parse_mode='Markdown'
        )
        return
    
    # Set reminder menggunakan job queue
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    
    # Simpan reminder info
    job_context = {
        'chat_id': chat_id,
        'user_id': user_id,
        'message': message,
        'original_time': time_str
    }
    
    # Buat job
    updater = update.message.bot._updater
    if hasattr(updater, 'job_queue') and updater.job_queue:
        job = updater.job_queue.run_once(send_reminder, delay_seconds, context=job_context)
        
        # Hitung waktu reminder
        target_time = datetime.datetime.now() + datetime.timedelta(seconds=delay_seconds)
        
        update.message.reply_text(
            "✅ *Reminder berhasil dibuat!*\n\n"
            "⏰ **Waktu:** {}\n"
            "💬 **Pesan:** {}\n"
            "🕐 **Akan diingatkan pada:**\n`{}`".format(
                time_str, 
                message, 
                target_time.strftime("%Y-%m-%d %H:%M:%S")
            ),
            parse_mode='Markdown'
        )
    else:
        update.message.reply_text(
            "❌ *Job queue tidak tersedia*\n\n"
            "Fitur reminder tidak dapat digunakan saat ini.",
            parse_mode='Markdown'
        )

def parse_time(time_str):
    """Parse string waktu menjadi detik"""
    try:
        # Format: 5m, 2h, 1d
        if re.match(r'^\d+[mhd]$', time_str):
            number = int(time_str[:-1])
            unit = time_str[-1]
            
            if unit == 'm':
                return number * 60
            elif unit == 'h':
                return number * 3600
            elif unit == 'd':
                return number * 86400
        
        # Format: 15:30 (jam hari ini)
        elif re.match(r'^\d{1,2}:\d{2}$', time_str):
            hour, minute = map(int, time_str.split(':'))
            if hour > 23 or minute > 59:
                return None
                
            now = datetime.datetime.now()
            target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            # Jika waktu sudah lewat hari ini, set untuk besok
            if target <= now:
                target += datetime.timedelta(days=1)
            
            delta = target - now
            return int(delta.total_seconds())
        
        # Format: 2024-12-25 (tanggal tertentu)
        elif re.match(r'^\d{4}-\d{2}-\d{2}$', time_str):
            target_date = datetime.datetime.strptime(time_str, '%Y-%m-%d')
            now = datetime.datetime.now()
            delta = target_date - now
            return int(delta.total_seconds())
        
        return None
    except:
        return None

def send_reminder(bot, job):
    """Kirim pesan reminder"""
    context = job.context
    chat_id = context['chat_id']
    message = context['message']
    
    bot.send_message(
        chat_id=chat_id,
        text="🔔 *REMINDER ALARM!*\n\n"
             "⏰ **Waktunya:** {}\n\n"
             "Jangan lupa! 😊\n\n"
             "_Reminder ini telah selesai._".format(message),
        parse_mode='Markdown'
    )

def jadwal_command(bot, update):
    """Handle /jadwal command - lihat reminder aktif"""
    update.message.reply_text(
        "📅 *Jadwal Reminder*\n\n"
        "Fitur untuk melihat daftar reminder yang aktif.\n"
        "_Akan segera hadir!_ 🚧\n\n"
        "Saat ini Anda dapat:\n"
        "• Membuat reminder dengan `/reminder`\n"
        "• Melihat panduan dengan `/bantuan`",
        parse_mode='Markdown'
    )

def hapus_command(bot, update):
    """Handle /hapus command - hapus reminder"""
    update.message.reply_text(
        "🗑️ *Hapus Reminder*\n\n"
        "Fitur untuk menghapus reminder yang aktif.\n"
        "_Akan segera hadir!_ 🚧\n\n"
        "Sementara ini, reminder akan otomatis\n"
        "terhapus setelah dijalankan.",
        parse_mode='Markdown'
    )

def chatid_command(bot, update):
    """Handle /chatid command"""
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    
    # Buat inline keyboard dengan tombol copy
    keyboard = [
        [InlineKeyboardButton("📋 Copy Chat ID", callback_data="copy_chat_{}".format(chat_id))],
        [InlineKeyboardButton("👤 Copy User ID", callback_data="copy_user_{}".format(user_id))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text(
        "📊 *Informasi ID Anda:*\n\n"
        "💬 Chat ID: `{}`\n"
        "👤 User ID: `{}`\n\n"
        "_Klik tombol di bawah untuk copy ID_".format(chat_id, user_id),
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

def button_callback(bot, update):
    """Handle button callback"""
    query = update.callback_query
    
    if query.data == "show_chatid":
        query.answer("📋 Menampilkan Chat ID")
        chatid_command(bot, update)
        
    elif query.data == "show_reminder_help":
        query.answer("⏰ Panduan Reminder")
        bot.send_message(
            chat_id=query.message.chat_id,
            text="⏰ *Cara Menggunakan Reminder:*\n\n"
                 "*Format:* `/reminder [waktu] [pesan]`\n\n"
                 "*Contoh Penggunaan:*\n"
                 "• `/reminder 5m Minum obat`\n"
                 "• `/reminder 30m Meeting tim`\n"
                 "• `/reminder 2h Istirahat`\n"
                 "• `/reminder 1d Deadline tugas`\n"
                 "• `/reminder 15:30 Rapat sore`\n"
                 "• `/reminder 2024-12-25 Hari Natal`\n\n"
                 "*Format waktu yang didukung:*\n"
                 "• `m` = menit (contoh: 5m, 30m)\n"
                 "• `h` = jam (contoh: 1h, 2h)\n"
                 "• `d` = hari (contoh: 1d, 7d)\n"
                 "• `HH:MM` = jam tertentu hari ini/besok\n"
                 "• `YYYY-MM-DD` = tanggal tertentu\n\n"
                 "Coba sekarang: `/reminder 1m Test reminder`",
            parse_mode='Markdown'
        )
        
    elif query.data == "show_help":
        query.answer("❓ Menampilkan bantuan")
        help_command(bot, update)
        
    elif query.data.startswith("copy_chat_"):
        query.answer("✅ Chat ID dikirim!")
        chat_id = query.data.replace("copy_chat_", "")
        bot.send_message(
            chat_id=query.message.chat_id,
            text="📋 *Chat ID untuk di-copy:*\n\n`{}`\n\n_Tekan dan tahan pada angka di atas untuk copy_".format(chat_id),
            parse_mode='Markdown'
        )
        bot.send_message(
            chat_id=query.message.chat_id,
            text=chat_id
        )
        
    elif query.data.startswith("copy_user_"):
        query.answer("✅ User ID dikirim!")
        user_id = query.data.replace("copy_user_", "")
        bot.send_message(
            chat_id=query.message.chat_id,
            text="👤 *User ID untuk di-copy:*\n\n`{}`\n\n_Tekan dan tahan pada angka di atas untuk copy_".format(user_id),
            parse_mode='Markdown'
        )
        bot.send_message(
            chat_id=query.message.chat_id,
            text=user_id
        )

def text_message(bot, update):
    """Handle text messages"""
    user_message = update.message.text.lower()
    
    # Respon pintar
    if any(word in user_message for word in ['halo', 'hai', 'hello', 'hi']):
        response = "👋 Halo! Senang bertemu dengan Anda!\n\nKetik /bantuan untuk melihat apa yang bisa saya lakukan."
    elif any(word in user_message for word in ['terima kasih', 'thanks', 'makasih']):
        response = "😊 Sama-sama! Senang bisa membantu Anda."
    elif any(word in user_message for word in ['reminder', 'alarm', 'ingatkan']):
        response = "⏰ Untuk membuat reminder, gunakan:\n`/reminder [waktu] [pesan]`\n\nContoh: `/reminder 30m Meeting tim`"
    elif any(word in user_message for word in ['bantuan', 'help', 'tolong']):
        response = "🆘 Saya di sini untuk membantu!\n\nKetik /bantuan untuk melihat semua perintah yang tersedia."
    else:
        response = "💬 Anda menulis: {}\n\nKetik /bantuan untuk melihat fitur yang tersedia.".format(update.message.text)
    
    update.message.reply_text(response, parse_mode='Markdown')

def error_handler(bot, update, error):
    """Handle errors"""
    error_message = "Terjadi kesalahan: {}".format(error)
    logger.error(error_message)
    if update and update.message:
        update.message.reply_text("❌ Maaf, terjadi kesalahan. Silakan coba lagi.")

def main():
    """Main function"""
    print("Starting Bot FMIPA with Reminder feature...")
    
    # Buat Updater dengan token
    updater = Updater(TOKEN)
    
    # Dapatkan dispatcher
    dp = updater.dispatcher
    
    # Command handlers
    dp.add_handler(CommandHandler("mulai", start_command))
    dp.add_handler(CommandHandler("start", start_command))  # Alias
    dp.add_handler(CommandHandler("bantuan", help_command))
    dp.add_handler(CommandHandler("help", help_command))  # Alias
    dp.add_handler(CommandHandler("chatid", chatid_command))
    dp.add_handler(CommandHandler("reminder", reminder_command))
    dp.add_handler(CommandHandler("alarm", reminder_command))  # Alias
    dp.add_handler(CommandHandler("jadwal", jadwal_command))
    dp.add_handler(CommandHandler("hapus", hapus_command))
    
    # Callback query handler untuk tombol
    dp.add_handler(CallbackQueryHandler(button_callback))
    
    # Text message handler
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, text_message))
    
    # Error handler
    dp.add_error_handler(error_handler)
    
    # Start polling
    print("Bot is running... Press Ctrl+C to stop")
    updater.start_polling(poll_interval=1)
    
    # Run until Ctrl+C
    updater.idle()

if __name__ == "__main__":
    main()
