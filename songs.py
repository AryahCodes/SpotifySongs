import spotipy
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from youtube_search import YoutubeSearch
import threading
import time
from queue import Queue


#We need this to get info from the account.
client_Id = '1920c832be0b4515b89bc7cf77e605d3'
client_screte = '2df906b28bd44f6f9312540c38eb7dab'

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

results_q = Queue()
def youtube_url(song_name, artist_name):
    style = song_name + " - " + artist_name
    #to_dict because we need infividual elements.
    results = YoutubeSearch(style, max_results=1).to_dict()
    video_id = results[0]['url_suffix']
    url = f"https://www.youtube.com{video_id}"
    results_q.put(f"{song_name} by {artist_name} -> {url}")

threads = []
for items in tracks['items']:
    track = items['track']
    name = track['name']    
    artist = track['artists'][0]['name']
    #the url for the link
    t1 = threading.Thread(target=youtube_url,args=(name, artist))
    threads.append(t1)
    t1.start()

for thr in threads:
    thr.join()

while not results_q.empty():
    print(results_q.get())