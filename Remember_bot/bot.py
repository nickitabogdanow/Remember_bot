import asyncio
import os
import logging
import sqlite3
import datetime


from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

from message_texts import GREETING, HELP, REMEMBER, REMEMBER_PROCESS, LIST_OF_MESSAGES


conn = sqlite3.connect('db.sql')
cur = conn.cursor()
with conn:
    cur.execute('''
CREATE TABLE IF NOT EXISTS bot_users (
    id integer primary key,
    created_at TIMESTAMP default current_timestamp not null,
    telegram_id bigint UNIQUE not null
);
''')
    cur.execute('''
CREATE TABLE IF NOT EXISTS messages (
    id integer primary key,
    telegram_id bigint UNIQUE not null,
    created_at TIMESTAMP default current_timestamp not null,
    message VARCHAR UNIQUE,
    FOREIGN KEY(id) REFERENCES bot_user(id) on DELETE CASCADE
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
    await asyncio.sleep(0.3)


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=HELP)
    await asyncio.sleep(0.3)


async def remember(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=REMEMBER)
    await asyncio.sleep(0.3)


async def remember_process(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=REMEMBER_PROCESS)
    message = update.message.text
    telegram_id = update.effective_user.id
    created_at = datetime.datetime.now()
    user_message = (telegram_id, created_at, message)
    with conn:
        cur.execute('''INSERT OR IGNORE INTO messages (telegram_id, created_at, message)
        VALUES(?, ?, ?);''', user_message)
    await asyncio.sleep(0.3)


async def list_of_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=LIST_OF_MESSAGES)
    with conn:
        cur.execute('''SELECT message FROM messages WHERE telegram_id = ?;''', (update.effective_user.id,))пше
    await context.bot.send_message(chat_id=update.effective_chat.id, text=cur.fetchall()[0][0])
    await asyncio.sleep(0.3)


async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    help_handler = CommandHandler('help', help)
    application.add_handler(help_handler)

    remember_handler = CommandHandler('remember', remember)
    application.add_handler(remember_handler)

    remember_process_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), remember_process)
    application.add_handler(remember_process_handler)

    list_of_messages_handler = CommandHandler('list_of_messages', list_of_messages)
    application.add_handler(list_of_messages_handler)

    unknown_command_handler = MessageHandler(filters.COMMAND, unknown_command)
    application.add_handler(unknown_command_handler)

    application.run_polling()
