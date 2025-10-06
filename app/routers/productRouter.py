from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.database import get_db
from app.services import productService
router = APIRouter()

# Initialize templates here — no need to import from main.py
templates = Jinja2Templates(directory="app/templates")


@router.get("/showAllProducts", response_class=HTMLResponse)
def get_products(request: Request, db=Depends(get_db)):
    products = productService.get_all_products(db)
    return templates.TemplateResponse("products.html", {"request": request, "products": products})
