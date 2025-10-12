from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.algorithmService import generate_diet_plan
from app.schemas.requests.dietRequest import DietRequest
from app.schemas.responses.generateMenuResponse import GenerateMenuResponse

templates = Jinja2Templates(directory="app/templates")

generateMenu = APIRouter()
showMenuForm = APIRouter()

@generateMenu.post("/generateMenu", response_model=GenerateMenuResponse, response_class=JSONResponse)
def generate_Menu(request: DietRequest, db: Session = Depends(get_db)):
    # just pass the whole request to service
    return generate_diet_plan(db, request)

@showMenuForm.get("/form", response_class=HTMLResponse)
def show_Menu_Form(request: Request):
    return templates.TemplateResponse("menuForm.html", {"request": request})