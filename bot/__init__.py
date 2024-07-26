from telegram.ext import Updater
from .config import TELEGRAM_BOT_TOKEN
from .handlers import register_handlers

def create_bot():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    register_handlers(dispatcher)
    return updater

def setup_scheduler(bot):
    from .scheduler import scheduler

    job_queue = bot.job_queue
    scheduler(job_queue)
