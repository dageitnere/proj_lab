from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from app.database import get_db
from app.dependencies.getUserUuidFromToken import get_uuid_from_token
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


@userProduct.get("/getUserProducts", response_model=UserProductsListResponse, response_class=JSONResponse)
def getUserProducts(userUuid: int = Depends(get_uuid_from_token), db: Session = Depends(get_db)):
    return userProductService.get_user_products(db, userUuid)

@userProduct.get("/showUserProducts", response_model=UserProductsListResponse, response_class=HTMLResponse)
def showUserProducts(request: Request, userUuid: int = Depends(get_uuid_from_token), db=Depends(get_db)):
    products = userProductService.get_user_products(db, userUuid)
    return templates.TemplateResponse("userProducts.html", {"request": request, "products": products})


@userProduct.get("/userProductsNames", response_model=ProductsNamesResponse, response_class=JSONResponse)
def getUserProductsNames(userUuid: int = Depends(get_uuid_from_token), db: Session = Depends(get_db)):
    return userProductService.get_user_products_names(db, userUuid)

@userProduct.post("/addUserProduct")
def addUserProduct(request: AddUserProductRequest, userUuid: int = Depends(get_uuid_from_token), db: Session = Depends(get_db)):
    new_product = userProductService.add_user_product(db, request, userUuid)
    return {
        "status": "success",
        "message": f"Product '{new_product.productName}' added successfully."
    }

@userProduct.post("/addUserProductUrlRimi")
def addUserProductByRimiUrl(request: AddUserProductByRimiUrlRequest, userUuid: int = Depends(get_uuid_from_token), db: Session = Depends(get_db)):
    return add_user_product_by_rimi_url(db, request, userUuid)

@userProduct.post("/addUserProductUrlNutritionValue")
def addUserProductByNutritionValueUrl(request: AddUserProductByNutritionValueUrlRequest, userUuid: int = Depends(get_uuid_from_token), db: Session = Depends(get_db)):
    return add_user_product_by_nutrition_value_url(db, request, userUuid)

@userProduct.delete("/deleteUserProduct")
def deleteUserProduct(request: DeleteUserProductRequest, userUuid: int = Depends(get_uuid_from_token), db: Session = Depends(get_db)):
    return userProductService.delete_user_product(db, request, userUuid)