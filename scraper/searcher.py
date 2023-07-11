import logging
import uuid

import mercari.mercari.mercari as mercari


# returns an generator for Item objects
def search(
    keywords,
    sort=mercari.MercariSort.SORT_CREATED_TIME,
    order=mercari.MercariOrder.ORDER_DESC,
    status=mercari.MercariSearchStatus.ON_SALE,
    exclude_keywords=""
):

    # This is per page and not for the final result
    limit = 120

    data = {
        # this seems to be random, but we'll add a prefix for mercari to track if they wanted to
        "userId": "MERCARI_BOT_{}".format(uuid.uuid4()),
        "pageSize": limit,
        "pageToken": mercari.pageToPageToken(0),
        # same thing as userId, courtesy of a prefix for mercari
        "searchSessionId": "MERCARI_BOT_{}".format(uuid.uuid4()),
        # this is hardcoded in their frontend currently, so leaving it
        "indexRouting": "INDEX_ROUTING_UNSPECIFIED",
        "searchCondition": {
            "keyword": keywords,
            "sort": sort,
            "order": order,
            "status": [status],
            "excludeKeyword": exclude_keywords,
        },
        # I'm not certain what these are, but I believe it's what mercari queries against
        # this is the default in their site, so leaving it as these 2
        "defaultDatasets": [
            "DATASET_TYPE_MERCARI",
            "DATASET_TYPE_BEYOND"
        ]
    }

    items = []
    try:
        items = mercari.fetch(mercari.searchURL, data)
        return items[0]
    except Exception as e:
        logging.error(f'error while fetching mercari: {e.__class__}')

    return items
