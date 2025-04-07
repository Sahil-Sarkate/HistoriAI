import os
import requests
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

import requests

def generate_gpt_answer(query: str):
    try:
        headers = {
            "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:3000",  # Change to your domain if deployed
        }

        data = {
            "model": "mistralai/mixtral-8x7b",  # You can change to "openai/gpt-3.5-turbo" or others
            "messages": [
                {"role": "user", "content": query}
            ]
        }

        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")


def search_wikimedia_image(query: str):
    try:
        search_url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "prop": "pageimages",
            "format": "json",
            "titles": query,
            "pithumbsize": 500
        }
        response = requests.get(search_url, params=params).json()
        pages = response.get("query", {}).get("pages", {})
        for page in pages.values():
            if "thumbnail" in page:
                return page["thumbnail"]["source"]
        return None
    except Exception as e:
        print("Wikimedia error:", e)
        return None


def search_pixabay_image(query: str):
    try:
        key = os.getenv("PIXABAY_API_KEY")
        url = f"https://pixabay.com/api/?key={key}&q={query}&image_type=photo"
        response = requests.get(url).json()
        hits = response.get("hits", [])
        if hits:
            return hits[0]["webformatURL"]
        return None
    except Exception as e:
        print("Pixabay error:", e)
        return None


def get_answer_and_image(query: str):
    try:
        answer = generate_gpt_answer(query)
        image_url = search_wikimedia_image(query) or search_pixabay_image(query)
        return {"answer": answer, "image_url": image_url or ""}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {e}")
