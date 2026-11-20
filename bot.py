import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
from google import genai

# Load API keys
load_dotenv("APIkeys.env")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

# Connect to Gemini
client = genai.Client(api_key=GEMINI_KEY)

# Logging
logging.basicConfig(level=logging.INFO)

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "What's good! I'm your personal AI assistant. Send me a message."
    )

# Handle messages
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text

    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=message
        )

        await update.message.reply_text(response.text)

    except Exception as e:
        await update.message.reply_text("Something went wrong. Try again.")
        print(e)

# Run bot
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

print("Your AI Telegram bot is running!")

app.run_polling()