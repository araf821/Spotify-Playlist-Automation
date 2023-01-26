# This is a project where I'll be web scraping the billboard top 100 songs
# and turning it into a spotify playlist. The top 100 songs selected will
# be from the day the user's birthday is, which we will take in as an input.

from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

YEAR = 0

def get_date():
    year = int(input("What year were you born in? (yyyy): "))
    while year < 1900 or year > 2022:
        print("Please enter a year between 1900 and 2022.")
        year = int(input("What year were you born in? (yyyy): "))
    month = int(input("What month were you born in? (mm): "))
    while month < 1 or month > 12:
        print("Please enter a valid month, between 01 and 12.")
        month = int(input("What month were you born in? (mm): "))
    day = int(input("What day were you born in? (dd): "))
    while day < 1 or day > 31:
        print("Please enter a valid day, between 01 and 31.")
        day = int(input("What day were you born in? (dd): "))

    global YEAR
    YEAR = year

    # Let's format the date so that it is accepted in the URL.
    if day < 10 and month < 10:
        date = f"{year}-0{month}-0{day}"
    elif day < 10:
        date = f"{year}-{month}-0{day}"
    elif month < 10:
        date = f"{year}-0{month}-{day}"

    return date


def create_playlist(user_id="", playlist_name="Undefined", description=""):
    sp.user_playlist_create(
        user=user_id, name=f"{playlist_name}", public=False, description=f"{description}")


def retrieve_track_uris():
    # Save the uri of every track to a list, we'll add them to a playlist later in the code
    track_uris = []
    tracks_not_found = []

    print("Please wait a few seconds while we add all the tracks to your new playlist!")

    # Loop through each title in the 'songs' list
    for song in songs:
        # search for the song:
        search_result = sp.search(q=f"track:{song}", limit=1, type="track")
        try:
            song_uri = search_result["tracks"]["items"][0]["uri"]
            track_uris.append(song_uri)
        except:
            tracks_not_found.append(song)

    print(f"Songs found for the year {YEAR}: {len(track_uris)} out of 100.")
    if len(tracks_not_found) > 0:
        print("\nHere are the songs we couldn't find:")
        for song in tracks_not_found:
            print(song)
    
    return track_uris


def get_playlist_id():
    # Retrieving the ID of the last playlist created
    result = sp.current_user_playlists(limit=1)
    playlist_uri = result["items"][0]["uri"]
    playlist_id = playlist_uri.split(":")[2]

    return playlist_id

URL = "https://www.billboard.com/charts/hot-100/"

# ---------------------------- START -----------------------------

print("Welcome! Let's get your birthday and we'll create you a Spotify playlist\nconsisting of the top 100 songs on the day you were born.")

# --------------------------- GET DATE --------------------
date = get_date()

# ------------------------ GET LIST OF SONGS ----------------------
response = requests.get(url=f"{URL}{date}")
html = response.text

# The line below gives us the entire website's html
soup = BeautifulSoup(html, "html.parser")
tags = soup.select(".o-chart-results-list__item #title-of-a-story")
# The tags variable now contains every h3 tag that stores the title of the song

# Let's break it down and get just the title and add it to a list
list = [tag.text for tag in tags]
songs = []
# The way they formatted this website, the title consists of many \t and \n,
# so, we need to break it down even further to get the actual title.
for text in list:
    x = text.split()
    songs.append(' '.join(x))
# Now, we've got the complete list of 100 songs.

# ------------------------ AUTHORIZE THE USER -----------------------

load_dotenv()
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

user_id = "227mp6rbrjo5sdym35eyem2ha"
scopes = ["playlist-read-private", "playlist-modify-private", "playlist-modify-public"]

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope=scopes,
    redirect_uri="https://example.com",
    client_id=client_id,
    client_secret=client_secret,
    show_dialog=True,
    cache_path="token.txt"))

# ----------------------- CREATE NEW PLAYLIST ------------------------

print("Let's create you a new playlist! What would you like to call it?")
playlist_name = input("")
description = input("Playlist Description (Optional) :\n")

create_playlist(user_id, playlist_name, description)

# ------------------------- GET TRACK URIs -------------------------

tracks = retrieve_track_uris()

# --------------------- ADD TRACKS TO PLAYLIST ----------------

playlist_id = get_playlist_id()

# Let's add the track uris to this playlist:
sp.playlist_add_items(playlist_id=playlist_id, items=tracks)

print("\n AND we're done! Enjoy your new playlist!")