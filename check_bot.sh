#!/bin/bash

# Script untuk mengecek dan merestart bot jika mati
# File: check_bot.sh

BOT_DIR="$HOME/bot_telegram"  # Ganti sesuai path di hosting Anda
PYTHON_CMD="python3"

# Cek apakah bot sedang jalan
BOT_PID=$(pgrep -f "python.*bot.py")

if [ -z "$BOT_PID" ]; then
    echo "$(date): Bot tidak berjalan, memulai ulang..."
    cd "$BOT_DIR"
    nohup bash run_bot.sh > bot.log 2>&1 &
    echo "$(date): Bot dimulai ulang"
else
    echo "$(date): Bot masih berjalan (PID: $BOT_PID)"
fi
