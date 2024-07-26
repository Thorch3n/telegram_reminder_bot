from bot import create_bot, setup_scheduler

if __name__ == "__main__":
    bot = create_bot()
    setup_scheduler(bot)
    bot.start_polling()
    bot.idle()