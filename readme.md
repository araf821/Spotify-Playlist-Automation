# Spotify Playlist Automation

### Description

A test-based application that takes in the user's birth date and creates them a new Spotify playlist out of the top 100 most popular songs on the day of their birth.

#### Created using:
- Python
- BeautifulSoup (module)
- Spotipy API (library made for the Spotify API)
- Requests (module)

***

#### Step by step process of how it works:

1. Takes in the user's birth date as input.
2. Using the BeautifulSoup module, it scrapes the list of the top 100 songs on Billboard charts for the date given by the user.
3. The information scraped from Billboard then is broken down into a list containing of the 100 tracks' titles.
4. A new private playlist is created taking inputs from the user for the name and description of the playlist.
5. Using the Spotipy API, the application searches on Spotify for every track in the list created earlier in the program.
6. The first track in the search results is added to the playlist.
7. Any title not found on Spotify is then added to another list and displayed to the user. The user is also made aware of how many tracks were found and how many were not.