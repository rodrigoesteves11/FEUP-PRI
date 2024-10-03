import requests
from bs4 import BeautifulSoup

r = requests.get('https://species.wikimedia.org/w/index.php?title=Special:AllPages&from=A+History+of+British+Ferns')

# Prints sucess code
print(r)

# Parsing the HTML
soup = BeautifulSoup(r.content, 'html.parser')

entriesChunk = soup.find('ul', class_='mw-allpages-chunk')

for element in entriesChunk:
    print(element)



#Entry example:
# 
#  <li><a href="/wiki/Abacetus_bequaerti" title="Abacetus bequaerti">Abacetus bequaerti</a></li>

# Need to find the next element in the end of the page, that allows me to create a new URL



