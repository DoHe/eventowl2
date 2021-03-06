import requests
from retrying import retry

OPENSEARCH_URL = "https://en.wikipedia.org/w/api.php?origin=*&format=json&formatversion=2&action=opensearch&search="
THUMBNAIL_URL = "https://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&pithumbsize=100&formatversion=2&titles="


@retry(wait_fixed=2000, stop_max_attempt_number=10)
def get_thumbnail(title):
    response = requests.get(THUMBNAIL_URL + title).json()
    return response['query']['pages'][0].get('thumbnail', {'source': None})['source']


@retry(wait_fixed=2000, stop_max_attempt_number=10)
def get_wikipedia_description(name):
    _, titles, descriptions, urls = requests.get(OPENSEARCH_URL + name).json()
    if not titles:
        return None
    for title, description, url in zip(titles, descriptions, urls):
        if title.endswith('(band)'):
            return description, url, get_thumbnail(title)
    return descriptions[0], urls[0], get_thumbnail(titles[0])
