from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from app.database import get_db
from app.dependencies.getUserUuidFromToken import get_uuid_from_token
from app.services.recipeService import get_recipes_by_menu
from app.schemas.responses.recipeResponse import GenerateRecipesResponse

recipes = APIRouter()

@recipes.get("/{menuId}", response_model=GenerateRecipesResponse, response_class=JSONResponse)
def getRecipesByMenu(menuId: int, userUuid: int = Depends(get_uuid_from_token), db: Session = Depends(get_db)):
    return get_recipes_by_menu(db, userUuid, menuId)


'''
@recipes.post("/generateRecipes", response_model=GenerateRecipesResponse)
def generate_recipes(request: GenerateRecipesRequest, db: Session = Depends(get_db)):
    return create_recipes_from_menu(db, request.userMenuId, request.products)
'''
# TODO receptes pārģenerēšana