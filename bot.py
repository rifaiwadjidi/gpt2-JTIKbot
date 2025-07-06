import os
import requests
from telegram.ext import Updater, MessageHandler, Filters
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("7628207191:AAGIbXPicedQ2Rex-TwmFx96PAyEXl8RNuM")
HF_API_URL = os.getenv("https://hf.space/embed/rifaiwadjidi/chatbot-gpt2/+/api/predict/")

def ask_model(prompt):
    try:
        res = requests.post(HF_API_URL, json={"data": [prompt]})
        return res.json()['data'][0]
    except:
        return "Maaf, model tidak merespons."

def handle_message(update, context):
    user_msg = update.message.text
    bot_reply = ask_model(user_msg)
    update.message.reply_text(bot_reply)

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    print("Bot berjalan...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
