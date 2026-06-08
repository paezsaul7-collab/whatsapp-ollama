import requests
import json

def consultar_ollama(pregunta):
    url = "http://localhost:11434/api/generate"
    body = {
        "model": "tinyllama",
        "prompt": pregunta,
        "stream": False
    }
    response = requests.post(url, data=json.dumps(body))
    data = response.json()
    return data["response"]