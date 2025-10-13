from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.requests.userConsumedProductRequest import UserConsumedProductRequest
from app.schemas.responses.userConsumedProductResponse import  UserConsumedProductListResponse
from app.services.consumedProductService import add_consumed_product, get_all_consumed_products, get_consumed_today, get_consumed_last_7_days, get_consumed_last_30_days

consumedProduct = APIRouter()

@consumedProduct.post("/saveConsumedProduct")
def addConsumedProduct(data: UserConsumedProductRequest, db: Session = Depends(get_db)):
    return add_consumed_product(db, data)

@consumedProduct.get("/all/{user_uuid}", response_model=UserConsumedProductListResponse)
def getAllConsumedProducts(user_uuid: int, db: Session = Depends(get_db)):
    return get_all_consumed_products(db, user_uuid)


@consumedProduct.get("/today/{user_uuid}", response_model=UserConsumedProductListResponse)
def getConsumedToday(user_uuid: int, db: Session = Depends(get_db)):
    return get_consumed_today(db, user_uuid)


@consumedProduct.get("/last7days/{user_uuid}", response_model=UserConsumedProductListResponse)
def getCOnsumedLast7Days(user_uuid: int, db: Session = Depends(get_db)):
    return get_consumed_last_7_days(db, user_uuid)


@consumedProduct.get("/last30days/{user_uuid}", response_model=UserConsumedProductListResponse)
def getConsumedLast30Days(user_uuid: int, db: Session = Depends(get_db)):
    return get_consumed_last_30_days(db, user_uuid)