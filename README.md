# LyricsExplorer
A web app allowing you to compare French Hip Hop lyrics

[![Continous Integration](https://github.com/cmnemoi/LyricsExplorer/actions/workflows/ci.yaml/badge.svg)](https://github.com/cmnemoi/LyricsExplorer/actions/workflows/ci.yaml)
[![codecov](https://codecov.io/github/cmnemoi/LyricsExplorer/graph/badge.svg?token=31F9TEL4OU)](https://codecov.io/github/cmnemoi/LyricsExplorer)

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://lyrics-explorer.streamlit.app/)

# Overview

Stack : **Python, Streamlit, Pandas, Plotly, Matplotlib, LyricsGenius, SQLAlchemy, MySQL, AWS RDS**

* 21723 songs collected through LyricsGenius API
* ~~MySQL database hosted on a AWS RDS DB instance~~ Moved to SQLite 
* Nice looking charts automatically generated from data and user entries
* Web app with Streamlit
* Quality pipeline with Github Actions (lint with Ruff, test with Pytest)

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

![Imgur](https://i.imgur.com/5Gz1bBm.png)

## Individual artist

![Imgur](https://imgur.com/inJcVRM.png)

## Correlations

![Imgur](https://imgur.com/nxUandz.png)
