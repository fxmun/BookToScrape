import requests
from bs4 import BeautifulSoup
from etl import Livre
from csv_make import csvGen

# requete de l'ensemble des données brutes de la page d'accueil et parse de celles-ci
données = requests.get('http://books.toscrape.com/index.html')
soup = BeautifulSoup(données.text, 'lxml')

themes = {}
print("traitement en cours...")
# boucle sur toutes les balises "a" enfants des balises "ul" enfants des balises "div" de classe "side_categories" puis remplit le dictionnaire "themes"
for a in soup.find('div', {'class': 'side_categories'}).ul.find_all('a'):
    if 'books_1' not in a.get('href'):
        themes[a.text.replace('\n', '').replace('  ', '')] = 'http://books.toscrape.com/' + a.get('href')

# boucle sur chaque element du dictionnaire "themes" afin d'extraire et parser toutes les pages de livres dans chaque theme
for theme, themUrl in themes.items():
    datas = requests.get(themUrl)
    soup = BeautifulSoup(datas.text, 'lxml')

    # verifit si une pagination est existante dans chaque page du dictionnaire "themes" et initialise une variable (nombreDePages)
    if soup.find('ul', {'class': 'pager'}):
        nombreDePages = int(soup.find('li', {'class': 'current'}).text.split(' ')[31].replace('\n',''))
    else:
        nombreDePages = 1

    # boucle sur chaque livre et incremente son url dans un tableau tant que tous les livres de toutes les pages n'ont pas été itérés
    iterPages = 0
    livresUrl = []
    while iterPages < nombreDePages:
        for livre in soup.find_all('article'):
            livreUrl = livre.h3.a.get('href').replace('../../../', 'http://books.toscrape.com/catalogue/')
            livresUrl.append(livreUrl)
        iterPages += 1
        if nombreDePages > 1:
            nextPage = requests.get(themUrl.replace('index.html', 'page-' + str(iterPages+1) + '.html'))
            soup = BeautifulSoup(nextPage.text, 'lxml')

    # incrémente un tableau avec les url de chaque livre pour en extraire les données par les fonctions d'un fichier spécifiques (etl.py)
    livresThemeCourant = []
    for url in livresUrl:
        livreCourant = Livre().generData(url)
        livresThemeCourant.append(livreCourant)

    
    # génère les fichiers csv au moyen d'une fonction d'un fichier dédiée (csv.py)
    csvGen(livresThemeCourant)

    # messages de validation du nombre de livres traités en "Extract Transform Load" par theme
    print("Traitement reussit sur " + str(len(livresThemeCourant)) + " livres de la categorie " + theme)