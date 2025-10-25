from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies.getUserUuidFromToken import get_uuid_from_token
from app.schemas.requests.postDietPlanRequest import PostDietPlanRequest
from app.schemas.requests.deleteUserMenuRequest import DeleteUserMenuRequest
from app.schemas.requests.getMenuRequest import GetMenuRequest
from app.schemas.requests.dietRequest import DietRequest
from app.schemas.responses.generateMenuResponse import GenerateMenuResponse
from app.schemas.responses.dietPlanResponse import DietPlanListResponse, DietPlanResponse
from app.services.menuService import generate_diet_menu, save_diet_menu, get_user_menus, get_single_menu, delete_user_menu

templates = Jinja2Templates(directory="app/templates")

menu = APIRouter()

@menu.post("/generateMenu", response_model=GenerateMenuResponse, response_class=JSONResponse)
def generate_Menu(request: DietRequest, userUuid: int = Depends(get_uuid_from_token), db: Session = Depends(get_db)):
    # just pass the whole request to service
    return generate_diet_menu(db, request, userUuid)

@menu.get("/form", response_class=HTMLResponse)
def showMenuForm(request: Request):
    return templates.TemplateResponse("menuForm.html", {"request": request})

@menu.get("/userMenuForm", response_class=HTMLResponse)
def showUserMenuForm(request: Request):
    return templates.TemplateResponse("userMenuForm.html", {"request": request})

@menu.post("/saveMenu")
def saveDietMenu(request: PostDietPlanRequest, userUuid: int = Depends(get_uuid_from_token), db: Session = Depends(get_db)):
    return save_diet_menu(db, request, userUuid)

@menu.get("/getUserMenus", response_model=DietPlanListResponse)
def getUserMenus(userUuid: int = Depends(get_uuid_from_token), db: Session = Depends(get_db)):
    return get_user_menus(db, userUuid)

@menu.post("/getUserMenu", response_model=DietPlanResponse)
def getSingleMenu(request: GetMenuRequest, userUuid: int = Depends(get_uuid_from_token), db: Session = Depends(get_db)):
    return get_single_menu(db, request, userUuid)

@menu.delete("/deleteMenu")
def deleteMenu(request: DeleteUserMenuRequest, userUuid: int = Depends(get_uuid_from_token), db: Session = Depends(get_db)):
    return delete_user_menu(db, request, userUuid)