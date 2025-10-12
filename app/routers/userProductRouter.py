from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from app.database import get_db
from app.schemas.requests.addUserProductRequest import AddUserProductRequest
from app.services import userProductService
from sqlalchemy.orm import Session
from app.schemas.responses.userProductBaseResponse import UserProductsListResponse
from app.schemas.responses.productsNamesResponse import ProductsNamesResponse

showUserProducts = APIRouter()
userProductsNames = APIRouter()
addUserProduct = APIRouter()

# Initialize templates here — no need to import from main.py
templates = Jinja2Templates(directory="app/templates")


@showUserProducts.get("/showUserProducts/{userUuid}", response_model=UserProductsListResponse, response_class=HTMLResponse)
def get_Products(request: Request, userUuid: int, db=Depends(get_db)):
    products = userProductService.getAllUserProducts(db, userUuid)
    return templates.TemplateResponse("userProducts.html", {"request": request, "products": products})


@userProductsNames.get("/userProductsNames/{userUuid}", response_model=ProductsNamesResponse, response_class=JSONResponse)
def get_Products_Names(userUuid: int, db: Session = Depends(get_db)):
    return userProductService.getUserProductsNames(db, userUuid)

@addUserProduct.post("/addUserProduct/{userUuid}")
def add_user_product_route(userUuid: int, product: AddUserProductRequest, db: Session = Depends(get_db)):
    new_product = userProductService.add_user_product(db, userUuid, product)
    return {
        "status": "success",
        "product_id": new_product.id,
        "message": f"Product '{new_product.produkts}' added successfully for user {userUuid}"
    }