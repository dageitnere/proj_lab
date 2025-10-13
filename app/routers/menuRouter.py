from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.requests.dietPlanSaveRequest import DietPlanSaveRequest
from app.schemas.responses.dietPlanResponse import DietPlanListResponse, DietPlanResponse
from app.services.menuService import generate_diet_menu
from app.services.menuService import save_user_diet_menu
from app.services.menuService import get_all_user_menus
from app.services.menuService import get_single_plan
from app.schemas.requests.dietRequest import DietRequest
from app.schemas.responses.generateMenuResponse import GenerateMenuResponse

templates = Jinja2Templates(directory="app/templates")

generateMenu = APIRouter()
showMenuForm = APIRouter()
saveMenu = APIRouter()
getUserMenus = APIRouter()
getSingleUserMenu = APIRouter()

@generateMenu.post("/generateMenu", response_model=GenerateMenuResponse, response_class=JSONResponse)
def generate_Menu(request: DietRequest, db: Session = Depends(get_db)):
    # just pass the whole request to service
    return generate_diet_menu(db, request)

@showMenuForm.get("/form", response_class=HTMLResponse)
def show_Menu_Form(request: Request):
    return templates.TemplateResponse("menuForm.html", {"request": request})

@saveMenu.post("/saveMenu")
def save_diet_menu(plan: DietPlanSaveRequest, db: Session = Depends(get_db)):
    return save_user_diet_menu(db, plan)

@getUserMenus.get("/getUserMenus/{userUuid}", response_model=DietPlanListResponse)
def get_user_menus(userUuid: int, db: Session = Depends(get_db)):
    return get_all_user_menus(db, userUuid)

@getSingleUserMenu.get("/getUserMenu/{menuName}", response_model=DietPlanResponse)
def get_single_menu_route(menuName: str, db: Session = Depends(get_db)):
    return get_single_plan(db, menuName)