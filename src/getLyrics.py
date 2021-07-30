import lyricsgenius as genius
from decouple import config
import pandas as pd
import json


client_access_token = config('GENIUS_CLIENT_ACCESS_TOKEN')
# artists = pd.read_csv('../data/artists.csv')['artists'].values.tolist()

api = genius.Genius(client_access_token)
api.remove_section_headers=True
api.retries=1000
api.timeout=60
api.excluded_terms = ["(Remix)", "(Live)"]

def getLyrics(artists,max_songs=2):
    for artist in artists:
        a = api.search_artist(artist,max_songs)
        a.save_lyrics('test_'+artist,overwrite=True)

def getSongs(artists):
    songs = {}
    for artist in artists:
        songs[artist] = json.load(open('test_'+artist+'.json'))['songs']
    return songs

def formatSongs(raw_songs,artists):
    songs = pd.DataFrame()
    for artist in artists:
        for song in raw_songs[artist]:
            songs=songs.append(pd.DataFrame.from_dict(song, orient="index").transpose())
    songs.drop(['annotation_count', 'api_path', 'full_title',
       'header_image_thumbnail_url', 'header_image_url', 'id',
       'lyrics_owner_id', 'lyrics_state', 'path', 'pyongs_count',
       'song_art_image_thumbnail_url', 'song_art_image_url', 'stats',
       'title_with_featured', 'url', 'song_art_primary_color',
       'song_art_secondary_color', 'song_art_text_color', 'primary_artist',
       'apple_music_id', 'apple_music_player_url', 'description',
       'embed_content', 'featured_video', 'lyrics_placeholder_reason',
       'recording_location', 'release_date', 'release_date_for_display',
       'current_user_metadata', 'album', 'custom_performances',
       'description_annotation', 'featured_artists',
       'lyrics_marked_complete_by', 'media', 'producer_artists',
       'song_relationships', 'verified_annotations_by',
       'verified_contributors', 'verified_lyrics_by', 'writer_artists'],axis=1,inplace=True)
    songs.reset_index(inplace=True,drop=True)
    return songs


artists = ['MRC','Vald']
getLyrics(artists)
raw_songs = getSongs(artists)
songs = formatSongs(raw_songs,artists)
print(songs)