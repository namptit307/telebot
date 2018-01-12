import logging
import os

from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater

LOG = logging.getLogger(__name__)


def strip_extension(lst):
    return (os.path.splitext(l)[0] for l in lst)


class Bot(object):
    def __init__(self, token):
        self.scheduler = None
        self.updater = Updater(token=token)
        self.dispatcher = self.updater.dispatcher
        self.plugin_modules = []
        self.init_handlers()

    def init_handlers(self):
        """Init all command handlers"""
        # Init general command handlers
        start_handler = CommandHandler('start', self.start)
        self.dispatcher.add_handler(start_handler)
        # Listen notification
        file_handler = MessageHandler(filters=Filters.chat(
            username='namptit307'), callback=self.notification_to_user)
        self.dispatcher.add_handler(file_handler)
        self.dispatcher.add_error_handler(self.error)

    def error(self, bot, update, error):
        """Log Errors caused by Updates."""
        LOG.warning('Update "%s" caused error "%s"', update, error)

    def notification_to_user(self, bot, update):
        LOG.warning(update.message)
        # bot.send_message(chat_id="<id_sender>", text=update.message)

    def run(self):
        self.updater.start_polling(clean=True)
        return

    def start(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id,
                         text='Hanno! I\'m Telebot for notification')

    def stop(self):
        self.updater.stop()
        return

    def idle(self):
        self.updater.idle()
        return

