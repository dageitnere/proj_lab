from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from app.database import get_db
from app.dependencies.getUserUuidFromToken import get_uuid_from_token
from app.services.recipeService import get_recipes_by_menu, regenerate_recipes_for_menu, delete_recipes_batch
from app.schemas.responses.recipeResponse import GenerateRecipesResponse
from app.schemas.requests.getRecipeRequest import RegenerateRecipesRequest, DeleteRecipesBatchRequest

recipes = APIRouter()

@recipes.get("/{menuId}", response_model=GenerateRecipesResponse, response_class=JSONResponse)
def getRecipesByMenu(menuId: int, userUuid: int = Depends(get_uuid_from_token), db: Session = Depends(get_db)):
    return get_recipes_by_menu(db, userUuid, menuId)

@recipes.post("/regenerate", response_model=GenerateRecipesResponse, response_class=JSONResponse)
def regenerateMenuRecipes(request: RegenerateRecipesRequest, userUuid: int = Depends(get_uuid_from_token), db: Session = Depends(get_db)):
    return regenerate_recipes_for_menu(db, userUuid, request.menuId)

@recipes.delete("/batch", response_class=JSONResponse)
def deleteRecipesBatch(request: DeleteRecipesBatchRequest, userUuid: int = Depends(get_uuid_from_token), db: Session = Depends(get_db)):
    return delete_recipes_batch(db, userUuid, request.menuId, request.batchId)