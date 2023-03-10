import logging
import pandas as pd
from telegram import Update,Bot
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CommandHandler,JobQueue
import datetime
from dotenv import load_dotenv
import pytz
import os
load_dotenv()
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def getQuestions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    df = pd.read_excel('Questions.xlsx')
    index = df.sample(n=1).index
    question = df.iloc[index]['Questions'].to_string(index=False)
    link = df.iloc[index]['Links'].to_string(index=False)
    result =  f"Question: {question}\nLink: {link}"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=result)


async def getQuestionsOnce(context: ContextTypes.DEFAULT_TYPE):
    print("Hello")
    df = pd.read_excel('Questions.xlsx')
    index = df.sample(n=1).index
    question = df.iloc[index]['Questions'].to_string(index=False)
    link = df.iloc[index]['Links'].to_string(index=False)
    result =  f"Question: {question}\nLink: {link}"
    await context.bot.send_message(chat_id="@DailyChallenger", text=result)


async def main():
    bot = Bot("5886411017:AAFWeXE3_BAst74tFAmmh8seofLDAWT5Dtc")
    async with bot:
        print(await bot.get_me())

if __name__ == '__main__':
    application = ApplicationBuilder().token(os.getenv('API_KEY')).build()
    if(not application._job_queue):
        application._job_queue = JobQueue()

    asian = pytz.timezone('Asia/Kolkata')

    start_handler = CommandHandler('start', start)
    question_handler = CommandHandler('question',getQuestions)
    application.add_handler(start_handler)
    application.add_handler(question_handler)
    job_daily = application.job_queue.run_daily(getQuestionsOnce, days=(0,1,2,3,4,5,6), time=datetime.time(hour=7, minute=00, second=00,tzinfo=asian))
    application.run_polling()