import json
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
import os
import boto3 
from datetime import datetime 
from io import StringIO

def lambda_handler(event, context):
    # Use a with statement to ensure cleanup of Spotify session
    SPOTIPY_CLIENT_ID = os.environ.get('SPOTIPY_CLIENT_ID')
    SPOTIPY_CLIENT_SECRET = os.environ.get('SPOTIPY_CLIENT_SECRET')

    class SpotifySession:
        def __enter__(self):
            auth_manager = SpotifyClientCredentials(
                client_id=SPOTIPY_CLIENT_ID,
                client_secret=SPOTIPY_CLIENT_SECRET
            )
            self.sp = Spotify(auth_manager=auth_manager)
            return self.sp

        def __exit__(self, exc_type, exc_val, exc_tb):
            # Cleanup when the 'with' block finishes execution
            pass

    # Playlist link to process
    playlist_link = "https://open.spotify.com/playlist/37i9dQZEVXbKqiTGXuCOsB"
    playlist_URI = playlist_link.split("/")[-1]

    with SpotifySession() as sp:
        # Store link
        data = sp.playlist_tracks(playlist_URI)

    client = boto3.client('s3')
    filename = "Spotify_raw_" + str(datetime.now()) + ".json"
    client.put_object(
        Bucket = "spotify-etl-pipeline-cm",
        Key = "raw_data/bronze/" + filename,
        Body= json.dumps(data)
        )
