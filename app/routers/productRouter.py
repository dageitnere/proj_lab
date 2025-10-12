from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from app.database import get_db
from app.schemas.responses.productBaseResponse import ProductsListResponse
from app.schemas.responses.productsNamesResponse import ProductsNamesResponse
from sqlalchemy.orm import Session
from app.services import productService

showProducts = APIRouter()
productsNames = APIRouter()

# Initialize templates here — no need to import from main.py
templates = Jinja2Templates(directory="app/templates")


@showProducts.get("/showProducts", response_model=ProductsListResponse, response_class=HTMLResponse)
def get_Products(request: Request, db=Depends(get_db)):
    products = productService.getAllProducts(db)
    return templates.TemplateResponse("products.html", {"request": request, "products": products})

@productsNames.get("/productsNames", response_model=ProductsNamesResponse, response_class=JSONResponse)
def get_Products_Names(db: Session = Depends(get_db)):
    return productService.getProductsNames(db)