import json
import time
from typing import List

import cache.cache
from config import config
from scraper import searcher


def start(searches: List[config.Search], delay: int):
    while True:
        data = read_cache()

        scraped = {}
        for s in searches:
            kw = s['keywords']
            items = handle_search(kw)
            scraped[kw] = items
            time.sleep(2)

        write_cache(scraped)

        time.sleep(delay)


def handle_search(kw):
    print(f'Handling keywords {kw}...')

    items = searcher.search(kw)
    print(f'Found {len(items)} new items for keywords {kw}')

    return items


def build_cache(scraped):
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

        last_ids = cache.cache.last_ids_separator.join(ids)

        res[kw] = last_ids

    return res


def read_cache():
    try:
        res = json.load(open('scraped.txt'))
    except:
        print('could not read cache')
        return {}

    return res


def write_cache(scraped):
    print('Writing cache...')
    to_persist = build_cache(scraped)
    # with open('scraped.txt', 'w') as f:
    #     print(to_persist, file=f)
    json.dump(to_persist, open('scraped.txt', 'w'))

    print('Cache written!')
