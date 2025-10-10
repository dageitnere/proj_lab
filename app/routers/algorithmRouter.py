from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.algorithmService import generate_diet_plan
from app.schemas.dietRequest import DietRequest

router = APIRouter()

@router.post("/menu/generate")
def generate_menu(request: DietRequest, db: Session = Depends(get_db)):
    # just pass the whole request to service
    return generate_diet_plan(db, request)
