from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.algorithmService import generate_diet_plan
from app.schemas.dietRequest import DietRequest

showMainPage = APIRouter()

# Initialize templates here — no need to import from main.py
templates = Jinja2Templates(directory="app/templates")

@showMainPage.get("/mainPage", response_class=HTMLResponse)
def get_main(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})