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

    items, _ = mercari.fetch(mercari.searchURL, data)
    return items
