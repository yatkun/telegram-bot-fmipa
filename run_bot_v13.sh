#!/bin/bash

# Script untuk menjalankan bot dengan restart otomatis (untuk python-telegram-bot v13)
# File: run_bot_v13.sh

BOT_DIR="$HOME/telegram-bot-fmipa"  # Ganti sesuai path di hosting Anda
BOT_FILE="bot_v13.py"
PYTHON_CMD="python3"  # Atau python jika hosting menggunakan python

cd "$BOT_DIR"

# Function untuk menjalankan bot
run_bot() {
    echo "$(date): Starting bot v13..."
    $PYTHON_CMD $BOT_FILE
    echo "$(date): Bot stopped. Exit code: $?"
}

# Loop untuk restart otomatis jika bot crash
while true; do
    run_bot
    echo "$(date): Restarting bot in 5 seconds..."
    sleep 5
done
