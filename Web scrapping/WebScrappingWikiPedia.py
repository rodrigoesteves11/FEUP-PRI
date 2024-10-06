from bs4 import BeautifulSoup
import json
import requests


def get_wikipedia_pages():
   
    wikipedia_base_url = 'https://en.wikipedia.org/wiki/'
    fileR = open("testSample.txt", "r")

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

get_wikipedia_pages()

