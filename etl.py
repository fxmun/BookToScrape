import requests
import os
from bs4 import BeautifulSoup


class Livre:

    # Extract Transform Load de l'url passée en parametre 
    def initSoup(self, url):
        htmlContent = requests.get(url).content.decode('utf8').encode('utf8', 'ignore')
        soup = BeautifulSoup(htmlContent, 'lxml')
        return soup

    # retourner dictionnaire de produit
    def livreUrl(self, url):
        return {'product_page_url': url}

    # retourner dictionnaire de titre
    def tritreLivre(self, url):
        soup = self.initSoup(url)
        return {'title': soup.h1.text}

    # retourner dictionnaire du taux d'appréciation du livre et de sa description
    def livreNote(self, url):
        soup = self.initSoup(url)

        description = ""
        revision = ""

        for p in soup.find_all('p'):
            try:
                evaluation = p['class']
                if 'star-rating' in evaluation:
                    revision = evaluation[1]
            except KeyError:
                description = p.text
        return {
            'review_rating': revision,
            'product_description': description
        }

    # retourner dictionnaire de categorie
    def themeLivre(self, url):
        soup = self.initSoup(url)
        for a in soup.ul.find_all('a'):
            if 'Home' not in a.text and 'Books' not in a.text:
                return {'category': a.text}

    # retourner dictionnaire de prix ht, de prix ttc et de nombre de  produits disponibles
    def livreUpcPrixStock(self, url):
        soup = self.initSoup(url)

        upc = ""
        prixHt = ""
        prixTtc = ""
        stock = ""

        for tr in soup.find_all('tr'):
            if 'UPC' in tr.text:
                upc = tr.td.text
            elif 'excl' in tr.text:
                prixHt = tr.td.text#.replace('£', '')
            elif 'incl' in tr.text:
                prixTtc = tr.td.text#.replace('£', '')
            elif 'Availability' in tr.text:
                stock = tr.td.text.split(' ')[2].replace('(','')
        return {
            'universal_ product_code': upc,
            'price_excluding_tax': prixHt,
            'price_including_tax': prixTtc,
            'number_available': stock
        }

    # definir l'environnement de variabes nécesssaires aux traitements des images et copie du fichier dans le path definit
    def imgLivre(self, url):
        soup = self.initSoup(url)

        imageUrl = soup.img['src'].replace('../..', 'http://books.toscrape.com')
        imageGet = requests.get(imageUrl)
        categorie = self.themeLivre(url)
        titre = self.tritreLivre(url)
        path = 'data/' + categorie['category'] + '/images'
        titreImg = ''.join([x for x in titre['title'] if x.isalnum()]) + '.jpg'

        # créer une variable d'environement path dans l'operating system
        if not os.path.exists(path):
            os.makedirs(path)
        
        # copie de l'image
        open(path + '/' + titreImg, 'wb').write(imageGet.content)

        return {
            'image_url': imageUrl,
            #'pathImg': path + '/' + titreImg
        }

    # fonction généraliste faisant appel aux fonctions précédentes du code
    def generData(self, url):
        livresDatas = {}
        livresDatas.update(self.livreUrl(url))
        livresDatas.update(self.tritreLivre(url))
        livresDatas.update(self.livreNote(url))
        livresDatas.update(self.themeLivre(url))
        livresDatas.update(self.livreUpcPrixStock(url))
        livresDatas.update(self.imgLivre(url))

        return livresDatas