import spotipy
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

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

for items in tracks['items']:
    track = items['track']
    name = track['name']    
    print(name)