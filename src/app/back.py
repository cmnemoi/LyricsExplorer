import numpy as np
import pandas as pd
import streamlit as st
from matplotlib import pyplot as plt
import seaborn as sns
sns.set()
import plotly.express as px
import plotly.graph_objects as go
from stop_words import get_stop_words
import re
from wordcloud import WordCloud
from datetime import datetime
from sqlalchemy import create_engine
from os import environ
import lyricsgenius as genius
from sqlalchemy import *
# from dotenv import load_dotenv
# load_dotenv()


@st.cache
def clean_text(text):
    #remove \n=
    text = text.replace('\n',' ')

    #remove... something
    text = re.sub(r'43embedshare urlcopyembedcopy','',text)
    
    #Remove punctuations
    text = re.sub(r'[?!.;:,#@-]', '', text)

    #Convert to lowercase to maintain consistency
    text = text.lower()
    return text

@st.cache
def gen_freq(text,nb_words=20):
    #Will store the list of words
    word_list = []

    #Loop over all the tweets and extract words into word_list
    for tw_words in text.split():
        word_list.append(tw_words)

    #Create word frequencies using word_list
    stopwords = get_stop_words('fr',cache=False)
    word_freq = pd.Series(word_list).value_counts()
    word_freq = word_freq.drop(labels=stopwords, errors='ignore')
    
    word_freq[:nb_words]
    
    return word_freq

@st.cache
def all_lyrics():
    s=''
    for i in range(len(songs['lyrics'])):
        s = s.__add__(songs.loc[i,'cleaned_lyrics'])

    return s

@st.cache
def artist_lyrics(artist):
    s = ''
    for i in range(len(songs['lyrics'])):
        if songs.loc[i,'artist'] == artist:
          s += songs.loc[i,'cleaned_lyrics']
    return s

@st.cache
def lexdiv(lyrics):
    try:
        return len(set(lyrics.split()))/float(len(lyrics.split()))
    except:
        return 0

@st.cache
def calc_artist_nb_of_words(artist):
    return len(artist_lyrics(artist).split(' '))
    
@st.cache
def calcFreqOfTerm(artist, terms):    
    # Determine how many songs mention a given term
    sgs = songs[songs['artist'] == artist]
    sgs.reset_index(drop=True,inplace=True)
    song_count, term_count = len(sgs), 0
    for i in range(len(sgs)):
        for term in terms:            
            if term.lower() in sgs.loc[i,'cleaned_lyrics'].lower():
                term_count += 1
                break

    term_freq = round(term_count/float(song_count),5)    
    data = np.reshape([term_freq, term_count, song_count],(1,3))
    # return data
    return pd.DataFrame(data, columns=['frequency','count','total'], index=[artist])

@st.cache
def calcTermFreqAcrossArtists(artists, terms):
    if not isinstance(terms, list):
        terms = [terms]

    term_freqs = pd.concat([calcFreqOfTerm(artist, terms) for artist in artists],axis=0)
    term_freqs.term = "_OR_".join(terms)
    return term_freqs

@st.cache
def fitLine(x, y):
    A = np.vstack([x, np.ones(len(x))]).T
    soln = np.linalg.lstsq(A, y, rcond=None)[0]    
    
    # residual sum of squares
    y_fit = soln[0]*x + soln[1]
    ss_res = np.sum((y - y_fit)**2) # residuals ?
    ss_tot = np.sum((y - y.mean())**2) # total sum of squares
    r2 = round(1 - (ss_res / ss_tot), 3) # r-squared
        
    return y_fit, x, r2
  
@st.cache
def load_dataset():
    engine = create_engine('mysql+mysqlconnector://'+db_config['user']+':'+db_config['password']+"@"
    +db_config['host']+':'+str(db_config['port'])+'/'+db_config['database'])
    connection = engine.connect()

    return pd.read_sql('songs'.lower(),connection)

@st.cache
def getLyrics(artist,max_songs=None):

    client_access_token = environ['GENIUS_CLIENT_ACCESS_TOKEN']

    api = genius.Genius(client_access_token)
    api.remove_section_headers=True
    api.retries=1000
    api.timeout=10
    api.excluded_terms = ["(Remix)", "(Live)"]

    a = api.search_artist(artist,max_songs)
    songs = []
    for i in range(len(a.songs)):
        songs.append(a.songs[i].to_dict())
    return songs
    

db_config = {
  'user': environ['USER'],
  'password': environ['PASSWORD'],
  'host': environ['HOST'],
  'database': environ['DATABASE'],
  'port': environ['PORT']
}

#connecting to DB and get dataset
songs = load_dataset()

