import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

# ====== KONFIGURASI ======
TELEGRAM_TOKEN = "7628207191:AAGIbXPicedQ2Rex-TwmFx96PAyEXl8RNuM"
MODEL_REPO = "rifaiwadjidi/gpt2_JTIKbot"

# ====== SETUP ======
logging.basicConfig(level=logging.INFO)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load model dan tokenizer dari Hugging Face
tokenizer = GPT2Tokenizer.from_pretrained(MODEL_REPO)
model = GPT2LMHeadModel.from_pretrained(MODEL_REPO).to(device)

def generate_response(prompt_text, max_length=200):
    inputs = tokenizer(prompt_text, return_tensors="pt").to(device)
    outputs = model.generate(
        inputs["input_ids"],
        max_length=max_length,
        num_return_sequences=1,
        pad_token_id=tokenizer.eos_token_id,
    )
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    if prompt_text in response:
        response = response.replace(prompt_text, "").strip()
    if "[SEP]" in response:
        response = response.split("[SEP]")[1].strip()
    return response

# ====== HANDLER TELEGRAM ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Saya JTIKbot. Silakan bertanya tentang informasi akademik JTIK.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    reply = generate_response(f"Pertanyaan: {user_input}\n")
    await update.message.reply_text(reply)

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()