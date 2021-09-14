import streamlit as st
import back


nb_artists = len(back.artists)
nb_songs = len(back.songs)
oldest_song_year = back.songs['release_date'].min().year
newest_song_year = back.songs['release_date'].max().year
nb_songs_over_2000_words = len([song for song in back.songs['lyrics'] if len(song.split(' ')) > 2000])


st.title("French Rap Lyrics Explorator")
st.header("Insights on French Rap with Data")
'''
 * '''+str(nb_artists)+''' artists
 * '''+str(nb_songs)+''' songs from '''+str(oldest_song_year)+''' to '''+str(newest_song_year)

st.header('Who has the biggest ?  (songs produced)')
st.subheader('Number of songs per artist :')
st.write(back.nb_songs_per_artist)

st.subheader('Number of songs per artist per year:')
st.write(back.nb_songs_per_artist_per_year)

st.subheader('Top 5 of most prolific artists ever :')
st.write(back.nb_songs_per_artist.sort_values(ascending=False,by='Number of songs').head(5))

st.subheader('... relatively to their longevity :')
st.write(back.nb_songs_per_artist_per_year.sort_values(ascending=False).head(5))

st.subheader('Most of artists released less than 200 songs')
st.plotly_chart(back.fig1)
st.subheader('... or 20 songs per year')
st.plotly_chart(back.fig2)

st.subheader("Recent artists release more songs than old-school ones")
st.write("(Try to find Jul...)")
st.plotly_chart(back.fig3)

st.header('"Suis-je le seul érudit du carré VIP ?" (Vald - Primitif)')
st.write("Does Vald is as erudite as he claims ? Let's find out.")

st.subheader("Number of words used per song :")
st.plotly_chart(back.fig4)
st.write("Only "+str(nb_songs_over_2000_words)
+" songs contains more than 2000 words ("+r'${:0.2f}%$'.format(nb_songs_over_2000_words*100/nb_songs)+").")

st.subheader("Artist vocabularies :")
st.plotly_chart(back.fig5)

st.plotly_chart(back.fig6)
st.plotly_chart(back.fig7)

st.plotly_chart(back.fig8)

