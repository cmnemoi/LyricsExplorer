from lyricsgenius import Genius
from decouple import config
import pandas as pd

def downloadLyrics(artist_names, max_songs=None):
    artist_objects = [api.search_artist(name, max_songs=max_songs) for name in artist_names]
    for artist in artist_objects:
        artist.save_lyrics()


GENIUS_CLIENT_ACCESS_TOKEN = config('GENIUS_CLIENT_ACCESS_TOKEN')
api = Genius(GENIUS_CLIENT_ACCESS_TOKEN)
api.retries=1000
api.timeout=60
api.remove_section_headers=True

artists = pd.read_csv('../data/artists.csv')['artists'].values.tolist()

downloadLyrics(artists)