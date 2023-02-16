import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from message_texts import GREETING, HELP, REMEMBER
import sqlite3
import datetime


conn = sqlite3.connect('users.db')
cur = conn.cursor()
with conn:
    cur.execute('''
    CREATE TABLE IF NOT EXISTS bot_users (
        id integer primary key AUTOINCREMENT,
        created_at TIMESTAMP default current_timestamp not null,
        telegram_id bigint UNIQUE not null
    );
    ''')


TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    created_at = datetime.datetime.now()
    telegram_id = update.effective_user.id
    user = (created_at, telegram_id)
    with conn:
        cur.execute('''INSERT OR IGNORE INTO bot_users (created_at, telegram_id)
        VALUES(?, ?);''', user)

    await context.bot.send_message(chat_id=update.effective_chat.id, text=GREETING)


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=HELP)


async def remember(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=REMEMBER)


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    help_handler = CommandHandler('help', help)
    application.add_handler(help_handler)

    remember_handler = CommandHandler('remember', remember)
    application.add_handler(remember_handler)

    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)

    application.run_polling()
