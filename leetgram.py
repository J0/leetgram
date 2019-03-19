from telegram.ext import Updater
from telegram.ext import CommandHandler
import requests
import random
import os
import logging

# Enable logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)
updater = Updater(token=os.environ["TELEGRAM_KEY"], use_context=True)


def start(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id, text="I'm a bot, please talk to me!"
    )


def generate_random_question():
    LEETCODE_LINK = "https://leetcode.com/problems/"
    NUM_QUESTIONS = 957
    r = requests.get("https://leetcode.com/api/problems/algorithms/")
    question_id = random.randint(0, NUM_QUESTIONS - 1)
    question_title = r.json()["stat_status_pairs"][question_id]["stat"][
        "question__article__slug"
    ]
    return LEETCODE_LINK + question_title


def send_random_question(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Here is your random question: {}".format(generate_random_question()),
    )


def schedule_question(update, context):
    chat_id = update.message.chat_id
    try:
        # args[0] should contain the time for the timer in days
        due = int(context.args[0])
        if due < 0:
            update.message.reply_text("The past is obdurate!")
            return
        # Add job to queue
        job = context.job_queue.run_daily(
            create_daily_question_job, due, context=chat_id
        )
        context.chat_data["job"] = job
        update.message.reply_text("Timer successfully set!")

    except (IndexError, ValueError):
        update.message.reply_text("Usage: /schedule_question <days>")


def create_daily_question_job(context):
    job = context.job
    context.bot.send_message(job.context, text="{}".format(generate_random_question()))


def unschedule_question(update, context):
    """Remove the job if the user changed their mind."""
    if "job" not in context.chat_data:
        update.message.reply_text("You have no active timer")
        return

    job = context.chat_data["job"]
    job.schedule_removal()
    del context.chat_data["job"]
    update.message.reply_text("Timer successfully unset!")


dispatcher = updater.dispatcher
start_handler = CommandHandler("start", start)
random_question_handler = CommandHandler("send_random_question", send_random_question)
schedule_question_handler = CommandHandler("schedule_question", schedule_question)
unschedule_question_handler = CommandHandler("unschedule_question", unschedule_question)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(random_question_handler)
updater.start_polling()
