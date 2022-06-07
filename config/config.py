import os
import sys

import toml
from dotenv import load_dotenv
from typing import List


class Search:
    keywords: str


class Config:
    telegram_chat_id: str
    telegram_token: str
    searches: List[Search]
    delay: int
    msg_tpl: str
    change_rate: float
    download_photos: bool

    def __init__(self, telegram_chat_id, telegram_token, searches, delay, msg_tpl, change_rate, download_photos):
        self.telegram_chat_id = telegram_chat_id
        self.telegram_token = telegram_token
        self.searches = searches
        self.delay = delay
        self.msg_tpl = msg_tpl
        self.change_rate = change_rate
        self.download_photos = download_photos


def load():
    load_dotenv()
    parsed_toml = toml.load('config.toml')

    check_env_var('TELEGRAM_CHAT_ID')
    check_env_var('TELEGRAM_TOKEN')
    check_toml_var('searches', parsed_toml)
    check_toml_var('delay', parsed_toml)
    check_toml_var('message', parsed_toml)

    telegram_chat_id = os.environ['TELEGRAM_CHAT_ID']
    telegram_token = os.environ['TELEGRAM_TOKEN']
    searches = parsed_toml['searches']
    delay = parsed_toml['delay']
    msg_tpl = parsed_toml['message']

    change_rate = 0.0
    if 'changerate' in parsed_toml:
        change_rate = parsed_toml['changerate']

    download_photos = False
    if 'downloadphotos' in parsed_toml:
        download_photos = parsed_toml['downloadphotos']

    return Config(
        telegram_chat_id=telegram_chat_id,
        telegram_token=telegram_token,
        searches=searches,
        delay=delay,
        msg_tpl=msg_tpl,
        change_rate=change_rate,
        download_photos=download_photos
    )


def check_toml_var(val, toml_val):
    if val not in toml_val:
        print(f'{val} not found in toml')
        sys.exit()


def check_env_var(val):
    if val not in os.environ:
        print(f'{val} env var not found')
        sys.exit()
