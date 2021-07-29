from bs4 import BeautifulSoup
import urllib.request

page = urllib.request.urlopen('https://www.senscritique.com/top/resultats/Les_meilleurs_albums_de_rap_francais/224928')
soup = BeautifulSoup(page,'html.parser')


links = soup.find_all('a',attrs={'class':'elco-baseline-a'})
artists_1 = [item.contents[0] for item in links]

page = urllib.request.urlopen('https://www.senscritique.com/top/resultats/Les_meilleurs_morceaux_de_rap_francais/531666')
soup = BeautifulSoup(page,'html.parser')

links = soup.find_all('a',attrs={'class':'elco-baseline-a'})
artists_2 = [item.contents[0] for item in links]

artists = artists_1 + artists_2
artists = list(dict.fromkeys(artists))