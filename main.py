import toml

from searcher import searcher

parsed_toml = toml.load('config.toml')

for s in parsed_toml['searches']:
    url = s['keywords']

    for item in searcher.search(url):
        print('{}, {}'.format(item.productName, item.productURL))