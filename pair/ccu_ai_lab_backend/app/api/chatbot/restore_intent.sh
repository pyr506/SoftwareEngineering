#!/bin/bash
ABSOLUTE_PATH="/home/hacker/桌面/軟體工程網頁/software_engineering/pair/ccu_ai_lab_backend/app/api/chatbot"

mv "$ABSOLUTE_PATH"/intents.json "$ABSOLUTE_PATH"/restore_intents.json
mv "$ABSOLUTE_PATH"/old_intents.json "$ABSOLUTE_PATH"/intents.json

python3 "$ABSOLUTE_PATH"/train.py
