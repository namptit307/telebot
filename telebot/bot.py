import logging
import importlib
import os
import pkgutil
import sys
import traceback

from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater

import telebot.plugins
from telebot import emojies
from telebot import settings

LOG = logging.getLogger(__name__)


def strip_extension(lst):
    return (os.path.splitext(l)[0] for l in lst)


class Bot(object):
    def __init__(self, token):
        self.scheduler = None
        self.updater = Updater(token=token)
        self.dispatcher = self.updater.dispatcher
        self.plugins = {}
        self.plugin_modules = []
        self.init_handlers()

    def init_handlers(self):
        """Init all command handlers"""
        # Init general command handlers
        start_handler = CommandHandler('start', self.start)
        self.dispatcher.add_handler(start_handler)
        # Listen notification
        file_handler = MessageHandler(filters='@namnh307',
                                      callback=self.notification_to_user)
        self.dispatcher.add_handler(file_handler)
        self.dispatcher.add_error_handler(self.error)

    def error(self, bot, update, error):
        """Log Errors caused by Updates."""
        LOG.warning('Update "%s" caused error "%s"', update, error)

    def notification_to_user(self, bot, update):
        pass

    def _get_commands(self):
        commands = []
        for name, helper in self.plugins.items():
            command = '/' + name
            whatis = helper['whatis']
            commands.append([command, whatis])
        return commands

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

