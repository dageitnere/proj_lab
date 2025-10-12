from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

showMainPage = APIRouter()

# Initialize templates here — no need to import from main.py
templates = Jinja2Templates(directory="app/templates")

@showMainPage.get("/mainPage", response_class=HTMLResponse)
def get_main(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})