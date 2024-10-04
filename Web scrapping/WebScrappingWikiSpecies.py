from lxml import html
import requests

# Text file because json is only for the data according to the wikipedia
file = open("WikiSpecies.txt","w")
nextPage = True
url = 'https://species.wikimedia.org/w/index.php?title=Special:AllPages&from=A+History+of+British+Ferns'

while(nextPage):
    response = requests.get(url)

    tree = html.fromstring(response.content)
    link_titles = tree.xpath('//ul[@class="mw-allpages-chunk"]//li/a/@title')

    next_page_link = tree.xpath('//a[contains(text(),"Next page")]/@href')

    # if next_page_link:
    next_page_url = 'https://species.wikimedia.org' + next_page_link[0]

    for title in link_titles:
        file.write(title)
        file.write("\n")
        print(title)

    print("ola")
    print(next_page_url)
    
    # Changes url if next page exists, otherwise, changes the var to false
    nextPage = False

file.close()
# Need to find the next element in the end of the page, that allows me to create a new URL
