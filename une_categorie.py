import requests
from bs4 import BeautifulSoup
import csv
import os

homeUrl = "http://books.toscrape.com/"
page = requests.get(homeUrl)
soup = BeautifulSoup(page.content, 'lxml')

def allUrls():#retourne toutes les catégories
    urls = []
    for a in soup.find('ul',{'class':'nav nav-list'}).li.find_all('a'):
        url = a.get('href').replace('catalogue/','http://books.toscrape.com/catalogue/')
        urls.append(url)
    new = urls[1:]
    return new
new = allUrls()

def oneCateg():#retourne une catégorie
    oneCategories = []
    for oneCateg in allUrls():
        oneCategories.append(oneCateg)
    return oneCategories[2]
oneCategories = oneCateg()

def catBooks(oneCategories):# boucle sur chaque elément d'une catégorie afin d'extraire l'url de chaque livre
    page = requests.get(oneCategories)
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
        if iterPages >= 1:
            nextPage = oneCategories.replace('index.html','page-' + str(iterPages + 1) + '.html')
            page = requests.get(nextPage)
            soup = BeautifulSoup(page.content,'lxml')

    return livresUrl
livresUrl = catBooks(oneCategories)

def main(livresUrl):#boucle sur chaque url de livre d'une catégorie pour en extraire les datas et compléter le fichier csv
    nbrLivres = len(livresUrl)
    unit = 0
    while unit < nbrLivres:
        unLivre = livresUrl[unit]
        unit += 1
        def genData():#extrait les datas d'un livre nécéssaires pour compléter le fichier csv et stocke les images du livre en créant l'arborescence locale
            datas = []
            def prodUrl(unLivre):#retourne l'url du livre
                page = requests.get(oneCategories)
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

            def categorie(oneCategories):#retourne la catégorie du livre
                page = requests.get(oneCateg())
                soup = BeautifulSoup(page.content,'lxml')
                for cat in soup.ul.find_all('li'):
                    if 'Home' not in cat.text and 'Books' not in cat.text:
                        categories = cat.text
                return categories

            categories = categorie(oneCategories)
            datas.append(categories)

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

            def imgLivre():#définit les parametres de création de fichier image du livre
                imageGet = requests.get(image)
                soup = BeautifulSoup(imageGet.content,'lxml')
                cat = categories
                cat = ''.join([x for x in cat if x.isalnum()])
                path = 'data/' + cat + '/images/'
                titre = titres
                titre = ''.join([x for x in titres if x.isalnum()]) + '.jpg'

                # créer les repertoires du path
                if not os.path.exists(path):
                    os.makedirs(path)                
                #copie de l'image
                open(path + titre, 'wb').write(imageGet.content)
                return imageGet
            
            imageGet = imgLivre()
            return datas

        datas = genData()
        #print(datas)
        #print (unit)          
        
        def csvGen(datas):#création du fichier csv
            
                en_tete = ['product_page_url' , 'universal_product_code' , 'title' , 'price_including_tax' , 'price_excluding_tax' , 'number_available' ,'product_description' , 'category' , 'review_rating' , 'image_url']
                cat = datas[7]
                cat = ''.join([x for x in cat if x.isalnum()])
                csvFile = cat + '.csv'
                with open('data/' + cat + '/' + csvFile, 'a', errors = 'replace') as csvFile:
                    scribe = csv.writer(csvFile , delimiter = ";")
                    scribe.writerow(en_tete)      
                    scribe.writerow(datas)
                            
        csvGen(datas)
main(livresUrl)
print('traitement termine avec succes !')