from lxml import html
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
import requests

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



#GPT MULTITHREAD
def fetch_and_filter_species(line, url, file_lock):
    searchUrl = url + line.strip()
    try:
        response = requests.get(searchUrl)
        if response.status_code == 200:
            tree = html.fromstring(response.content)

            xpath_str = '//h2[contains(text(),"Taxonavigation")]'
            check = tree.xpath(xpath_str)

            if check:
                print(line.strip())  # Printing the species found
                with file_lock:  # Ensure thread-safe file write
                    with open("wikiSpeciesFilterSpecies.txt", "a") as fileW:
                        fileW.write(line)
    except Exception as e:
        print(f"Error fetching {searchUrl}: {e}")

def filter_wikiSpecies_gpt():
    url = 'https://species.wikimedia.org/wiki/'
    
    # Reading all lines at once to avoid reading from the file in threads
    with open("WikiSpeciesUnderScore.txt", "r") as fileR:
        lines = fileR.readlines()

    file_lock = Lock()  # Lock to handle file writing in threads

    # Using ThreadPoolExecutor to manage multiple threads
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(fetch_and_filter_species, line, url, file_lock) for line in lines]

        # Ensuring all threads complete their work
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error in thread execution: {e}")

#filter_wikiSpecies()

read_wikiSpecies()
WikiSpeciesUnderScore()
filter_wikiSpecies_gpt()
