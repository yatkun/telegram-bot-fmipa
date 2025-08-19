#!/bin/bash

# Script untuk menjalankan bot dengan restart otomatis (Python 3.6)
# File: run_bot_py36.sh

BOT_DIR="$HOME/telegram-bot-fmipa"  # Ganti sesuai path di hosting Anda
BOT_FILE="bot_py36.py"
PYTHON_CMD="python3"

cd "$BOT_DIR"

# Function untuk menjalankan bot
run_bot() {
    echo "$(date): Starting bot for Python 3.6..."
    $PYTHON_CMD $BOT_FILE
    echo "$(date): Bot stopped. Exit code: $?"
}

# Loop untuk restart otomatis jika bot crash
while true; do
    run_bot
    echo "$(date): Restarting bot in 5 seconds..."
    sleep 5
done
