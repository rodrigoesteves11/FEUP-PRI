from lxml import html
from bs4 import BeautifulSoup
import requests
import json

def read_wikiSpecies():
    # Text file because json is only for the data according to the wikipedia
    file = open("WikiSpeciesV0.txt","w",encoding="utf-8")
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

def get_wikipedia_pages():
   
    wikipedia_base_url = 'https://en.wikipedia.org/wiki/'
    fileR = open("WikiSpeciesUnderScore.txt", "r")

    species_data = {}
    
        
    for line in fileR:
           
            wikipedia_url = wikipedia_base_url + line.strip()  
            
        
            response = requests.get(wikipedia_url)
            
            if response.status_code == 200:
                print(f"Página encontrada: {wikipedia_url}")
                soup = BeautifulSoup(response.content, 'html.parser')
                paragraphs = soup.find_all('p')
                paragraph_texts = [p.get_text().strip() for p in paragraphs if p.get_text().strip()]
                page_content = '\n\n'.join(paragraph_texts)

                infobox = soup.find('table', {'class': 'infobox'})

                if infobox:
                
                    image_tags = infobox.find_all('img')
                
                    if len(image_tags) > 0:
                    
                        image_url = "https:" + image_tags[0]['src']
                        print(f"Segunda imagem encontrada: {image_url}")
                    else:
                        image_url = "No second image found in infobox"
                else:
                    image_url = "No infobox found"
                             
                    
                species_data[line.strip()] = {
                    "content": page_content,
                    "image_url": image_url
                }
                print(f"Conteúdo da página: {page_content[:100]}")
            else:
                print(f"Falha ao obter a página: {wikipedia_url} (Status Code: {response.status_code})")

    with open("species_data.json", "w", encoding="utf-8") as json_file:
        json.dump(species_data, json_file, ensure_ascii=False, indent=4)


#filter_wikiSpecies()
get_wikipedia_pages()

