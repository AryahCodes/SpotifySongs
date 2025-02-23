import spotipy
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from youtube_search import YoutubeSearch
import threading
import os
import yt_dlp


current_directory = os.getcwd()
folders_Idrectory = {"songs":os.path.join(current_directory, "songs")}
os.makedirs(folders_Idrectory["songs"], exist_ok=True) #We use makedirs because this won't count for intermediate directories.

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

def download(url, song, artist):
    try:
        print(f"Starting download for {song} by {artist}...")
        ydl_opts = {
            'format': 'bestaudio/best',  # Best audio quality
            'outtmpl': f"{folders_Idrectory['songs']}/{song} - {artist}.%(ext)s",  # Output filename pattern
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',  # Extract audio
                'preferredcodec': 'mp3',
                'preferredquality': '192',  # MP3 quality
            }],
            'embedthumbnail': True,  # Embed album art
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)

        # Get the downloaded file name
        filename = ydl.prepare_filename(info_dict)
        print(f"Downloaded: {filename}")        
    except Exception as e:
        print(f"Unexpected error: {e}")


def youtube_url(song_name, artist_name):
    style = song_name + " - " + artist_name
    #to_dict because we need infividual elements.
    results = YoutubeSearch(style, max_results=1).to_dict()
    video_id = results[0]['url_suffix']
    url = f"https://www.youtube.com{video_id}"
    download(url, song_name, artist_name)

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