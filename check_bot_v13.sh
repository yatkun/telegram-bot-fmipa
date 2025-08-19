#!/bin/bash

# Script untuk mengecek dan merestart bot jika mati (untuk v13)
# File: check_bot_v13.sh

BOT_DIR="$HOME/telegram-bot-fmipa"  # Ganti sesuai path di hosting Anda
PYTHON_CMD="python3"

# Cek apakah bot sedang jalan
BOT_PID=$(pgrep -f "python.*bot_v13.py")

if [ -z "$BOT_PID" ]; then
    echo "$(date): Bot tidak berjalan, memulai ulang..."
    cd "$BOT_DIR"
    nohup bash run_bot_v13.sh > bot_v13.log 2>&1 &
    echo "$(date): Bot dimulai ulang"
else
    echo "$(date): Bot masih berjalan (PID: $BOT_PID)"
fi
