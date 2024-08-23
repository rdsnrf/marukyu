#import requests
#print(requests.__version__)
#from bs4 import BeautifulSoup
#from telegram import Bot
#from telegram.ext import Updater, CommandHandler, CallbackContext
#import logging
#import time

from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import logging
import requests
from bs4 import BeautifulSoup
import asyncio

# Configuration
TELEGRAM_TOKEN = '7074485841:AAFk-dNz4ZRNV99DYSwZBRPpHcvwdCIZABc'
CHAT_ID = 'MarukyuKoyamaen_bot'  # Replace with your chat ID
PRODUCT_URL = 'https://www.marukyu-koyamaen.co.jp/english/shop/products/1141020c1/'  # Replace with the URL of the product page

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def check_product_availability():
    response = requests.get(PRODUCT_URL)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the button by class name and check its display property
    button = soup.find(class_='single_add_to_cart_button button')

    # Simplified check
    if button and button.get('style') and 'display: block' in button['style']:
        return True
    return False

async def send_notification(context: CallbackContext):
    if check_product_availability():
        await context.bot.send_message(chat_id=CHAT_ID, text="The product is available! Check it out here: " + PRODUCT_URL)

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text('I will notify you when the product becomes available.')

async def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))

    # Schedule the send_notification function to run periodically
    application.job_queue.run_repeating(send_notification, interval=3600, first=0)  # Check every hour

    # Start polling
    await application.run_polling()

# Handling event loop for interactive environments
loop = asyncio.get_event_loop()
if loop.is_running():
    import nest_asyncio
    nest_asyncio.apply()
loop.run_until_complete(main())