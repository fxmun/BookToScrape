# BookToScrape

Projet de scraping sur tous les livres du site http://books.toscrape.com/

Elements relevés:

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

|>> data/
    |>> categorie/
        |>> categorie1.csv
        |>> imgs/
            |>> img1.jpg
            |>> img2.jpg
            |...........
    |-- categorie/
        |>> ............   
```
Installer Python et Git sur l'ordinateur
démarrez la console et se  positionner dans un dossier dédié à cette procédure puis clonez  le dépot avec la commande ci dessous:
```
git clone https://github.com/fxmun/BookToScrape.git
```
Placez vous dans le dossier BookToScrape et executez la commande ci dessous pour créer l'environnement virtuel:
```
python -m venv env
```
Activez l'environnement

Windows:
```
call env\scripts\activate.bat
```
Linux:
```
source env/bin/activate

Installer les packages:
```
pip install -r requirements.txt
```
Executez le fichier avec la commande ci dessous:
```
python main.py