import json
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
import os
import boto3 
from datetime import datetime 
from io import StringIO
import pandas as pd

def album(data):
    album_list = []
    for row in data['items']:
        album_id = row['track']['album']['id']
        album_name = row['track']['album']['name']
        album_release_date = row['track']['album']['release_date']
        album_URL = row['track']['album']['external_urls']['spotify']
        album_elements = {
            'album_id': album_id,
            'album_name': album_name,
            'album_release_date': album_release_date,
            'album_URL': album_URL
        }
        album_list.append(album_elements)
    return album_list

def artist(data):
    artist_list = []
    for row in data['items']:
        if 'track' in row:  # Ensure 'track' exists
            for artist in row['track']['artists']:
                artist_elements = {
                    'artist_id': artist['id'],
                    'artist_name': artist['name'],
                    'artist_URL': artist['external_urls']['spotify'],
                }
                artist_list.append(artist_elements)
    return artist_list

def song(data):
    song_list = []
    for row in data['items']:
        if 'track' in row:  # Ensure 'track' exists
            song_id = row['track']['id']
            song_name = row['track']['name']
            song_duration = row['track']['duration_ms']
            song_url = row['track']['external_urls']['spotify']
            song_popularity = row['track']['popularity']
            song_added = row['added_at']
            song_explicit_flag = row['track']['explicit']
            album_id = row['track']['album']['id']
            artist_id = [artist['id'] for artist in row['track']['album']['artists']]
            song_element = {
                'song_id': song_id,
                'song_name': song_name,
                'song_duration': song_duration,
                'song_url': song_url,
                'song_popularity': song_popularity,
                'song_added': song_added,
                'song_explicit_flag': song_explicit_flag,
                'album_id': album_id,
                'artist_id': artist_id
            }
            song_list.append(song_element)
    return song_list

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    Bucket = "spotify-etl-pipeline-cm"
    Key = "raw_data/bronze/"
    
    # Collect the data from S3
    spotify_data = []
    spotify_keys = []
    for file in s3.list_objects(Bucket=Bucket, Prefix=Key)['Contents']:
        filekey = file['Key']
        if filekey.split('.')[-1] == "json":
            response = s3.get_object(Bucket=Bucket, Key=filekey)
            content = response['Body']
            jsonObject = json.loads(content.read())
            spotify_data.append(jsonObject)
            spotify_keys.append(filekey)
    


    # Process the data
    for data in spotify_data:
        album_list = album(data)
        artist_list = artist(data)
        song_list = song(data)#
        
    
    # Create dataframes and drop duplicates
        album_df = pd.DataFrame.from_dict(album_list)
        album_df = album_df.drop_duplicates(subset=['album_id'])
        artist_df = pd.DataFrame.from_dict(artist_list)
        artist_df = artist_df.drop_duplicates(subset=['artist_id'])
        song_df = pd.DataFrame.from_dict(song_list)
        song_df = song_df.drop_duplicates(subset=['song_id'])
        
    # adjust datatypes
        album_df['album_release_date'] = pd.to_datetime( album_df['album_release_date'])
        song_df['song_added'] = pd.to_datetime( song_df['song_added'])
        
        
    # put csv files in respective folders
        song_key = "trasnformed_data/songs_data/song_transformed" + str(datetime.now()) + ".csv"
        song_buffer = StringIO()
        song_df.to_csv(song_buffer, index = False )
        song_content = song_buffer.getvalue()
        s3.put_object(Bucket = Bucket, Key = song_key, Body = song_content)
        
        album_key = "trasnformed_data/album_data/album_transformed" + str(datetime.now()) + ".csv"
        album_buffer = StringIO()
        album_df.to_csv(album_buffer, index = False)
        album_content = album_buffer.getvalue()
        s3.put_object(Bucket = Bucket, Key = album_key, Body = album_content)
        
        artist_key = "trasnformed_data/artist_data/artist_transformed" + str(datetime.now()) + ".csv"
        artist_buffer = StringIO()
        artist_df.to_csv(artist_buffer, index = False)
        artist_content = artist_buffer.getvalue()
        s3.put_object(Bucket = Bucket, Key = artist_key, Body = artist_content)
        
        
        
    

 
        
        


        
            
            
