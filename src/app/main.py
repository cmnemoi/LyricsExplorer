from matplotlib import pyplot as plt
from wordcloud import WordCloud
import streamlit as st

import back


nb_artists = len(back.artists)
nb_songs = len(back.songs)
oldest_song_year = back.songs["release_date"].min().year
newest_song_year = back.songs["release_date"].max().year
nb_songs_over_2000_words = len(
    [song for song in back.songs["lyrics"] if len(song.split(" ")) > 2000]
)

PAGES = ["Global stats", "Individual artist", "Correlations"]
st.sidebar.title("Menu :bulb:")
choix_page = st.sidebar.radio(label="", options=PAGES)


def show_stats_page():
    st.title("French Rap Lyrics Explorator")
    st.header("Insights on French Rap with Data")
    (
        """
    * """
        + str(nb_artists)
        + """ artists
    * """
        + str(nb_songs)
        + """ songs from """
        + str(oldest_song_year)
        + """ to """
        + str(newest_song_year)
    )

    st.header("Who has the biggest ?  (songs produced)")
    st.subheader("Number of songs per artist :")
    st.write(back.nb_songs_per_artist)

    st.subheader("Number of songs per artist per year:")
    st.write(back.nb_songs_per_artist_per_year)

    st.subheader("Top 5 of most prolific artists ever :")
    st.write(
        back.nb_songs_per_artist.sort_values(
            ascending=False, by="Number of songs"
        ).head(5)
    )

    st.subheader("... relatively to their longevity :")
    st.write(back.nb_songs_per_artist_per_year.sort_values(ascending=False).head(5))

    st.subheader("Most of artists released less than 200 songs")
    st.plotly_chart(back.fig1)
    st.subheader("... or 20 songs per year")
    st.plotly_chart(back.fig2)

    st.subheader("Recent artists release more songs than old-school ones")
    st.write("(Try to find Jul...)")
    st.plotly_chart(back.fig3)

    st.header('"Suis-je le seul érudit du carré VIP ?" (Vald - Primitif)')
    st.write("Does Vald is as erudite as he claims ? Let's find out.")

    st.subheader("Number of words used per song :")
    st.plotly_chart(back.fig4)
    st.write(
        "Only "
        + str(nb_songs_over_2000_words)
        + " songs contains more than 2000 words ("
        + r"${:0.2f}%$".format(nb_songs_over_2000_words * 100 / nb_songs)
        + ")."
    )

    st.subheader("Artist vocabularies :")
    st.plotly_chart(back.fig5)

    st.plotly_chart(back.fig6)
    st.plotly_chart(back.fig7)

    st.plotly_chart(back.fig8)


def show_artist_page():
    st.write("Work In Progress")

    st.title("French Rap Lyrics Explorator")
    st.header("Insights on French Rap with Data")

    selected_artist = st.selectbox("Choose an artist", back.artists)

    st.subheader(
        selected_artist
        + " produced "
        + str(back.nb_songs_per_artist.loc[selected_artist, "Number of songs"])
        + " songs in total and "
        + str("{:0.2f}".format(back.nb_songs_per_artist_per_year.loc[selected_artist]))
        + " songs per year"
    )
    st.write(
        "That's more than "
        + str(
            "{:0.2f}".format(
                (
                    1
                    - back.nb_songs_per_artist.rank(pct=True).loc[
                        selected_artist, "Number of songs"
                    ]
                )
                * 100
            )
        )
        + "% of artists."
    )

    st.subheader(
        selected_artist
        + " used "
        + str("{:0.2f}".format(back.nb_words_per_song_per_artist.loc[selected_artist]))
        + " words in total and "
        + str(
            "{:0.2f}".format(back.lexical_diversity.loc[selected_artist, "mean"] * 100)
        )
        + "% of unique words per song in average"
    )
    st.write(
        "That's more than "
        + str(
            "{:0.2f}".format(
                (
                    1
                    - back.nb_words_per_song_per_artist.rank(pct=True).loc[
                        selected_artist
                    ]
                )
                * 100
            )
        )
        + "% of artists."
    )

    st.subheader("Word cloud of " + selected_artist)

    wc = WordCloud(width=800, height=400).generate_from_frequencies(
        back.gen_freq(back.artist_lyrics(selected_artist))
    )
    chart = plt.figure(figsize=(20, 20))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    st.pyplot(chart)


def show_correlations_page():
    st.write("Work In Progress")

    st.title("French Rap Lyrics Explorator")
    st.header("Insights on French Rap with Data")

    first_term = st.text_input("Type one term")
    second_term = st.text_input("Type another term")

    if first_term != "" and second_term != "":
        first_term_frequency = back.calcTermFreqAcrossArtists(back.artists, first_term)
        second_term_frequency = back.calcTermFreqAcrossArtists(
            back.artists, second_term
        )

        x = first_term_frequency["frequency"].values * 100
        y = second_term_frequency["frequency"].values * 100
        y_fit, t, r2 = back.fitLine(x, y)
        i, j = back.np.argmin(t), back.np.argmax(t)

        fig9_1 = back.px.scatter(x=x, y=y, hover_name=back.artists)
        fig9 = back.go.Figure(
            data=fig9_1.data, layout=back.go.Layout(width=800, height=800)
        )
        fig9.add_scatter(
            x=t[[i, j]], y=y_fit[[i, j]], mode="lines", line=dict(color="white")
        )
        fig9.update_layout(
            title='Mentions of "{}" and "{}" in French rap'.format(
                first_term_frequency.term, second_term_frequency.term
            )
        )
        fig9.update_xaxes(
            title='Percent of an artist\'s songs mentioning "{}"'.format(
                first_term_frequency.term
            )
        )
        fig9.update_yaxes(
            title='% of an artist\'s songs mentioning "{}"'.format(
                second_term_frequency.term
            )
        )
        fig9.add_annotation(text=r"R²={:0.2f}".format(r2), x=30, y=0)

        st.plotly_chart(fig9)


if choix_page == "Global stats":
    show_stats_page()
elif choix_page == "Individual artist":
    show_artist_page()
elif choix_page == "Correlations":
    show_correlations_page()
