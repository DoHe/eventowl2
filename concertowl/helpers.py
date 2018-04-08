import requests

WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php?origin=*&format=json&formatversion=2&action=opensearch&search="


def get_wikipedia_description(name):
    _, titles, descriptions, urls = requests.get(WIKIPEDIA_API_URL + name).json()
    for title, description, url in zip(titles, descriptions, urls):
        if title.endswith('(band)'):
            return description, url
    return descriptions[0], urls[0]


print(get_wikipedia_description('slipknot'))
