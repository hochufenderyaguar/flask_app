# from threading import Thread
#
# import schedule
#
#
# def somecode():
#     pass
#
#
# def cache():
#     schedule.every().day.at("10:00").do(check_price)
#     while True:
#         schedule.run_pending()
#
#
# if __name__ == '__main__':
#     thread = Thread(target=cache)
#     thread.start()
import random

import schedule
from telegram import Bot
from telegram.ext import Updater, CommandHandler

TOKEN = ''
bot = Bot(TOKEN)

chat_id = None


def start(update, context):
    global chat_id
    chat_id = update.message.chat_id


def send_message():
    if chat_id:
        bot.send_message(chat_id=chat_id, text='1')


updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))

updater.start_polling()
schedule.every(10).seconds.do(send_message)
while True:
    schedule.run_pending()
updater.idle()
