import csv


def csvGen(livresListe):

    csvColumns = ['product_page_url', 'universal_ product_code', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url']
    categories = livresListe[0]['category']
    csvFile = categories + '.csv'

    with open('data/' + categories + '/' + csvFile, 'w', errors='replace') as csvFile:
        scribe = csv.DictWriter(csvFile, delimiter=";", fieldnames=csvColumns)
        scribe.writeheader()
        for unit in livresListe:
            scribe.writerow(unit)