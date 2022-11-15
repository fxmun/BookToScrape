import requests
from bs4 import BeautifulSoup
import csv
import os

homeUrl = "http://books.toscrape.com/"
page = requests.get(homeUrl)
soup = BeautifulSoup(page.content, 'html.parser')

#print('traitement en cours, veuillez patienter ...')

def allUrls():#retourne toutes les catégories
    urls=[]
    for a in soup.find('ul',{'class':'nav nav-list'}).li.find_all('a'):
        url=a.get('href').replace('catalogue/','http://books.toscrape.com/catalogue/')
        urls.append(url)
    return urls

allUrls()

def oneCateg():#retourne une catégorie
    oneCategories=[]
    for oneCateg in allUrls():
        oneCategories.append(oneCateg)
    return oneCategories[10]

oneCateg()

def catBooks():# boucle sur chaque elément d'une catégorie afin d'extraire l'url de chaque livre
    page=requests.get(oneCateg())
    soup=BeautifulSoup(page.content,'html.parser')
    
    # verifit si une pagination est existante
    if soup.find('ul', class_='pager'):
        nombreDePages = int(soup.find('li', class_='current').text.split(' ')[31].replace('\n',''))
    else:
        nombreDePages = 1

    # boucle sur chaque livre et incremente son url dans un tableau
    iterPages = 0
    livresUrl = []
    nextPage=""
    
    if iterPages < 1:

        for livre in soup.find_all('article'):
            livreUrl = livre.h3.a.get('href').replace('../../../', 'http://books.toscrape.com/catalogue/')
            livresUrl.append(livreUrl)
        iterPages += 1

    while iterPages != nombreDePages:
        
        if iterPages < nombreDePages:
            nextPage = oneCateg().replace('index.html','page-'+str(iterPages+1)+'.html')
            page=requests.get(nextPage)
            soup=BeautifulSoup(page.content,'html.parser')

            for book in soup.find_all('article'):
                livre = book.div.a.get('href').replace('../../../', 'http://books.toscrape.com/catalogue/')
                livresUrl.append(livre)    
            iterPages += 1
                  
        return livresUrl[0]

catBooks()

def prodUrl():#retourne l'url du livre
    page=requests.get(oneCateg())
    soup=BeautifulSoup(page.content,'html.parser')
    data1=[]
    prod=catBooks()
    data1.append(prod)
    return prod

prodUrl()

def upc():#retourne le code du livre
    page=requests.get(catBooks())
    soup=BeautifulSoup(page.content,'html.parser')
    data2=[]
    for upc in soup.find_all('tr'):
        if 'UPC' in upc.text:
            upcs = upc.td.text
            data2.append(upcs)
    return upcs

upc()

def titre():#retourne le titre du livre
    page=requests.get(catBooks())
    soup=BeautifulSoup(page.content,'html.parser')
    data3=[]
    for titre in soup.find_all('h1'):
        titres=titre.text
        data3.append(titres)
    return titres

titre()

def ttc():#retourne le prix ttc du livre
    page=requests.get(catBooks())
    soup=BeautifulSoup(page.content,'html.parser')
    data4=[]
    for ttc in soup.find_all('tr'):
        if 'excl' in ttc.text:
            ttcs = ttc.td.text
            data4.append(ttcs)
    return ttcs

ttc()

def ht():#retourne le prix ht du livre
    page=requests.get(catBooks())
    soup=BeautifulSoup(page.content,'html.parser')
    data5=[]
    for ht in soup.find_all('tr'):
        if 'excl' in ht.text:
            hts = ht.td.text
            data5.append(hts)
    return hts

ht()

def dispo():#retourne le nombre de livres disponibles
    page=requests.get(catBooks())
    soup=BeautifulSoup(page.content,'html.parser')
    data6=[]
    for dispo in soup.find_all('tr'):
        if 'Availability' in dispo.text:
            dispos = dispo.td.text.split(' ')[2].replace('(','')
            data6.append(dispos)
    return dispos

dispo()

def descript():#retourne un résumé du livre
    page=requests.get(catBooks())
    soup=BeautifulSoup(page.content,'html.parser')
    data7 = []
    desc=soup.find_all('p',)[3]
    descript = desc.text
    data7.append(descript)
    return descript

descript()     

def categorie():#retourne la catégorie du livre
    page=requests.get(oneCateg())
    soup=BeautifulSoup(page.content,'html.parser')
    data8 = []
    for cat in soup.ul.find_all('li'):
        if 'Home' not in cat.text and 'Books' not in cat.text:
            categ = cat.text
            data8.append(categ)    
    return categ

categorie()

def eval():#retourne l'appréciation du livre
    page=requests.get(catBooks())
    soup=BeautifulSoup(page.content,'html.parser')
    data9=[]
    for star in soup.find_all('p',limit=4):
        try:
            note = star['class']
            if 'star-rating' in note:
                note = note[1]
                data9.append(note)
        except KeyError:
            pass
    return note            

eval()

def img():#retourne l'url de l'image du livre
    page=requests.get(catBooks())
    soup=BeautifulSoup(page.content,'html.parser')
    data10=[]
    img=soup.find('img')
    image=img['src'].replace('../..','http://books.toscrape.com')
    data10.append(image)
    return image

img()

livresUrl=[catBooks()]
product_page_url=[prodUrl()]
universal_product_code=[upc()]
title=[titre()]
price_including_tax=[ttc()]
price_excluding_tax=[ht()]
number_available=[dispo()]
product_description=[descript()]
category=[categorie()]
review_rating=[eval()]
image_url=[img()]

def imgLivre():#définit les parametres de création de fichier image du livre
    imageGet=requests.get(img())
    cat=str(category)
    cat=''.join([x for x in cat if x.isalnum()])
    path = 'data/' + cat + '/images'
    titreImg=titre()
    titreImg = ''.join([x for x in title if x.isalnum()]) + '.jpg'

    # créer les repertoires du path
    if not os.path.exists(path):
        os.makedirs(path)
    
    #copie de l'image
    open(path + '/' + titreImg, 'wb').write(imageGet.content)
    return imageGet
    
imgLivre()

#création du fichier csv
en_tete = ["product_page_url" , "universal_product_code" , "title" , "price_including_tax" , "price_excluding_tax" , "number_available" ,"product_description" , "category" , "review_rating" , "image_url"]
with open("un_livre.csv" , "w") as fichier_csv:
    scribe = csv.writer(fichier_csv , delimiter=";")
    scribe.writerow(en_tete)
    for prod,upc,titr,ttc,ht,numb,descr,catego,review,imag in zip(product_page_url,universal_product_code,title,price_including_tax,price_excluding_tax,number_available,product_description,category,review_rating,image_url):
        liste=[prod,upc,titr,ttc,ht,numb,descr,catego,review,imag]
    scribe.writerow(liste)

print('traitement termine avec succes !')