## Read Apple Music Library data
## Note: the data should be an .xml file, located in the same directory as this file.

import xml.etree.ElementTree as ET

# Edit this value if the library data isn't saved with the default name
LIBRARY_FILE_NAME = 'Library.xml'

tree = ET.parse(LIBRARY_FILE_NAME)
root = tree.getroot()

tracks = []

for d in root.iter('dict'):
    track = {}

    name = False
    artist = False
    for child in d:
        if child.tag == 'key':
            if child.text == 'Name':
                name = True
                continue 
            elif child.text == 'Artist':
                artist = True 
                continue    
       
        if name:
            track['name'] = child.text
            name = False
        elif artist:
            track['artist'] = child.text
            artist = False

    if track != dict():
        # If track doesn't have a name, skip. We don't listen to headless tunes here
        if 'name' not in track:
            continue    

        # If track doesn't have an artist, keep it empty. God always rolls the dice, baby.
        if 'artist' not in track:
            track['artist'] = ' '

        tracks.append(track)


## Loop through tracks, search for each one & add the first search result to the current user's library

import os

import spotipy
import spotipy.util as util

# Adding all the tracks will probably take some time
from tqdm import tqdm

# Probably nobody enjoys reading raw text output
from pprint import pprint

# Get client_id  & client_secret from environment variables
CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')

if any(v is None for v in [CLIENT_ID, CLIENT_SECRET]):
    print('Could not find required environment variables. Aborting.')
    quit()

if CLIENT_SECRET is
token = util.prompt_for_user_token(username='spleen', scope='user-library-modify', client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri='http://localhost/')

sp = spotipy.Spotify(auth=token)

track_uris = []
untrack_uris = []
for track in tqdm(tracks):
    # Search for track & retrieve ID
    res = sp.search("{} {}".format(track['name'], track['artist']), limit=1)

    if len(res['tracks']['items']) > 0:
        uri = res['tracks']['items'][0]['uri']
    else:
        untrack_uris.append(track)

    # Add uri to list of track uris to add to the current user's library
    track_uris.append(uri)

# Add track to current user's library, in groups of 50
while track_uris != []:
    sp.current_user_saved_tracks_add(track_uris[:50])
    del track_uris[:50]

# Spit out tracks that weren't found
print("Couldn't find {} tracks. Will dump 'em here.".format(len(untrack_uris)))
pprint(untrack_uris)
