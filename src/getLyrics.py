from lyricsgenius import Genius
from decouple import config

GENIUS_CLIENT_ACCESS_TOKEN = config('GENIUS_CLIENT_ACCESS_TOKEN')
print(GENIUS_CLIENT_ACCESS_TOKEN)
