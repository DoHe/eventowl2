import os

import requests
from django_q.tasks import async as async_q
from spotipy import Spotify

GENERATED_PLAYLISTS = ['spotify', 'spotifydiscover']

SPOTIFY_ID = os.getenv('SPOTIFY_ID')
SPOTIFY_SECRET = os.getenv('SPOTIFY_SECRET')
SPOTIFY_URL = os.getenv('SPOTIFY_URL')


def spotify_token_from_code(code):
    url = 'https://accounts.spotify.com/api/token'
    response = requests.post(url, data={'code': code,
                                        'grant_type': 'authorization_code',
                                        'redirect_uri': SPOTIFY_URL,
                                        'client_id': SPOTIFY_ID,
                                        'client_secret': SPOTIFY_SECRET})
    token_info = response.json()
    return token_info


def spotify_artists(token):
    spotify_client = Spotify(auth=token)
    async_q(playlist_artists, spotify_client, hook='concertowl.apis.spotify._got_artists')
    async_q(saved_artists, spotify_client, hook='concertowl.apis.spotify._got_artists')
    async_q(followed_artists, spotify_client, hook='concertowl.apis.spotify._got_artists')


def _got_artists(task):
    print("============", task.func)
    print(task.result)
    print(task.func, "===========")


def playlist_artists(client):
    print("Reading artists from playlists...")
    playlists = _all_playlists(client)
    result = set()
    for playlist in playlists:
        owner = playlist['owner']['id']
        if owner not in GENERATED_PLAYLISTS:
            playlist_content = client.user_playlist(owner, playlist['id'], fields="tracks,next")
            result |= set(_artists_from_playlist(playlist_content, client))
    return result


def saved_artists(client):
    print("Reading artists from saved tracks...")
    tracks = client.current_user_saved_tracks()
    result = set(_artists_from_tracks(tracks))
    while tracks['next']:
        tracks = client.next(tracks)
        result |= set(_artists_from_tracks(tracks))
    return result


def followed_artists(client):
    print("Reading followed artists...")
    artists = client.current_user_followed_artists()['artists']
    result = {artist['name'] for artist in artists['items']}
    while artists['next']:
        artists = client.next(artists)['artists']
        result |= {artist['name'] for artist in artists['items']}
    return result


def _all_playlists(client):
    playlists = client.user_playlists(client.current_user()["id"])
    yield from playlists['items']
    while playlists['next']:
        playlists = client.next(playlists)
        yield from playlists['items']


def _artists_from_playlist(playlist_content, client):
    tracks = playlist_content['tracks']
    yield from _artists_from_tracks(tracks)
    while tracks['next']:
        tracks = client.next(tracks)
        yield from _artists_from_tracks(tracks)


def _artists_from_tracks(tracks):
    for track_item in tracks['items']:
        for artist in track_item['track']['artists']:
            yield artist['name']


def add_spotify_artists(code, user):
    token = spotify_token_from_code(code)['access_token']
    spotify_artists(token)
