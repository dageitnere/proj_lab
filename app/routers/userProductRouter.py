from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from app.database import get_db
from app.schemas.requests.addUserProductByNutritionValueRequest import AddUserProductByNutritionValueUrlRequest
from app.schemas.requests.addUserProductByRimiUrlRequest import AddUserProductByRimiUrlRequest
from app.schemas.requests.addUserProductRequest import AddUserProductRequest
from app.services import userProductService
from sqlalchemy.orm import Session
from app.schemas.responses.userProductBaseResponse import UserProductsListResponse
from app.schemas.responses.productsNamesResponse import ProductsNamesResponse
from app.schemas.requests.deleteUserProductRequest import DeleteUserProductRequest
from app.services.userProductService import add_user_product_by_rimi_url, add_user_product_by_nutrition_value_url

userProduct = APIRouter()

# Initialize templates here — no need to import from main.py
templates = Jinja2Templates(directory="app/templates")


@userProduct.get("/getUserProducts/{userUuid}", response_model=UserProductsListResponse, response_class=JSONResponse)
def getUserProducts(userUuid: int, db: Session = Depends(get_db)):
    return userProductService.get_user_products(db, userUuid)

@userProduct.get("/showUserProducts/{userUuid}", response_model=UserProductsListResponse, response_class=HTMLResponse)
def show_User_Products(request: Request, userUuid: int, db=Depends(get_db)):
    products = userProductService.get_user_products(db, userUuid)
    return templates.TemplateResponse("userProducts.html", {"request": request, "products": products})


@userProduct.get("/userProductsNames/{userUuid}", response_model=ProductsNamesResponse, response_class=JSONResponse)
def getUserProductsNames(userUuid: int, db: Session = Depends(get_db)):
    return userProductService.get_user_products_names(db, userUuid)

@userProduct.post("/addUserProduct")
def addUserProduct(request: AddUserProductRequest, db: Session = Depends(get_db)):
    new_product = userProductService.add_user_product(db, request)
    return {
        "status": "success",
        "message": f"Product '{new_product.productName}' added successfully for user {new_product.userUuid}."
    }

@userProduct.post("/addUserProductUrlRimi")
def addUserProductByRimiUrl(request: AddUserProductByRimiUrlRequest, db: Session = Depends(get_db)):
    return add_user_product_by_rimi_url(db, request)

@userProduct.post("/addUserProductUrlNutritionValue")
def addUserProductByNutritionValueUrl(request: AddUserProductByNutritionValueUrlRequest, db: Session = Depends(get_db)):
    return add_user_product_by_nutrition_value_url(db, request)

@userProduct.delete("/deleteUserProduct")
def deleteUserProduct(request: DeleteUserProductRequest, db: Session = Depends(get_db)):
    return userProductService.delete_user_product(db, request)