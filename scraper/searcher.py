import logging

import mercari.mercari.mercari as mercari


# returns an generator for Item objects
def search(keywords, sort="created_time", order="desc"):
    data = {
        "keyword": keywords,
        "limit": 120,
        "page": 0,
        "sort": sort,
        "order": order,
    }

    items = []
    try:
        items = mercari.fetch(mercari.searchURL, data)
        return items[0]
    except Exception as e:
        logging.error(f'error while fetching mercari: {e.__class__}')

    return items
