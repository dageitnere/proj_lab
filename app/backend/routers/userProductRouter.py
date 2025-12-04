from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse, JSONResponse
from app.backend.database import get_db
from app.backend.dependencies.getUserUuidFromToken import get_uuid_from_token
from app.backend.schemas.requests.postUserProductByNutritionValueRequest import PostUserProductByNutritionValueUrlRequest
from app.backend.schemas.requests.postUserProductByRimiUrlRequest import PostUserProductByRimiUrlRequest
from app.backend.schemas.requests.postUserProductRequest import PostUserProductRequest
from app.backend.schemas.requests.updateUserProductRequest import UpdateUserProductRequest
from app.backend.schemas.responses.userProductBaseResponse import UserProductsListResponse
from app.backend.schemas.responses.productsNamesResponse import ProductsNamesResponse
from app.backend.schemas.requests.deleteUserProductRequest import DeleteUserProductRequest
from app.backend.services.userProductService import add_user_product_by_rimi_url, add_user_product_by_nutrition_value_url, update_user_product, \
    get_user_products, get_user_products_names, add_user_product, delete_user_product

userProduct = APIRouter()

templates = Jinja2Templates(directory="app/frontend/templates")

@userProduct.get("/showUserProducts", response_model=UserProductsListResponse, response_class=HTMLResponse)
def showUserProductsPage(request: Request, userUuid: int = Depends(get_uuid_from_token), db=Depends(get_db)):
    products = get_user_products(db, userUuid)
    return templates.TemplateResponse("userProducts.html", {"request": request, "products": products})

@userProduct.get("/getUserProducts", response_model=UserProductsListResponse, response_class=JSONResponse)
def getUserProducts(userUuid: int = Depends(get_uuid_from_token), db: Session = Depends(get_db)):
    return get_user_products(db, userUuid)

@userProduct.get("/userProductsNames", response_model=ProductsNamesResponse, response_class=JSONResponse)
def getUserProductsNames(userUuid: int = Depends(get_uuid_from_token), db: Session = Depends(get_db)):
    return get_user_products_names(db, userUuid)

@userProduct.post("/addUserProduct")
def addUserProduct(request: PostUserProductRequest, userUuid: int = Depends(get_uuid_from_token), db: Session = Depends(get_db)):
    return add_user_product(db, request, userUuid)

@userProduct.post("/addUserProductUrlRimi")
def addUserProductByRimiUrl(request: PostUserProductByRimiUrlRequest, userUuid: int = Depends(get_uuid_from_token), db: Session = Depends(get_db)):
    return add_user_product_by_rimi_url(db, request, userUuid)

@userProduct.post("/addUserProductUrlNutritionValue")
def addUserProductByNutritionValueUrl(request: PostUserProductByNutritionValueUrlRequest, userUuid: int = Depends(get_uuid_from_token), db: Session = Depends(get_db)):
    return add_user_product_by_nutrition_value_url(db, request, userUuid)

@userProduct.delete("/deleteUserProduct")
def deleteUserProduct(request: DeleteUserProductRequest, userUuid: int = Depends(get_uuid_from_token), db: Session = Depends(get_db)):
    return delete_user_product(db, request, userUuid)


@userProduct.put("/updateUserProduct")
def update_user_product_endpoint(request: UpdateUserProductRequest, db: Session = Depends(get_db), user_uuid: int = Depends(get_uuid_from_token)):
    return update_user_product(db, request, user_uuid)