from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.requests.deleteConsumedProductRequest import DeleteConsumedProductRequest
from app.schemas.requests.addUserConsumedProductRequest import AddUserConsumedProductRequest
from app.schemas.requests.getConsumedProductByDateRequest import GetConsumedProductByDateRequest
from app.schemas.responses.userConsumedProductResponse import UserConsumedProductListResponse
from app.services.consumedProductService import add_consumed_product, get_all_consumed_products, get_consumed_today, get_consumed_last_7_days, get_consumed_last_30_days, delete_consumed_product, get_consumed_by_date
from app.dependencies.getUserUuidFromToken import get_uuid_from_token
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")

consumedProduct = APIRouter()

@consumedProduct.get("/form")
def showConsumedProductPage(request: Request):
    return templates.TemplateResponse("consumedProducts.html", {"request": request})

@consumedProduct.post("/saveConsumedProduct")
def addConsumedProduct(request: AddUserConsumedProductRequest, userUuid: int = Depends(get_uuid_from_token), db: Session = Depends(get_db)):
    return add_consumed_product(db, request, userUuid)

@consumedProduct.get("/all", response_model=UserConsumedProductListResponse)
def getAllConsumedProducts(userUuid: int = Depends(get_uuid_from_token), db: Session = Depends(get_db)):
    return get_all_consumed_products(db, userUuid)


@consumedProduct.get("/today", response_model=UserConsumedProductListResponse)
def getConsumedToday(userUuid: int = Depends(get_uuid_from_token), db: Session = Depends(get_db)):
    return get_consumed_today(db, userUuid)


@consumedProduct.get("/last7days", response_model=UserConsumedProductListResponse)
def getConsumedLast7Days(userUuid: int = Depends(get_uuid_from_token), db: Session = Depends(get_db)):
    return get_consumed_last_7_days(db, userUuid)


@consumedProduct.get("/last30days", response_model=UserConsumedProductListResponse)
def getConsumedLast30Days(userUuid: int = Depends(get_uuid_from_token), db: Session = Depends(get_db)):
    return get_consumed_last_30_days(db, userUuid)

@consumedProduct.delete("/deleteProduct")
def deleteConsumedProduct(request: DeleteConsumedProductRequest, db: Session = Depends(get_db)):
    return delete_consumed_product(db, request)

@consumedProduct.post("/byDate")
def getConsumedByDate(request: GetConsumedProductByDateRequest, userUuid: int = Depends(get_uuid_from_token), db: Session = Depends(get_db)):
    return get_consumed_by_date(db, request, userUuid)