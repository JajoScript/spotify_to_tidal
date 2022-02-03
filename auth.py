#!/usr/bin/env python3

import sys
import spotipy
import tidalapi
import os
from dotenv import load_dotenv
import webbrowser
import yaml

# Variables de entorno.
config = load_dotenv(".env");
my_session_id:str = os.environ['SESSION_ID'];
my_token_type:str = os.environ['TOKEN_TYPE'];
my_access_token:str = os.environ['ACCESS_TOKEN'];
my_refresh_token:str = os.environ['REFRESH_TOKEN'];
my_playlist_uri:str = os.environ['PLAYLIST_URI'];

def open_spotify_session(config):
    credentials_manager = spotipy.SpotifyOAuth(username=config['username'],
				       scope='playlist-read-private',
				       client_id=config['client_id'],
				       client_secret=config['client_secret'],
				       redirect_uri=config['redirect_uri'])
    try:
        credentials_manager.get_access_token(as_dict=False)
    except spotipy.SpotifyOauthError:
        sys.exit("Error opening Spotify sesion; could not get token for username: ".format(config['username']))

    return spotipy.Spotify(oauth_manager=credentials_manager)

def open_tidal_session():
    try:
        with open('.session.yml', 'r') as session_file:
            previous_session = yaml.safe_load(session_file)
    except OSError:
        previous_session = None

    session = tidalapi.Session()
    session.load_oauth_session(session_id=my_session_id, token_type=my_token_type, access_token=my_access_token, refresh_token=my_refresh_token);

    with open('.session.yml', 'w') as f:
        yaml.dump( {'session_id': session.session_id,
                   'token_type': session.token_type,
                   'access_token': session.access_token,
                   'refresh_token': session.refresh_token}, f )
    return session


