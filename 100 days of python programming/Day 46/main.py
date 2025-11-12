import logging
import os

import requests
import spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth

try:

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
    # Build top 100 songs list from Billboard
    url = "https://billboard.com/charts/hot-100/"
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    h3_element_list = soup.select('li.o-chart-results-list__item h3')
    top100_songs_list = [element.get_text().strip() for element in h3_element_list]

    # Build Spotify API client
    auth_manager = SpotifyOAuth(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
        redirect_uri="https://open.spotify.com/",  # must match with the redirect URI set in Spotify developer account
        scope="playlist-modify-public, playlist-modify-private",
        show_dialog=True,
        username="Sudheer")
    sp = spotipy.Spotify(auth_manager=auth_manager)
    user_id = sp.current_user()["id"]

    # Search for songs and build the playlist

    playlist_tracks = []
    for title in top100_songs_list:
        results = sp.search(q=f"track:{title}", type="track", limit=1)
        tracks = results["tracks"]["items"]
        if tracks:
            playlist_tracks = playlist_tracks + [track["external_urls"]["spotify"] for track in tracks]
    print(playlist_tracks)

    playlist_id = None
    playlist_name = "Sudheer's Top 100 songs"
    results = sp.current_user_playlists()
    for playlist in results["items"]:
        if playlist["name"] == playlist_name:
            playlist_id = playlist["id"]
            logging.info(f"Playlist exists already: {playlist_id}")
            break
    if not playlist_id:
        playlist_id = sp.user_playlist_create(
            user=user_id,
            name=playlist_name,
            public=False,
            description="Billboard Top 100"
        )["id"]
        logging.info(f"Playlist created successfully: {playlist_id}")

    print(sp.auth_manager.get_access_token(as_dict=True))
    playlist = sp.playlist(playlist_id)
    print(playlist['owner']['id'], sp.current_user()['id'])

    sp.playlist_add_items(playlist_id=playlist_id, items=playlist_tracks, position=None)
    print(f"Playlist created successfully: https://open.spotify.com/playlist/{playlist_id}")
except requests.exceptions.HTTPError as e:
    print(e)
except requests.exceptions.RequestException as e:
    print(e)
except Exception as e:
    print(e)