#cleaning dataset and feature engineerin
songs = songs[songs['artist'] != 'Blue Virus']
songs = songs[songs['lyrics'].notna()]

songs['release_date'] = [datetime.strptime(x,'%Y-%m-%d') if x != None else None for x in songs['release_date'] ]

songs['age'] = [ (datetime.now() - x).days/365.25 if x != None else None for x in songs['release_date']]
songs = songs[songs['age'] < 35]

songs['cleaned_lyrics']= [clean_text(item) for item in songs['lyrics']]


artists = np.unique(songs['artist'])

songs['lexical_diversity'] = songs['cleaned_lyrics'].apply(lexdiv)
lexical_diversity = songs.groupby('artist')['lexical_diversity'].describe()
min_lexdiv = artists[lexical_diversity['mean'].argmin()]
max_lexdiv = artists[lexical_diversity['mean'].argmax()]

songs.reset_index(drop=True,inplace=True)

nb_songs_per_artist_l = [songs.groupby('artist').count().loc[artist,'title'] for artist in artists]
nb_songs_per_artist = pd.DataFrame(nb_songs_per_artist_l,columns=['Number of songs'],index=artists)
nb_songs_per_artist_per_year = nb_songs_per_artist['Number of songs']/songs.groupby('artist')['age'].max().values

# Words per song
word_counts = [len(song.split(' ')) for song in songs['lyrics']]
word_counts = list(filter(lambda x: x<2000, word_counts))

#Words per song per artist
nb_words_per_song_per_artist = pd.Series([calc_artist_nb_of_words(artist)/nb_songs_per_artist.loc[artist,'Number of songs'] for artist in artists],index=artists)

#graphs
fig1 = px.bar(x=artists,y=nb_songs_per_artist_l,title='Distribution of number of songs per artist'
            ,labels={'x':'Artists','y':'Number of songs'},width=800,height=800)

fig2 = px.bar(x=artists,y=nb_songs_per_artist_per_year,title='Distribution of number of songs per artist per year',
                labels={'x':'Artists','y':'Number of songs per year'},width=800,height=800)

x= songs.groupby('artist')['age'].max().values
y= nb_songs_per_artist_per_year
y_fit, t, r2 = fitLine(x, y)
i,j = np.argmin(t), np.argmax(t)

fig3_1 = px.scatter(x=x,y=y,hover_name=artists,labels={'x':'Years of activity','y':'Number of songs per year'},width=800,height=800)
fig3 = go.Figure(data=fig3_1.data,layout=go.Layout(width=800,height=800))
fig3.add_scatter(x=t[[i,j]], y=y_fit[[i,j]],mode='lines',line=dict(color='white'))
fig3.add_annotation(text=r'R²={:0.2f}'.format(r2),x=28,y=50)
fig3.update_layout({'title':"Number of songs per year per years of activity",'width':800,'height':800})
fig3.update_xaxes(title="Years of activity")
fig3.update_yaxes(title="Number of songs per year")

fig4 = px.histogram(word_counts,title="Histogram of words per song",width=800,height=800,labels={'value':'Words in song','count':'Number of songs'})

fig5 = px.bar(x=artists,y=nb_words_per_song_per_artist,width=800,height=800,title='Distribution of number of words per song per artist',
              labels={'x':'Artists','y':'Number of words'})

fig6 = px.histogram(lexical_diversity['mean']*100,width=800,height=800,title='Histogram of percentage of UNIQUE words per song',
              labels={'x':'Percentage of unique words'})

fig7 = px.bar(x=artists,y=lexical_diversity['mean']*100,width=800,height=800,title='Percentage of UNIQUE words per song per artist',
              labels={'x':'Artists','y':'Percentage of unique words'})

x= songs['age']
y= songs['lexical_diversity']*100
y_fit, t, r2 = fitLine(x, y)
i,j = np.argmin(t), np.argmax(t)

fig8_1 = px.scatter(x=songs['age'],y=songs['lexical_diversity']*100,hover_name=songs['title'],
                    labels={'x':'Age','y':'Lexical diversity'})
fig8 = go.Figure(data=fig8_1.data,layout=go.Layout(width=800,height=800))
fig8.add_scatter(x=t[[i,j]], y=y_fit[[i,j]],mode='lines',line=dict(color='white'))
fig8.update_layout(title="Lexical diversity given the age of the song")
fig8.update_xaxes(title="Age")
fig8.update_yaxes(title="Lexical diversity (% of unique words)")
fig8.add_annotation(text=r'R²={:0.2f}'.format(r2),x=30,y=0)



