import streamlit as st
import back

nb_artists = len(back.artists)
nb_songs = len(back.songs)
oldest_song_year = back.songs['release_date'].min().year
newest_song_year = back.songs['release_date'].max().year

st.title("French Rap Lyrics Explorator")
st.header("Insights on French Rap with Data")
'''
 * '''+str(nb_artists)+''' artists
 * '''+str(nb_songs)+''' songs from '''+str(oldest_song_year)+''' to '''+str(newest_song_year)
