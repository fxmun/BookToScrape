import requests
from bs4 import BeautifulSoup
import csv
import os   

homeUrl = "http://books.toscrape.com/"

def allUrls(homeUrl):# retourne toutes les catégories
    page = requests.get(homeUrl)
    soup = BeautifulSoup(page.content, 'lxml')
    urls = []
    for a in soup.find('ul',{'class':'nav nav-list'}).li.find_all('a'):
        url = a.get('href').replace('catalogue/','http://books.toscrape.com/catalogue/')
        urls.append(url)
    categs = urls[1:]
    return categs
categs = allUrls(homeUrl)

def oneCateg(categs):# retourne une catégorie
    booksCategorie = ''
    for cat in categs:
        booksCategorie = cat
        return booksCategorie

booksCategorie = oneCateg(categs)

def catBooks(booksCategorie):# complete une liste (livresUrl) avec toutes les url d'une catégorie
    page = requests.get(booksCategorie)
    soup = BeautifulSoup(page.content,'lxml')
        
    # vérifit si une pagination est existante
    if soup.find('ul', class_ = 'pager'):
        nombreDePage = int(soup.find('li', class_='current').text[40])
    else:
        nombreDePage = 1

    # boucle sur chaque livre pour compléter son url en fonction de la pagination
    iterPages = 0
    livresUrl = []
        
    while iterPages < nombreDePage:
        for livre in soup.find_all('article'):
            livreUrl = livre.h3.a.get('href').replace('../../../', 'http://books.toscrape.com/catalogue/')
            livresUrl.append(livreUrl)
        iterPages += 1
        if iterPages >= 1 and nombreDePage > 1:
            nextPage = booksCategorie.replace('index.html','page-' + str(iterPages + 1) + '.html')
            page = requests.get(nextPage)
            soup = BeautifulSoup(page.content,'lxml')
    return livresUrl

livresUrl = catBooks(booksCategorie)

def oneBook(livresUrl):# retourne un livre de la liste des url d'une catgorie
    unLivre = ''
    for book in livresUrl:
        unLivre = book
        return unLivre

unLivre = oneBook(livresUrl)

