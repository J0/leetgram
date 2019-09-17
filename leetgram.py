from telegram.ext import Updater
from telegram.ext import CommandHandler
import requests
import random
import os

updater = Updater(token=os.environ['TELEGRAM_KEY'], use_context=True)

def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="This bot will help you select random leetcode questions. Select a /random_question to start!")

def help(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Commands available:\n/random - produces a random question\n\n To build:\n /interview - Display upcoming interviews\n /systems: Random System Design question. \n /calc - do math\n /happy - tell me a joke ")

def happy(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Q: Why do the French like to eat snails?\nA: Because they hate fast food")

def random_question(update, context):
    LEETCODE_LINK = "https://leetcode.com/problems/"
    NUM_QUESTIONS = 957
    r = requests.get('https://leetcode.com/api/problems/algorithms/')
    question_id = random.randint(0, NUM_QUESTIONS - 1)
    question_title = r.json()["stat_status_pairs"][question_id]["stat"]["question__article__slug"]
    context.bot.send_message(chat_id=update.message.chat_id, text="Here is your question of the day: {}".format(LEETCODE_LINK + question_title))
   
dispatcher = updater.dispatcher
start_handler = CommandHandler('start', start)
random_question_handler = CommandHandler('random', random_question)
help_handler = CommandHandler('help', help)
happy_handler = CommandHandler('happy', happy)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(random_question_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(happy_handler)
updater.start_polling()
