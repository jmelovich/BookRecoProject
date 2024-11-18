import requests
import json

global API_KEY
API_KEY = "your-api-key"

def get_text_embedding(input_text):
    url = "https://api.openai.com/v1/embeddings"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    data = {
        "input": input_text,
        "model": "text-embedding-3-small"
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        embedding = response.json().get('data')[0].get('embedding')
        return embedding
    else:
        response.raise_for_status()
        
