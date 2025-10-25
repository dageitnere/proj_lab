from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse, JSONResponse
from app.database import get_db
from app.dependencies.getUserUuidFromToken import get_uuid_from_token
from app.schemas.requests.postUserProductByNutritionValueRequest import PostUserProductByNutritionValueUrlRequest
from app.schemas.requests.postUserProductByRimiUrlRequest import PostUserProductByRimiUrlRequest
from app.schemas.requests.postUserProductRequest import PostUserProductRequest
from app.schemas.requests.updateUserProductRequest import UpdateUserProductRequest
from app.schemas.responses.userProductBaseResponse import UserProductsListResponse
from app.schemas.responses.productsNamesResponse import ProductsNamesResponse
from app.schemas.requests.deleteUserProductRequest import DeleteUserProductRequest
from app.services.userProductService import add_user_product_by_rimi_url, add_user_product_by_nutrition_value_url, update_user_product
from app.services import userProductService

userProduct = APIRouter()

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
def addUserProduct(request: PostUserProductRequest, userUuid: int = Depends(get_uuid_from_token), db: Session = Depends(get_db)):
    new_product = userProductService.add_user_product(db, request, userUuid)
    return {
        "status": "success",
        "message": f"Product '{new_product.productName}' added successfully."
    }

@userProduct.post("/addUserProductUrlRimi")
def addUserProductByRimiUrl(request: PostUserProductByRimiUrlRequest, userUuid: int = Depends(get_uuid_from_token), db: Session = Depends(get_db)):
    return add_user_product_by_rimi_url(db, request, userUuid)

@userProduct.post("/addUserProductUrlNutritionValue")
def addUserProductByNutritionValueUrl(request: PostUserProductByNutritionValueUrlRequest, userUuid: int = Depends(get_uuid_from_token), db: Session = Depends(get_db)):
    return add_user_product_by_nutrition_value_url(db, request, userUuid)

@userProduct.delete("/deleteUserProduct")
def deleteUserProduct(request: DeleteUserProductRequest, userUuid: int = Depends(get_uuid_from_token), db: Session = Depends(get_db)):
    return userProductService.delete_user_product(db, request, userUuid)


@userProduct.put("/updateUserProduct")
def update_user_product_endpoint(request: UpdateUserProductRequest, db: Session = Depends(get_db), user_uuid: int = Depends(get_uuid_from_token)):
    return update_user_product(db, request, user_uuid)