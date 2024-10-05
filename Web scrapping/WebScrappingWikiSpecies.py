from lxml import html
from bs4 import BeautifulSoup
import requests

def read_wikiSpecies():
    # Text file because json is only for the data according to the wikipedia
    file = open("WikiSpeciesV0.txt","w")
    nextPage = True
    url = 'https://species.wikimedia.org/w/index.php?title=Special:AllPages&from=A+History+of+British+Ferns'

    while(nextPage):
        response = requests.get(url)

        tree = html.fromstring(response.content)
        link_titles = tree.xpath('//ul[@class="mw-allpages-chunk"]//li/a/@title')

        next_page_link = tree.xpath('//a[contains(text(),"Next page")]/@href')


        # Changes url if next page exists, otherwise, changes the var to false
        if next_page_link:
            url = 'https://species.wikimedia.org' + next_page_link[0]
        else:
            nextPage = False

        for title in link_titles:
            file.write(title)
            file.write("\n")
            print(title)


    file.close()



def WikiSpeciesUnderScore():
    fileR = open("WikiSpeciesV0.txt","r")
    fileW = open("WikiSpeciesUnderScore.txt", "w")   
    for line in fileR:
        new_line = line.replace(" ", "_")
        fileW.write(new_line)

#def filter_wikiSpecies():
#    url = 'https://species.wikimedia.org/wiki/'
#
#    fileR = open("WikiSpeciesUnderScore.txt", "r")
#    fileW = open("wikiSpeciesFilterSpecies.txt", "w")
#
#    keywords = ["Realm", "Regnum", "Phylum", "Classis", "Ordo","Familia", "Subfamilia", "Tribus", "Subtribus",  "Genus", "Species"]
#
#    for line in fileR:
#        searchUrl = url + line.strip()
#        response = requests.get(searchUrl)
#        if response.status_code == 200:
#
#            tree = html.fromstring(response.content)
#            checkKeyord = False
#
#            for keyword in keywords:
#                str = '//a[contains(text(),"%s")]/@href' % keyword
#                check = tree.xpath(str)
#                if check:
#                    checkKeyord=True
#                    break
#
#            if checkKeyord:
#                print(line)
#                fileW.write(line)
 

def filter_wikiSpecies():
    url = 'https://species.wikimedia.org/wiki/'

    fileR = open("WikiSpeciesUnderScore.txt", "r")
    fileW = open("wikiSpeciesFilterSpecies.txt", "w")

    for line in fileR:
        searchUrl = url + line.strip()
        response = requests.get(searchUrl)
        if response.status_code == 200:

            tree = html.fromstring(response.content)

            str = '//h2[contains(text(),"Taxonavigation")]'
            check = tree.xpath(str)
            
            if check:
                print(line)
                fileW.write(line)


filter_wikiSpecies()

