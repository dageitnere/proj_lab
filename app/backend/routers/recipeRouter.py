from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from app.backend.database import get_db
from app.backend.dependencies.getUserUuidFromToken import get_uuid_from_token
from app.backend.services.recipeService import get_recipes_by_menu, regenerate_menu_recipes, delete_recipes_batch
from app.backend.schemas.responses.recipeResponse import GenerateRecipesResponse
from app.backend.schemas.requests.getRecipeRequest import RegenerateRecipesRequest, DeleteRecipesBatchRequest

recipes = APIRouter()

@recipes.get("/{menuId}", response_model=GenerateRecipesResponse, response_class=JSONResponse)
def getRecipesByMenu(menuId: int, userUuid: int = Depends(get_uuid_from_token), db: Session = Depends(get_db)):
    return get_recipes_by_menu(db, userUuid, menuId)

@recipes.post("/regenerate", response_model=GenerateRecipesResponse, response_class=JSONResponse)
def regenerateMenuRecipes(request: RegenerateRecipesRequest, userUuid: int = Depends(get_uuid_from_token), db: Session = Depends(get_db)):
    return regenerate_menu_recipes(db, userUuid, request.menuId)

@recipes.delete("/batch", response_class=JSONResponse)
def deleteRecipesBatch(request: DeleteRecipesBatchRequest, userUuid: int = Depends(get_uuid_from_token), db: Session = Depends(get_db)):
    return delete_recipes_batch(db, userUuid, request.menuId, request.batchId)