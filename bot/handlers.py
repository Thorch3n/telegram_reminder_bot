from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackContext
import re
from .scheduler import schedule_task

# Словарь для хранения последнего сообщения пользователя
last_messages = {}

# Словарь для перевода единиц времени
time_units = {
    'h': 'час(-a,-ов)',
    'd': 'день(-дней)',
    'w': 'неделю(-ь)',
    'm': 'месяц(-а,-ев)'
}

def register_handlers(dispatcher):
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), handle_message))
    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CommandHandler("help", help_command))

def start_command(update: Update, context: CallbackContext):
    update.message.reply_text("Привет! Я бот-напоминалка. Используйте команду /help для справки.")

def help_command(update: Update, context: CallbackContext):
    update.message.reply_text("Используйте @bot_name ctrl NM для создания напоминания, где N - интервал, а M - единица времени (h - час, d - день, w - неделя, m - месяц).")

def handle_message(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    message = update.message.text

    bot_username = context.bot.username

    # Проверяем, содержит ли сообщение команду "ctrl NM" и упомянут ли бот
    match = re.search(rf'@{bot_username} ctrl (\d+)([hdwm])', message, re.IGNORECASE)
    if match:
        interval = int(match.group(1))
        unit = match.group(2)
        task = last_messages.get((chat_id, user_id), "нет задачи")  # Используем последнее сообщение пользователя как задачу
        schedule_task(context.job_queue, chat_id, task, interval, unit)
        context.bot.send_message(chat_id, text=f"Задача *{task}* принята. Напомню о ней через {interval} {time_units[unit]}.")
    else:
        # Сохраняем текущее сообщение как последнее сообщение пользователя
        last_messages[(chat_id, user_id)] = message
        if update.message.chat.type == 'private':
            update.message.reply_text("Сообщение сохранено. Используйте @bot_name ctrl NM для создания напоминания.")
