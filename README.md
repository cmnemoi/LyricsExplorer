# LyricsExplorer
A web app allowing you to compare French Hip Hop lyrics

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://lyrics-explorer.streamlit.app/)

# Overview

Stack : **Python, Streamlit, Pandas, Plotly, Matplotlib, LyricsGenius, SQLAlchemy, MySQL, AWS RDS**

* 21723 songs collected through LyricsGenius API
* ~~MySQL database hosted on a AWS RDS DB instance~~ Moved to SQLite 
* Nice looking charts automatically generated from data and user entries
* Web app with Streamlit

# Run the project locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run src/app/main.py
```

# Sections

## Global stats

![](https://i.ibb.co/kMy7zCW/Sans-titre.png)
![](https://cdn.discordapp.com/attachments/513701275305639947/890300386139844678/newplot1.png)

## Individual artist

![](https://cdn.discordapp.com/attachments/513701275305639947/890300403135152128/newplot3.png)

## Correlations

![](https://cdn.discordapp.com/attachments/513701275305639947/890300388014694470/newplot4.png)

## Add artist

![](https://cdn.discordapp.com/attachments/513701275305639947/890300386286645298/newplot5.png)
![](https://cdn.discordapp.com/attachments/513701275305639947/890300386781593630/newplot6.png)

