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
response = requests.get(f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates')
print(response.json())

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
        logging.info(f"Fetching URL: {url}, Status Code: {response.status_code}")
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

# async def send_notification(context: CallbackContext):
#     available_products = []
#     unavailable_products = []

#     for product in PRODUCTS:
#         if check_product_availability(product['url']):
#             available_products.append(product['name'])
#         else:
#             unavailable_products.append(product['name'])

#     if available_products:
#         for product in available_products:
#             try:
#                 message = f"{product} is available! Check it out here: {product['url']}"
#                 await context.bot.send_message(chat_id=CHAT_ID, text=message)
#                 logging.info(f"Sent availability notification for {product}")
#             except Exception as e:
#                 logging.error(f"Failed to send message for {product}: {e}")
#     else:
#         try:
#             message = "None of the products are available at the moment."
#             await context.bot.send_message(chat_id=CHAT_ID, text=message)
#             logging.info("Sent no availability notification")
#         except Exception as e:
#             logging.error(f"Failed to send no availability message: {e}")

async def send_notification(context: CallbackContext):
    available_products = []
    unavailable_products = []

    for product in PRODUCTS:
        try:
            if check_product_availability(product['url']):
                available_products.append(product['name'])
            else:
                unavailable_products.append(product['name'])
        except Exception as e:
            logging.error(f"Error checking availability for {product['name']}: {e}")

    if available_products:
        message = "\n".join([f"{product} is available! Check it out here: {product['url']}" for product in available_products])
    else:
        message = "None of the products are available at the moment."

    try:
        # Debug logging
        logging.info(f"Attempting to send message to chat_id: {CHAT_ID}")
        logging.info(f"Message content: {message}")

        await context.bot.send_message(chat_id=CHAT_ID, text=message)
        logging.info("Message sent successfully.")
    except Exception as e:
        logging.error(f"Error sending notification: {e}")

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text('I will notify you when any of the products become available.')

async def check_command(update: Update, context: CallbackContext):
    logging.info("Received /check command")
    await send_notification(context)

async def test_command(update: Update, context: CallbackContext):
    await update.message.reply_text("Test command received!")

async def test_send_message(context: CallbackContext):
    try:
        test_chat_id = 'MarukyuKoyamaen_bot'  # Replace with a known working chat ID
        await context.bot.send_message(chat_id=test_chat_id, text="Test message from send_notification!")
        logging.info("Test message sent successfully.")
    except Exception as e:
        logging.error(f"Error sending test message: {e}")

async def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("check", check_command))
    application.add_handler(CommandHandler("test", test_command))  # Add test command handler
    application.add_handler(CommandHandler("test_send", test_send_message))


    # Ensure you have installed the job-queue support
    try:
        application.job_queue.run_repeating(send_notification, interval=300, first=0)  # Check every 5 minutes
        logging.info("Job queue started.")
    except AttributeError:
        logging.warning("JobQueue is not available. Make sure you have installed the job-queue optional dependencies.")
    except Exception as e:
        logging.error(f"Error starting job queue: {e}")

    # Start the bot
    # await application.run_polling()

    try:
        await application.run_polling()
    except Exception as e:
        logging.error(f"Error running bot: {e}")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except RuntimeError as e:
        logging.error(f"RuntimeError: {e}")