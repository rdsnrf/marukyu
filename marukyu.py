#import requests
#print(requests.__version__)
#from bs4 import BeautifulSoup
#from telegram import Bot
#from telegram.ext import Updater, CommandHandler, CallbackContext
#import logging
#import time

import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import tracemalloc
import asyncio
import requests
from bs4 import BeautifulSoup
tracemalloc.start()

import nest_asyncio
nest_asyncio.apply()

# Configuration
TELEGRAM_TOKEN = '7074485841:AAFk-dNz4ZRNV99DYSwZBRPpHcvwdCIZABc'
CHAT_ID = 'MarukyuKoyamaen_bot'  # Replace with your chat ID
# List of products with names and URLs
PRODUCTS = [
    {'name': 'Unkaku', 'url': 'https://www.marukyu-koyamaen.co.jp/english/shop/products/1141020c1/'},
    {'name': 'Aoarashi', 'url': 'https://www.marukyu-koyamaen.co.jp/english/shop/products/11a1040c1/'},
    {'name': 'Isuzu', 'url': 'https://www.marukyu-koyamaen.co.jp/english/shop/products/1191040c1/'},
    {'name': 'Chigi no Shiro', 'url': 'https://www.marukyu-koyamaen.co.jp/english/shop/products/1181040c1/'},
    {'name': 'Yugen', 'url': 'https://www.marukyu-koyamaen.co.jp/english/shop/products/1171020c1/'}
]

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def check_product_availability(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')

        # Check if the specific button is visible
        button = soup.find(class_='single_add_to_cart_button button')
        if button and button.get('style') and 'display: block' in button.get('style'):
            return True
        return False
    except requests.RequestException as e:
        logging.error(f"Error checking product availability: {e}")
        return False

async def send_notification(context: CallbackContext):
    for product in PRODUCTS:
        if check_product_availability(product['url']):
            await context.bot.send_message(chat_id=CHAT_ID, text=f"{product['name']} is available! Check it out here: {product['url']}")

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text('I will notify you when any of the products become available.')

async def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))

    # Ensure you have installed the job-queue support
    try:
        application.job_queue.run_repeating(send_notification, interval=300, first=0)  # Check every 5 minutes
    except AttributeError:
        logging.warning("JobQueue is not available. Make sure you have installed the job-queue optional dependencies.")

    # Start the bot
    await application.run_polling()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except RuntimeError as e:
        logging.error(f"RuntimeError: {e}")