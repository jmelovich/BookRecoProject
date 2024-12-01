import requests
import json
import time

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
    
    backoff_time = 5  # initial backoff time in seconds
    
    while True:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        
        if response.status_code == 200:
            embedding = response.json().get('data')[0].get('embedding')
            return embedding
        else:
            print(f"Request failed with status code {response.status_code}. Retrying in {backoff_time} seconds...")
            time.sleep(backoff_time)
            backoff_time = min(backoff_time * 2, 320)  # exponential backoff with a cap at 320 seconds