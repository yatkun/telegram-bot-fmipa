#!/bin/bash

# Script untuk menjalankan bot dengan restart otomatis
# File: run_bot.sh

BOT_DIR="$HOME/bot_telegram"  # Ganti sesuai path di hosting Anda
BOT_FILE="bot.py"
PYTHON_CMD="python3"  # Atau python jika hosting menggunakan python

cd "$BOT_DIR"

# Function untuk menjalankan bot
run_bot() {
    echo "$(date): Starting bot..."
    $PYTHON_CMD $BOT_FILE
    echo "$(date): Bot stopped. Exit code: $?"
}

# Loop untuk restart otomatis jika bot crash
while true; do
    run_bot
    echo "$(date): Restarting bot in 5 seconds..."
    sleep 5
done
