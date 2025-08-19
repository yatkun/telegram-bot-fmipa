#!/bin/bash

# Script untuk menjalankan bot dengan stop semua instance dulu
# File: start_single_bot.sh

echo "Stopping all existing bot instances..."

# Kill semua proses bot
pkill -f "python.*bot" 2>/dev/null
pkill -f "bot_py36" 2>/dev/null  
pkill -f "bot_simple_copy" 2>/dev/null

echo "Waiting 5 seconds..."
sleep 5

# Cek apakah masih ada bot yang berjalan
RUNNING_BOTS=$(ps aux | grep "python.*bot" | grep -v grep | wc -l)

if [ "$RUNNING_BOTS" -gt 0 ]; then
    echo "Warning: Still have running bot processes!"
    ps aux | grep "python.*bot" | grep -v grep
    echo "Force killing..."
    pkill -9 -f "python.*bot" 2>/dev/null
    sleep 3
fi

echo "Starting single bot instance..."
cd "$HOME/telegram-bot-fmipa"
python3 bot_simple_copy.py
