import asyncio
import os
import logging

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

from message_texts import GREETING, HELP


TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=GREETING)
    await asyncio.sleep(0.3)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=HELP)
    await asyncio.sleep(0.3)


async def schedule_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    chat_id = update.effective_chat.id

    # Schedule the message to be sent after 5 minutes
    delay = 5 * 60
    loop = asyncio.get_event_loop()
    loop.call_later(delay, asyncio.ensure_future, send_message(chat_id, message, context))

    # Schedule the message to be sent after 20 minutes
    delay = 20 * 60
    loop = asyncio.get_event_loop()
    loop.call_later(delay, asyncio.ensure_future, send_message(chat_id, message, context))

    # Schedule the message to be sent after 8 hours
    delay = 8 * 60 * 60
    loop = asyncio.get_event_loop()
    loop.call_later(delay, asyncio.ensure_future, send_message(chat_id, message, context))

    # Schedule the message to be sent after 24 hours
    delay = 24 * 60 * 60
    loop = asyncio.get_event_loop()
    loop.call_later(delay, asyncio.ensure_future, send_message(chat_id, message, context))

    await context.bot.send_message(chat_id=chat_id, text='Message scheduled successfully!')
    await asyncio.sleep(0.3)


async def send_message(chat_id, message, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=chat_id, text=message)
    await asyncio.sleep(0.3)


async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")
    await asyncio.sleep(0.3)


if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    start_handler = CommandHandler('start', start_command)
    application.add_handler(start_handler)

    help_handler = CommandHandler('help', help_command)
    application.add_handler(help_handler)

    message_handler = MessageHandler(filters.TEXT, schedule_message)
    application.add_handler(message_handler)

    unknown_command_handler = MessageHandler(filters.COMMAND, unknown_command)
    application.add_handler(unknown_command_handler)

    application.run_polling()
