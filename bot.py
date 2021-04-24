import schedule
from telegram import Bot
from telegram.ext import Updater, CommandHandler

TOKEN = ''
bot = Bot(TOKEN)

chat_id = None


def start(update, context):
    global chat_id
    chat_id = update.message.chat_id
    update.message.reply_text(
        "Спасибо за регистрацию, теперь можете переходить в свой личный кабинет на сайте, чтобы добавить товары.")


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
