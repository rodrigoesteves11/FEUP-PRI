import requests
from sentence_transformers import SentenceTransformer

def text_to_embedding(text):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embedding = model.encode(text, convert_to_tensor=False).tolist()
    
    # Convert the embedding to the expected format
    embedding_str = "[" + ",".join(map(str, embedding)) + "]"
    return embedding_str

def solr_combined_query(endpoint, collection, query_text, embedding):
    url = f"{endpoint}/{collection}/select"

    # Combine edismax query and KNN vector search
    data = {
        "q": f"{query_text}",
        "fq": f"{{!knn f=vector topK=60}}{embedding}",  # Filter query to include KNN search
        "defType": "edismax",
        "qf": "introduction^5 sections^6 kingdom^2",
        "pf": "introduction^4 sections^3",
        "ps": 6,
        "qs": 2,
        "tie": 0.5,
        "bq": "kingdom:Animalia^2",
        "rows": 300,
        "fl": "id, name, kingdom, introduction, sections, score",
        "wt": "json"
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(url, data=data, headers=headers)
    response.raise_for_status()
    return response.json()

def save_results_as_trec(results, output_file, run_id="run0"):
    try:
        docs = results.get("response", {}).get("docs", [])

        if not docs:
            print("No results found.")
            return

        with open(output_file, "w") as f:
            for rank, doc in enumerate(docs, start=1):
                line = f"0 Q0 {doc['id']} {rank} {doc['score']} {run_id}\n"
                f.write(line)
    except KeyError:
        print("Error: Invalid Solr response format. 'docs' key not found.")
        return

def main():
    solr_endpoint = "http://localhost:8983/solr"
    collection = "semantic"

    query_text = "(largest^2 huge^2 size) AND animal"
    user_query = "Large and Huge sized animal"
    embedding = text_to_embedding(user_query)
    output_file = "results_trec.txt"

    try:
        results = solr_combined_query(solr_endpoint, collection, query_text, embedding)
        save_results_as_trec(results, output_file)
        print(f"Results saved to {output_file}")
    except requests.HTTPError as e:
        print(f"Error {e.response.status_code}: {e.response.text}")

if __name__ == "__main__":
    main()