import os

import requests
from spotipy import Spotify

MIX_OF_THE_WEEK = 'spotifydiscover'

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
    artists = set(playlist_artists(spotify_client))
    artists.update(saved_artists(spotify_client))
    artists.update(followed_artists(spotify_client))
    return [artist.lower() for artist in artists]


def playlist_artists(client):
    print("Reading artists from playlists...")
    playlists = _all_playlists(client)
    for playlist in playlists:
        owner = playlist['owner']['id']
        if owner != MIX_OF_THE_WEEK:
            playlist_content = client.user_playlist(owner, playlist['id'], fields="tracks,next")
            yield from _artists_from_playlist(playlist_content, client)


def saved_artists(client):
    print("Reading artists from saved tracks...")
    tracks = client.current_user_saved_tracks()
    yield from _artists_from_tracks(tracks)
    while tracks['next']:
        tracks = client.next(tracks)
        yield from _artists_from_tracks(tracks)


def followed_artists(client):
    print("Reading followed artists...")
    artists = client.current_user_followed_artists()['artists']
    yield from (artist['name'] for artist in artists['items'])
    while artists['next']:
        artists = client.next(artists)['artists']
        yield from (artist['name'] for artist in artists['items'])


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
