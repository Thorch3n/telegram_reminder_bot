from datetime import timedelta, datetime
from apscheduler.schedulers.background import BackgroundScheduler
import pytz

def scheduler(job_queue):
    background_scheduler = BackgroundScheduler()
    background_scheduler.start()
    job_queue.scheduler = background_scheduler

def schedule_task(job_queue, chat_id, task, interval, unit):
    if unit == 'h':
        delta = timedelta(hours=interval)
    elif unit == 'd':
        delta = timedelta(days=interval)
    elif unit == 'w':
        delta = timedelta(weeks=interval)
    elif unit == 'm':
        delta = timedelta(days=30 * interval)  # упрощение для месяцев
    else:
        return

    # Используйте pytz для задания временной зоны
    tz = pytz.timezone('UTC')
    run_time = datetime.now(tz) + delta

    job_queue.run_once(send_reminder, run_time, context=(chat_id, task))

def send_reminder(context):
    job = context.job
    chat_id, task = job.context
    context.bot.send_message(chat_id, text=f"Напоминание: {task}")
