install:
	conda create -n lyrics-explorer python=3.9
	conda activate lyrics-explorer
	pip install -r requirements.txt

run:
	streamlit run src/app/main.py