#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import logging
from getlatestpostfromthread import get_all_posts_from_thread
from telegram import InlineQueryResultPhoto, InlineQueryResultGif, InlineQueryResultVideo
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
from uuid import uuid4


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
help_content = '''content'''

enabled_threads = ["a", "b", "c", "d", "e", "f", "g", "gif", "h", "hr", "k" "wg", "x"]


def start(bot, update):
    update.message.reply_text('Hi!')


def help(bot, update):
    update.message.reply_text(help_content)


def inline_query(bot, update):
    query = update.inline_query.query
    results = list()
    if query in enabled_threads:
        posts = get_all_posts_from_thread(query, 1)
        print(posts)
        for post in posts:
            if post["image"].endswith('.jpg'):
                results.append(
                    InlineQueryResultPhoto(
                        id=uuid4(),
                        thumb_url=post["thumbnail"],
                        photo_url=post["image"],
                        caption=post["link"]
                    )
                )
            if post["image"].endswith('.gif'):
                results.append(
                    InlineQueryResultGif(
                        id=uuid4(),
                        thumb_url=post["thumbnail"],
                        gif_url=post["image"],
                        caption=post["link"]
                    )
                )
            if post["image"].endswith('.webm'):
                results.append(
                    InlineQueryResultVideo(
                        id=uuid4(),
                        thumb_url=post["thumbnail"],
                        video_url=post["image"],
                        caption=post["link"],
                        title=post["description"],
                        mime_type="video/mp4"
                    )
                )
    update.inline_query.answer(results)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("300418672:AAF9FrOCEqXzD1lBBgYDaBuETzLVXsJujRU")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(InlineQueryHandler(inline_query))

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
