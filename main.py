from fastapi import FastAPI, Request, Form
from typing import List
import requests
from bs4 import BeautifulSoup
from googletrans import Translator
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="")


class URLList(BaseModel):
    urls: List[str]


@app.get("/")
async def read_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/translate", response_class=HTMLResponse)
async def translate_urls(request: Request, urls: str = Form(...)):
    results = []
    translator = Translator(service_urls=['translate.googleapis.com'])

    urls = urls.strip().split('\n')
    for url in urls:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        text = soup.get_text()
        translated_text = translator.translate(text, dest='hi').text
        translated_url = f'https://translate.google.com/translate?sl=auto&tl=hi&u=%7Burl%7D'
        result = {'url': url, 'translated_url': translated_url, 'content': translated_text}
        results.append(result)

    template = templates.get_template("index.html")
    return template.render(request=request, results=results)
