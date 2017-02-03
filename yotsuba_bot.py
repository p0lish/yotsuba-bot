#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.

import logging
from getlatestpostfromthread import get_newest_in_thread
from telegram.ext import Updater, CommandHandler


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def get_newest_thread(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="please wait...")
    thread = str.replace(update.message.text, "/", "", 1)
    result = get_newest_in_thread(thread, 10)
    bot.sendPhoto(chat_id=update.message.chat_id, photo=result['thumbnail'])
    bot.sendMessage(chat_id=update.message.chat_id, text=result['description'])
    bot.sendMessage(chat_id=update.message.chat_id, text=result['link'])


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("TOKEN")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("b", get_newest_thread))
    dp.add_handler(CommandHandler("wg", get_newest_thread))
    dp.add_handler(CommandHandler("pol", get_newest_thread))
    dp.add_handler(CommandHandler("x", get_newest_thread))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
