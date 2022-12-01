# BookToScrape

Projet "Extract Transform Load" sur tous les livres du site http://books.toscrape.com/

## Elements relevés:

     - URL du livre
     - Universal Product Code
     - Titre du livre
     - Prix TTC
     - Prix HT
     - Nombre de livres disponibles
     - Résumé
     - Catégorie
     - Note d'appréciation
     - URL de l'image du livre

## Arborescence des données:

### data/
    |>> categorie_1/
        |>> categorie_1.csv
        |>> images/
            |>> image_1.jpg
            |>> image_2.jpg
            |...........
    |>> categorie_2/
        |>> categorie_2.csv  
        |>> images/ 
            |>> image_1.jpg
            |>> image_2.jpg
            |...........


## Machine Windows:

### 1/  Installez Python sur l'ordinateur:

#### https://www.python.org/downloads/

### 2/  Installez Git sur l'ordinateur:

#### https://git-scm.com/downloads

### 3/  démarrez la console git bash (commandes linux) ou git cmd (commandes windows) 
### et se  positionner dans un dossier dédié à cette procédure puis clonez  le dépot en executant la commande:

#### git clone https://github.com/fxmun/BookToScrape.git

### 4/  Placez vous dans le dossier BookToScrape et créez l'environnement virtuel avec la commande:

#### python -m venv env

### 5/  Activez l'environnement virtuel dans la console git cmd avec la commande:

#### call env\scripts\activate.bat

### 6/  Ou activez l'environnement virtuel dans la console git bash avec la commande:

#### source env\scripts\activate.bat

### 7/  Installez les packages avec la commande:

#### pip install -r requirements.txt

## Important:  avant d'executer le fichier python assurez vous que la veille de votre machine n'est pas activée, 
## cela pourait interompre le traitement en cours selon la configuration de celle-ci.
## N'essayez pas d'ouvrir les fichiers pendant le traitement !
## Patientez jusqu'au message "Traitement terminé avec succès ! ...".

### 8/  Executez le fichier avec la commande:

#### python all_cat.py

## Machine Linux:

### 1/  Raprochez vous de votre référent linux pour l'installation des package Python et Git ainsi que pour les commandes
### de clonage du dépot git puis la creation de l'environnement virtuel.

### 2/  Adaptez les étapes 1 à 4 de la procedure windows avec la procedure linux:

### 3/  Activez l'environnement virtuel depuis la console avec la commande:

#### source env/bin/activate

### 4/  Executez le fichier python: