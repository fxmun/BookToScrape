'''def remplir_entete():
    en_tete = ['product_page_url' , 'universal_product_code' , 'title' , 'price_including_tax' , 'price_excluding_tax' , 'number_available' ,'product_description' , 'category' , 'review_rating' , 'image_url']
    with open('data/' + cat + '/' + csvFile, 'a', errors = 'replace') as csvFile:
                
                


def get_datas_of_a_book(url_book)
    ...
    
def get_urls_off_all_books_of_a_category(url_category)
    ...
    
def get_urls_off_all_categories(url_site)
    ...
    
def imgLivre(img):
    ...

    
main():
    url_site = 'https://....'
    list_of_cat = get_urls_off_all_categories(url_site)
    for cat in list_of_cat:
        list_of_books = get_urls_off_all_books_of_a_category(cat)
        # create cat_csv file and add entete line
        for book in list_of_books:
            datas = get_datas_of_a_book(book)
            # open cat_csv file and append datas sauf image
            imgLivre(datas.image)'''

import requests
from bs4 import BeautifulSoup
import csv
import os

homeUrl = "http://books.toscrape.com/"

def allUrls(homeUrl):#retourne toutes les catégories
    page = requests.get(homeUrl)
    soup = BeautifulSoup(page.content, 'lxml')
    urls = []
    for a in soup.find('ul',{'class':'nav nav-list'}).li.find_all('a'):
        url = a.get('href').replace('catalogue/','http://books.toscrape.com/catalogue/')
        urls.append(url)
    categs = urls[1:]
    return categs
categs = allUrls(homeUrl)

def oneCateg(categs):#retourne une catégorie
    #page = requests.get(categs)
    #soup = BeautifulSoup(page.content,'lxml')
    booksCategorie = categs[0]
    return booksCategorie
booksCategorie = oneCateg(categs)

def catBooks(booksCategorie):# boucle sur chaque elément d'une catégorie afin d'extraire l'url de chaque livre
    page = requests.get(booksCategorie)
    soup = BeautifulSoup(page.content,'lxml')
        
    # verifit si une pagination est existante
    if soup.find('ul', class_ = 'pager'):
        nombreDePage = int(soup.find('li', class_='current').text[40])
    else:
        nombreDePage = 1

    # boucle sur chaque livre et incremente son url dans un tableau
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

unLivre = livresUrl[0]

def genData(unLivre):
    datas = []
    def prodUrl(unLivre):#retourne l'url du livre
        page = requests.get(booksCategorie)
        soup = BeautifulSoup(page.content,'lxml')
        prods = unLivre
        return prods

    prods = prodUrl(unLivre)
    datas.append(prods)

    def upc(unLivre):#retourne le code du livre
        page = requests.get(unLivre)
        soup = BeautifulSoup(page.content,'lxml')
        for upc in soup.find_all('tr'):
            if 'UPC' in upc.text:
                upcs = upc.td.text
        return upcs

    upcs = upc(unLivre)
    datas.append(upcs)

    def titre(unLivre):#retourne le titre du livre
        page = requests.get(unLivre)
        soup = BeautifulSoup(page.content,'lxml')
        for titre in soup.find_all('h1'):
            titres = titre.text
        return titres

    titres = titre(unLivre)
    datas.append(titres)

    def ttc(unLivre):#retourne le prix ttc du livre
        page = requests.get(unLivre)
        soup = BeautifulSoup(page.content,'lxml')
        for ttc in soup.find_all('tr'):
            if 'excl' in ttc.text:
                ttcs = ttc.td.text
        return ttcs

    ttcs = ttc(unLivre)
    datas.append(ttcs)

    def ht(unLivre):#retourne le prix ht du livre
        page = requests.get(unLivre)
        soup = BeautifulSoup(page.content,'lxml')
        for ht in soup.find_all('tr'):
            if 'excl' in ht.text:
                hts = ht.td.text
        return hts

    hts = ht(unLivre)
    datas.append(hts)

    def dispo(unLivre):#retourne le nombre de livres disponibles
        page = requests.get(unLivre)
        soup = BeautifulSoup(page.content,'lxml')
        for dispo in soup.find_all('tr'):
            if 'Availability' in dispo.text:
                dispos = dispo.td.text.split(' ')[2].replace('(','')
        return dispos

    dispos = dispo(unLivre)
    datas.append(dispos)

    def descript(unLivre):#retourne un résumé du livre
        page = requests.get(unLivre)
        soup = BeautifulSoup(page.content,'lxml')
        desc = soup.find_all('p',)[3]
        descripts = desc.text
        return descripts

    descripts = descript(unLivre)
    datas.append(descripts)

    def categorie(booksCategorie):#retourne la catégorie du livre
        page = requests.get(booksCategorie)
        soup = BeautifulSoup(page.content,'lxml')
        for cat in soup.ul.find_all('li'):
            if 'Home' not in cat.text and 'Books' not in cat.text:
                categorie = cat.text
        return categorie

    categorie = categorie(booksCategorie)
    datas.append(categorie)

    def eval(unLivre):#retourne l'appréciation du livre
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

    def img(unLivre):#retourne l'url de l'image du livre
        page = requests.get(unLivre)
        soup = BeautifulSoup(page.content,'lxml')
        img = soup.find('img')
        image = img['src'].replace('../..','http://books.toscrape.com')
        return image

    image = img(unLivre)
    datas.append(image)  

    def path(categorie):
        cat = categorie
        cat = ''.join([x for x in cat if x.isalnum()])
        path = 'data/' + cat + '/images/'
        # créer les repertoires du path
        if not os.path.exists(path):
            os.makedirs(path)
        return path
    path = path(categorie)
    datas.append(path)

    def imgLivre(image, path, titres):#définit les parametres de création de fichier image du livre
        imageGet = requests.get(image)
        soup = BeautifulSoup(imageGet.content,'lxml')
        titres = ''.join([x for x in titres if x.isalnum()]) + '.jpg'    
        open(path + titres, 'wb').write(imageGet.content)
        return imageGet

    imageGet = imgLivre(image, path, titres)
    datas.append(imageGet)
    
    def genCsv():
        en_tete = ['product_page_url' , 'universal_product_code' , 'title' , 'price_including_tax' , 'price_excluding_tax' , 'number_available' ,'product_description' , 'category' , 'review_rating' , 'image_url']
        categorie = datas[7]
        categorie = ''.join([x for x in categorie if x.isalnum()])
        csvFile = categorie + '.csv'
        path = 'data/' + categorie + '/'
        with open(path + csvFile, 'w', errors = 'replace') as csvFile:
            scribe = csv.writer(csvFile , delimiter = ";")
            scribe.writerow(en_tete)
            scribe.writerow(datas[0:-2])
        return csvFile

    csvFile = genCsv() 

    return datas

datas = genData(unLivre)     

def main():
    homeUrl = "http://books.toscrape.com/"
    listCategs = allUrls(homeUrl)
    for cat in listCategs:
        listBooks = catBooks(cat)
        # create cat_csv file and add entete line
        for book in listBooks:
            datas = genData(book)
            imgLivre(datas[9], datas[10], datas[2])

print(datas)