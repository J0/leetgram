from telegram.ext import Updater
from telegram.ext import CommandHandler
import requests
import random

updater = Updater(token='yada', use_context=True)

def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

def random_question(update, context):
    LEETCODE_LINK = "https://leetcode.com/problems/"
    NUM_QUESTIONS = 957
    r = requests.get('https://leetcode.com/api/problems/algorithms/')
    question_id = random.randint(0, NUM_QUESTIONS - 1)
    question_title = r.json()["stat_status_pairs"][question_id]["stat"]["question__article__slug"]
    context.bot.send_message(chat_id=update.message.chat_id, text="Here is your question of the day: {}".format(LEETCODE_LINK + question_title))
   
dispatcher = updater.dispatcher
start_handler = CommandHandler('start', start)
random_question_handler = CommandHandler('random_question', random_question)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(random_question_handler)
updater.start_polling()
