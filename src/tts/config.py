import copy
import logging
import os

import yaml

from tts.contrib.cleaning import (
    DictionaryCleaner,
    clean_uppercase,
    keep_alpha,
)
from tts.messages.cleaning import MessageCleaner


logger = logging.getLogger(__name__)

ALPHA_ONLY = 'alphaOnly'
DICTIONARY = 'dictionary'
HOST = 'host'
LOWER_CASE = 'lowerCase'
MESSAGES = 'messages'
REPLIES = 'replies'
PORT = 'port'
SERVER = 'server'
SMS_MAX_LENGTH = 160

class Configuration:
    def __init__(self, path=None):
        self._alpha_only = False
        self._dictionary = None
        self._lower_case = False
        self._host = None
        self._port = None
        self._replies = []

        self._try_update_from_home_dir_yaml()
        if path is not None:
            self._try_update_from_yaml(path)

    def _try_add_reply(self, reply):
        if len(reply) <= SMS_MAX_LENGTH:
            self._replies.append(reply)
        else:
            logger.warning('Reply %r too long at %d (max is %d)', reply,
                           len(reply), SMS_MAX_LENGTH)

    def _try_update_from_home_dir_yaml(self):
        path = os.path.expanduser(os.path.join('~', '.tts.yaml'))
        self._try_update_from_yaml(path)

    def _try_update_from_yaml(self, path):
        if os.path.isfile(path):
            with open(path) as config_file:
                update = yaml.load(config_file)
            self._update_config(update)

    def _update_config(self, update):
        if MESSAGES in update:
            messages = update[MESSAGES]
            self._alpha_only = messages.get(ALPHA_ONLY, self._alpha_only)
            self._dictionary = messages.get(DICTIONARY, self._dictionary)
            self._lower_case = messages.get(LOWER_CASE, self._lower_case)
        if SERVER in update:
            server = update[SERVER]
            self._host = server.get(HOST, self._host)
            self._port = server.get(PORT, self._port)
        for reply in update.get(REPLIES, []):
            self._try_add_reply(reply)

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    def get_replies(self):
        return copy.copy(self._replies)

    def get_message_cleaner(self):
        cleaners = []
        if self._alpha_only:
            cleaners.append(keep_alpha)
        if self._lower_case:
            cleaners.append(clean_uppercase)
        if self._dictionary is not None:
            with open(self._dictionary) as file_:
                dictionary = frozenset(line[:-1] for line in file_)
            cleaners.append(DictionaryCleaner(dictionary))
        return MessageCleaner(cleaners)

