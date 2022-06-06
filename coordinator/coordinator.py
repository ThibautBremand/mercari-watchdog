import time
from typing import List

import cache.cache
from config import config
from scraper import searcher


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


def start(searches: List[config.Search], delay: int):
    while True:
        scraped = {}
        for s in searches:
            kw = s['keywords']
            items = searcher.search(kw)
            scraped[kw] = items

            time.sleep(2)

        to_persist = build_cache(scraped)

        with open('scraped.txt', 'w') as f:
            print(to_persist, file=f)

        time.sleep(delay)
