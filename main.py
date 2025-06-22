from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
import requests
from bs4 import BeautifulSoup
import urllib.parse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/outline", response_class=PlainTextResponse)
def get_outline(country: str = Query(...)):
    try:
        encoded_country = urllib.parse.quote(country.strip())
        url = f"https://en.wikipedia.org/wiki/{encoded_country}"
        response = requests.get(url)
        if response.status_code != 200:
            return f"Failed to fetch Wikipedia page for '{country}'"
        soup = BeautifulSoup(response.text, "html.parser")
        headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
        markdown = "## Contents\n\n"
        for tag in headings:
            level = int(tag.name[1])
            text = tag.get_text().strip()
            if text and "edit" not in text.lower():
                markdown += f"{'#' * level} {text}\n\n"
        return markdown
    except Exception as e:
        return f"Error: {str(e)}"
