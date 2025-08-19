# Bot Telegram - Deployment ke Shared Hosting

## Langkah-langkah Deployment:

### 1. Upload File ke Hosting
Upload semua file ke folder di hosting Anda (misalnya: `~/bot_telegram/`)

### 2. Login SSH ke Hosting
```bash
ssh username@your-hosting-server.com
```

### 3. Install Dependencies
```bash
cd ~/bot_telegram
pip3 install --user -r requirements.txt
```

### 4. Set Permission untuk Script
```bash
chmod +x run_bot.sh
chmod +x check_bot.sh
```

### 5. Test Jalankan Bot
```bash
python3 bot.py
```

### 6. Setup Cron Job untuk Auto-restart
Buka crontab:
```bash
crontab -e
```

Tambahkan baris ini:
```bash
# Cek bot setiap 5 menit, restart jika mati
*/5 * * * * /bin/bash ~/bot_telegram/check_bot.sh

# Optional: Restart bot setiap hari jam 2 pagi
0 2 * * * pkill -f "python.*bot.py" && sleep 10 && /bin/bash ~/bot_telegram/run_bot.sh > ~/bot_telegram/bot.log 2>&1 &
```

### 7. Jalankan Bot di Background
```bash
nohup bash run_bot.sh > bot.log 2>&1 &
```

### 8. Cek Status Bot
```bash
# Cek apakah bot berjalan
ps aux | grep bot.py

# Cek log
tail -f bot.log
```

## File Structure:
```
~/bot_telegram/
├── bot.py              # Bot utama
├── requirements.txt    # Dependencies
├── .env               # Environment variables (TOKEN)
├── run_bot.sh         # Script untuk menjalankan bot
├── check_bot.sh       # Script untuk cek & restart bot
└── bot.log            # Log file
```

## Troubleshooting:

### Bot tidak bisa install packages:
```bash
# Coba install dengan --user flag
pip3 install --user python-telegram-bot python-dotenv
```

### Python command tidak dikenali:
```bash
# Cek python version
which python3
python3 --version

# Jika tidak ada, coba:
which python
python --version
```

### Permission denied:
```bash
chmod 755 run_bot.sh check_bot.sh
```
