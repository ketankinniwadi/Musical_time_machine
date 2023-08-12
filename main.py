import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from secret import CLIENT_SECRET_SPOTIFY, CLIENT_ID_SPOTIFY, URL_REDIRECT
date = input("What year you would like to travel to? Please enter in YYYY-MM-DD format ")
response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}")
response.raise_for_status()
content = response.text

soup = BeautifulSoup(content, "html.parser")
title_tags = soup.findAll("h3", id="title-of-a-story", class_="u-letter-spacing-0021")
titles = [each.getText().strip() for each in title_tags if each.getText().strip() not in ['Songwriter(s):',
                                                                                          'Producer(s):',
                                                                                          'Imprint/Promotion Label:']]

print(titles)


sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=URL_REDIRECT,
        client_id=CLIENT_ID_SPOTIFY,
        client_secret=CLIENT_SECRET_SPOTIFY,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
song_uris = []
year = date.split("-")[0]
for song in titles:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
# print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)