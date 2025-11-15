from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

mainPage = APIRouter()

# Initialize templates
templates = Jinja2Templates(directory="app/frontend/templates")

@mainPage.get("/mainPage", response_class=HTMLResponse)
def getMainPage(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})