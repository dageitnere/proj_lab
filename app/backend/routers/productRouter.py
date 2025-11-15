from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from app.backend.database import get_db
from app.backend.schemas.responses.productBaseResponse import ProductsListResponse
from app.backend.schemas.responses.productsNamesResponse import ProductsNamesResponse
from sqlalchemy.orm import Session
from app.backend.services import productService

product = APIRouter()

templates = Jinja2Templates(directory="app/frontend/templates")

@product.get("/showProducts", response_model=ProductsListResponse, response_class=HTMLResponse)
def getAllProducts(request: Request, db=Depends(get_db)):
    products = productService.get_all_products(db)
    return templates.TemplateResponse("products.html", {"request": request, "products": products})

@product.get("/productsNames", response_model=ProductsNamesResponse, response_class=JSONResponse)
def getProductsNames(db: Session = Depends(get_db)):
    return productService.get_products_names(db)