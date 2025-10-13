from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

mainPage = APIRouter()

# Initialize templates here — no need to import from main.py
templates = Jinja2Templates(directory="app/templates")

@mainPage.get("/mainPage", response_class=HTMLResponse)
def getMainPage(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})