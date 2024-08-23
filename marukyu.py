#import requests
#print(requests.__version__)
#from bs4 import BeautifulSoup
#from telegram import Bot
#from telegram.ext import Updater, CommandHandler, CallbackContext
#import logging
#import time

import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext, ContextTypes
import tracemalloc
tracemalloc.start()

# Configuration
TELEGRAM_TOKEN = '7074485841:AAFk-dNz4ZRNV99DYSwZBRPpHcvwdCIZABc'
CHAT_ID = 'MarukyuKoyamaen_bot'  # Replace with your chat ID
PRODUCT_URL = 'https://www.marukyu-koyamaen.co.jp/english/shop/products/1141020c1/'  # Replace with the URL of the product page

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def check_product_availability():
    # Add your product checking logic here
    return True  # Example: Always returning True for testing

async def send_notification(context: CallbackContext):
    if await check_product_availability():
        await context.bot.send_message(chat_id=CHAT_ID, text="The product is available! Check it out here: " + PRODUCT_URL)

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text('I will notify you when the product becomes available.')

async def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))

    # Ensure you have installed the job-queue support
    try:
        application.job_queue.run_repeating(send_notification, interval=300, first=0)  # Check every hour
    except AttributeError:
        logging.warning("JobQueue is not available. Make sure you have installed the job-queue optional dependencies.")

    # Start the bot
    #await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())