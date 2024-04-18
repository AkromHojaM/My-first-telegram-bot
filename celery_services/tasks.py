import os
from celery.schedules import crontab
import asyncio
from dotenv import load_dotenv
from aiogram import Bot
from celery import Celery
from DB.Db import PG

TOKEN = os.getenv("TOKEN")
load_dotenv()
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_TIMEZONE = 'Asia/Tashkent'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'

app = Celery("celery_sevices.tasks",
             broker=CELERY_BROKER_URL,
             backend=CELERY_RESULT_BACKEND)
CELERY_BEAT_SCHEDULE = {
    'send-message-every-minute': {
        'task': 'PythonBot.celery_services.tasks.send_message',
        'schedule': crontab('*'),
        'args':(TOKEN,),
    }
}
app.conf.update({
    'timezone': CELERY_TIMEZONE,
    'beat_schedule': CELERY_BEAT_SCHEDULE,
})
@app.task(name='PythonBot.celery_services.tasks.send_message')
def send_message(bot_token):
    loop = asyncio.get_event_loop()
    obj = PG()
    bot = Bot(bot_token)
    all_users = obj.select_all_users()
    text = "Lokatsiyani jonating"
    for user in range(len(all_users)):
        try:
            loop.run_until_complete(bot.send_message(all_users[user][user],text))
        except Exception as e:
            return f"failed {e}"
        return "ok"