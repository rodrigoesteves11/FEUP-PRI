import concurrent.futures
from bs4 import BeautifulSoup
import json
import requests
import re

def fetch_species_data(species_name):
    wikipedia_base_url = 'https://en.wikipedia.org/wiki/'
    wikipedia_url = wikipedia_base_url + species_name.replace(" ", "_")
    
    response = requests.get(wikipedia_url)
    
    unwanted_sections = ['References', 'Gallery', 'Bibliography', 'External links', 'See also', 'Further reading']
    species_data = {}
    
    if response.status_code == 200:
        print(f"Página encontrada: {wikipedia_url}")
        soup = BeautifulSoup(response.content, 'html.parser')
        body_content = soup.find('div', id='bodyContent')
        if body_content:
            intro_paragraphs = []
            first_heading_found = False
            for element in body_content.find_all(['p', 'h2', 'h3']):
                if element.name in ['h2', 'h3']:
                    first_heading_found = True
                    break
                if element.name == 'p':
                    clean_text = re.sub(r'\[\d+\]', '', element.get_text().strip())
                    intro_paragraphs.append(clean_text)
                    
            introduction = '\n\n'.join(intro_paragraphs)
            
            sections = {}
            for header in body_content.find_all(['h2', 'h3']):
                section_title = header.get_text().strip().replace('[edit]', '')
                if any(unwanted in section_title for unwanted in unwanted_sections):
                    continue
                section_content = []
                next_element = header.find_next()
                while next_element:
                    if next_element.name in ['h2', 'h3']:
                        break
                    if next_element.name == 'p':
                        clean_text = re.sub(r'\[\d+\]', '', next_element.get_text().strip())
                        section_content.append(clean_text)
                    next_element = next_element.find_next()
                    
                if section_content:
                    sections[section_title] = '\n\n'.join(section_content)
                    
            infobox = body_content.find('table', {'class': 'infobox'})
            scientific_classification = {}
            who_discovered = "Not found"
            if infobox:
                image_tags = infobox.find_all('img')
                rows = infobox.find_all('tr')
                is_taxonomy_section = False
                is_binomial_name = False
                for row in rows:
                    th = row.find('a')
                    td = row.find('td')
                    if th and "Binomial name" in th.text:
                        is_taxonomy_section = False
                        is_binomial_name = True
                        continue
                    if th and "Scientific classification" in th.text:
                        is_taxonomy_section = True
                    if is_taxonomy_section and th and td:
                        classification_key = td.text.strip().replace(":", "")
                        classification_value = th.text.strip()
                        scientific_classification[classification_key] = classification_value
                    if is_binomial_name and th:
                        who_discovered = th.text.strip()
                        is_binomial_name = False
                
                scientific_classification['Species'] = species_name
                
                if len(image_tags) > 0:
                    image_url = "https:" + image_tags[0]['src']
                    print(f"Imagem encontrada: {image_url}")
                else:
                    image_url = "No image found in infobox"
            else:
                image_url = "No infobox found"
        else:
            introduction = "No body content found"
            sections = "No body content found"
            image_url = "No body content found"
            who_discovered = "No body content found"
            scientific_classification = "No body content found"
                    
        species_data[species_name] = {
            "introduction": introduction,
            "sections": sections,
            "scientific_classification": scientific_classification,
            "who_discovered": who_discovered,
            "image_url": image_url
        }
    else:
        print(f"Falha ao obter a página: {wikipedia_url} (Status Code: {response.status_code})")

    return species_data

def get_wikipedia_pages():
    with open("WikiTXT/wikiPart8.txt", "r") as fileR: #HERE
        species_list = [line.strip().replace("_", " ") for line in fileR]

    species_data = {}

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(fetch_species_data, species_list)

    for result in results:
        species_data.update(result)

    with open("JsonParts/Species_data8.json", "w", encoding="utf-8") as json_file: #HERE
        json.dump(species_data, json_file, ensure_ascii=False, indent=4)

get_wikipedia_pages()
