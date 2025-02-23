import spotipy
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from youtube_search import YoutubeSearch
import threading
import time



#We need this to get info from the account.
client_Id = 'your own'
client_screte = 'your own'

#The API credentials
spot_credits = SpotifyClientCredentials(
    client_id = client_Id,
    client_secret = client_screte,
)

#We need to get a token.    
sp = spotipy.Spotify(auth_manager=spot_credits) 

#We need the last part of the url.
playlist_url = input("What is the url for playlist: ")
playlist_id = playlist_url.split("/")[-1].split("?")[0]

#This method gives us the songs form the playlist.
tracks = sp.playlist_tracks(playlist_id)

#Get url from youtube for each song.
def youtube_url(song_name, artist_name):
    style = song_name + " - " + artist_name
    #to_dict because we need infividual elements.
    results = YoutubeSearch(style, max_results=1).to_dict()
    video_id = results[0]['url_suffix']
    return f"https://www.youtube.com{video_id}"

for items in tracks['items']:
    track = items['track']
    name = track['name']    
    artist = track['artists'][0]['name']
    youtube = youtube_url(name, artist)  # Get YouTube URL
    print(f"{name} by {artist} -> {youtube}")
