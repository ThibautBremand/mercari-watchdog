import json
import time
from typing import List

import cache.cache
import web.telegram
from config import config
from scraper import searcher
from string import Template


def start(searches: List[config.Search], delay: int, msg_tpl: str, telegram_token: str, telegram_chat_id: str):
    while True:
        cached_data = read_cache()

        scraped = {}
        for s in searches:
            kw: str = s['keywords']

            cached_ids_str = ''
            if kw in cached_data:
                cached_ids_str = cached_data[kw]

            cached_ids = cached_ids_str.split(cache.cache.last_ids_separator)

            items = handle_search(kw, cached_ids)
            scraped[kw] = items
            time.sleep(2)

        send_to_telegram(scraped, msg_tpl, telegram_token, telegram_chat_id)

        write_cache(scraped, cached_data)

        time.sleep(delay)


def handle_search(kw: str, cached_ids: List[str]):
    print(f'Handling keywords {kw}...')
    res = []
    items = searcher.search(kw, cached_ids)

    for it in items:
        if it.id in cached_ids:
            break
        res.append(it)

    print(f'Found {len(res)} new items for keywords {kw}')

    return res


def write_cache(scraped, cached_data):
    print('Writing cache...')
    to_persist = build_cache(scraped, cached_data)
    json.dump(to_persist, open('scraped.txt', 'w'))

    print('Cache written!')


def read_cache():
    try:
        res = json.load(open('scraped.txt'))
    except:
        print('could not read cache')
        return {}

    return res


def build_cache(scraped, cached_data):
    res = {}
    for kw in scraped:
        val = scraped[kw]
        ids = []
        i = 0
        for item in val:
            ids.append(item.id)
            i += 1
            if i >= cache.cache.last_ids_size:
                break

        # In case we have found less new items than last_ids_size, we add ids from the cache
        if len(ids) < cache.cache.last_ids_size:
            if kw in cached_data:
                cached = cached_data[kw].split(cache.cache.last_ids_separator)
                for i in cached:
                    ids.append(i)
                    if len(ids) >= cache.cache.last_ids_size:
                        break

        last_ids = cache.cache.last_ids_separator.join(ids)

        res[kw] = last_ids

    return res


def send_to_telegram(scraped, msg_tpl: str, telegram_token: str, telegram_chat_id: str):
    print('Sending messages to Telegram')

    for kw in scraped:
        for it in scraped[kw]:
            d = {
                'id': it.id,
                'imageURL': it.imageURL,
                'price': it.price,
                'productName': it.productName,
                'productURL': it.productURL,
                'soldOut': it.soldOut,
                'status': it.status,
            }

            src = Template(msg_tpl)
            formatted = src.substitute(d)

            web.telegram.send_telegram_message(formatted, telegram_token, telegram_chat_id)
