import asyncio
import aiohttp
from bs4 import BeautifulSoup
import json
import os
from tqdm import tqdm
import random
import time

# Lista de User-Agents para alternar
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'
]

# Função para processar a página de forma assíncrona
async def fetch_species_data(session, species_name, semaphore):
    wikipedia_base_url = 'https://en.wikipedia.org/wiki/'
    wikipedia_url = wikipedia_base_url + species_name.replace(" ", "_")
    headers = {
        'User-Agent': random.choice(USER_AGENTS)  # Escolher um User-Agent aleatório
    }

    async with semaphore:
        retries = 5  # Número de tentativas em caso de erro 429
        while retries > 0:
            try:
                async with session.get(wikipedia_url, headers=headers) as response:
                    if response.status == 429:
                        wait_time = random.uniform(5, 15)  # Aguardar de 5 a 15 segundos
                        print(f"Erro 429 para {wikipedia_url}. Aguardando {wait_time:.2f} segundos.")
                        await asyncio.sleep(wait_time)
                        retries -= 1
                        continue
                    # elif response.status != 200:
                    #     print(f"Falha ao obter a página: {wikipedia_url} (Status Code: {response.status})")
                    #     return {species_name: None}

                    unwanted_sections = ['References', 'Gallery', 'Bibliography', 'External links', 'See also', 'Further reading']
                    species_data = {}

                    content = await response.text()

                    # Realiza o parsing em paralelo
                    loop = asyncio.get_running_loop()
                    soup = await loop.run_in_executor(None, lambda: BeautifulSoup(content, 'html.parser'))

                    body_content = soup.find('div', id='bodyContent')
                    if body_content:
                        intro_paragraphs = []
                        for element in body_content.find_all(['p', 'h2', 'h3']):
                            if element.name in ['h2', 'h3']:
                                break
                            if element.name == 'p':
                                intro_paragraphs.append(element.get_text().strip())

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
                                    section_content.append(next_element.get_text().strip())
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
                    return species_data

            except Exception as e:
                print(f"Erro ao obter a página para {species_name}: {e}")
                return {species_name: None}

        # Caso não consiga após todas as tentativas
        return {species_name: None}


# Função principal para processar múltiplos arquivos com scraping
async def process_files(files):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for file_num, (input_file, output_file) in enumerate(files, start=5):
            base_dir = "C:/Users/estev/Documents/GitHub/MEIC-PRI/Web-scrapping"
            input_file = os.path.join(base_dir, input_file)
            output_file = os.path.join(base_dir, "JsonParts", output_file)

            # Lê a lista de espécies
            with open(input_file, "r", encoding="utf-8") as fileR:
                species_list = [line.strip().replace("_", " ") for line in fileR]

            species_data = {}
            semaphore = asyncio.Semaphore(5)  # Reduz o número de requisições simultâneas

            tasks_for_file = [fetch_species_data(session, species_name, semaphore) for species_name in species_list]
            tasks.append((tasks_for_file, output_file, species_data))

        # Processamento simultâneo de todos os arquivos
        for tasks_for_file, output_file, species_data in tasks:
            # Usa tqdm para mostrar o progresso
            for future in tqdm(asyncio.as_completed(tasks_for_file), total=len(tasks_for_file), desc=f"Processing file {output_file}"):
                result = await future
                species_data.update(result)

            # Salva os resultados em um arquivo JSON
            with open(output_file, "w", encoding="utf-8") as json_file:
                json.dump(species_data, json_file, ensure_ascii=False, indent=4)

            # Pausa aleatória entre lotes de arquivos para evitar sobrecarga
            time.sleep(random.uniform(2.0, 5.0))  # Aumenta a pausa entre arquivos


# Executa a função principal
files_to_process = [
    ("wikiPart5.txt", "Species_data5.json"),
    ("wikiPart6.txt", "Species_data6.json"),
    ("wikiPart7.txt", "Species_data7.json"),
    ("wikiPart8.txt", "Species_data8.json"),
]

asyncio.run(process_files(files_to_process))
