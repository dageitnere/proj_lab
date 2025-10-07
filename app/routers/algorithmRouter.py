from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.algorithmService import generate_diet_plan
from app.schemas.dietRequest import DietRequest

router = APIRouter()

@router.post("/menu/generate")
def generate_menu(request: DietRequest, db: Session = Depends(get_db)):
    result = generate_diet_plan(
        db,
        request.kcal,
        request.protein,
        request.fat,
        request.satFat,
        request.carbs,
        request.sugars,
        request.salt,
        request.restrictions
    )
    return result