def genData(unLivre,booksCategorie):# complete une liste avec toute les data du livre et sa categorie
    datas = []
    def prodUrl(unLivre):# retourne l'url du livre
        page = requests.get(unLivre)
        soup = BeautifulSoup(page.content,'lxml')
        prods = unLivre
        return prods

    prods = prodUrl(unLivre)
    datas.append(prods)

    def upc(unLivre):# retourne le code du livre
        page = requests.get(unLivre)
        soup = BeautifulSoup(page.content,'lxml')
        for upc in soup.find_all('tr'):
            if 'UPC' in upc.text:
                upcs = upc.td.text
        return upcs

    upcs = upc(unLivre)
    datas.append(upcs)

    def title(unLivre):# retourne le titre du livre
        page = requests.get(unLivre)
        soup = BeautifulSoup(page.content,'lxml')
        for title in soup.find_all('h1'):
            titre = title.text
        return titre

    titre = title(unLivre)
    datas.append(titre)

    def ttc(unLivre):# retourne le prix ttc du livre
        page = requests.get(unLivre)
        soup = BeautifulSoup(page.content,'lxml')
        for ttc in soup.find_all('tr'):
            if 'excl' in ttc.text:
                ttcs = ttc.td.text
        return ttcs

    ttcs = ttc(unLivre)
    datas.append(ttcs)

    def ht(unLivre):# retourne le prix ht du livre
        page = requests.get(unLivre)
        soup = BeautifulSoup(page.content,'lxml')
        for ht in soup.find_all('tr'):
            if 'excl' in ht.text:
                hts = ht.td.text
        return hts

    hts = ht(unLivre)
    datas.append(hts)

    def dispo(unLivre):# retourne le nombre de livres disponibles
        page = requests.get(unLivre)
        soup = BeautifulSoup(page.content,'lxml')
        for dispo in soup.find_all('tr'):
            if 'Availability' in dispo.text:
                dispos = dispo.td.text.split(' ')[2].replace('(','')
        return dispos

    dispos = dispo(unLivre)
    datas.append(dispos)

    def descript(unLivre):# retourne un résumé du livre
        page = requests.get(unLivre)
        soup = BeautifulSoup(page.content,'lxml')
        desc = soup.find_all('p',)[3]
        descripts = desc.text
        return descripts

    descripts = descript(unLivre)
    datas.append(descripts)

    def categorie(booksCategorie):# retourne la catégorie du livre
        page = requests.get(booksCategorie)
        soup = BeautifulSoup(page.content,'lxml')
        for cat in soup.ul.find_all('li'):
            if 'Home' not in cat.text and 'Books' not in cat.text:
                categorie = cat.text
        return categorie

    categorie = categorie(booksCategorie)
    datas.append(categorie)

    def eval(unLivre):# retourne l'appréciation du livre
        page = requests.get(unLivre)
        soup = BeautifulSoup(page.content,'lxml')
        for star in soup.find_all('p',limit = 4):
            try:
                note = star['class']
                if 'star-rating' in note:
                    note = note[1]

            except KeyError:
                pass
        return note

    note = eval(unLivre)
    datas.append(note)            

    def img(unLivre):# retourne l'url de l'image du livre
        page = requests.get(unLivre)
        soup = BeautifulSoup(page.content,'lxml')
        img = soup.find('img')
        image = img['src'].replace('../..','http://books.toscrape.com')
        return image

    image = img(unLivre)
    datas.append(image)  

    def path(categorie):# crée l'arborescence des dossiers et retourne le chemin relatif
        cat = categorie
        cat = ''.join([x for x in cat if x.isalnum()])
        path = 'data/' + cat + '/images/'
        # créer les repertoires du path
        if not os.path.exists(path):
            os.makedirs(path)
        return path
    
    path = path(categorie)
    datas.append(path)

    def imgLivre(image, path, titre):# définit les paramètres de création du fichier image du livre et crée le fichier
        imageGet = requests.get(image)
        soup = BeautifulSoup(imageGet.content,'lxml')
        titre = ''.join([x for x in titre if x.isalnum()]) + '.jpg'    
        open(path + titre, 'wb').write(imageGet.content)
        return imageGet

    imageGet = imgLivre(image, path, titre)
    datas.append(imageGet)

    return datas

datas = genData(unLivre, booksCategorie)

def main():# appele les fonctions sus-jacente  en leur passant les parametres nécessaires en arguments et crée les fichiers csv
    categs = allUrls(homeUrl)
    for cat in categs:
        booksCategorie = catBooks(cat)
        page = requests.get(cat)
        soup = BeautifulSoup(page.content,'lxml')
        for oneCat in soup.ul.find_all('li'):
            if 'Home' not in oneCat.text and 'Books' not in oneCat.text:
                categorie = oneCat.text

        # création du fichier csv pour chaque catégorie en complètant uniquement l'entête
        en_tete = ['product_page_url' , 'universal_product_code' , 'title' , 'price_including_tax' , 'price_excluding_tax' , 'number_available' ,'product_description' , 'category' , 'review_rating' , 'image_url']
        categorie = ''.join([x for x in categorie if x.isalnum()])
        csvFile = categorie + '.csv'
        path = 'data/' + categorie + '/'
        if not os.path.exists(path):
            os.makedirs(path)
        with open(path + csvFile, 'w', errors = 'replace') as csvFile:
            scribe = csv.writer(csvFile , delimiter = ";")
            scribe.writerow(en_tete)

        for book in booksCategorie:# récupère les data de chaque livre et complète le fichier csv de chaque catégorie
                livres = oneBook(booksCategorie)
                datas = genData(book, cat)
                page = requests.get(cat)
                soup = BeautifulSoup(page.content,'lxml')
                for oneCat in soup.ul.find_all('li'):
                    if 'Home' not in oneCat.text and 'Books' not in oneCat.text:
                        categorie = oneCat.text
                categorie = ''.join([x for x in categorie if x.isalnum()])
                csvFile = categorie + '.csv'
                path = 'data/' + categorie + '/'
                with open(path + csvFile, 'a', errors = 'replace') as csvFile:
                    scribe = csv.writer(csvFile , delimiter = ";")
                    scribe.writerow(datas[0:-2]) 

main()

print("Traitement termine avec succes ! ...")