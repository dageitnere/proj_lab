from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.userConsumedProducts import UserConsumedProduct
from app.models.userProducts import UserProduct
from app.models.productsProtSep import ProductProtSep
from app.schemas.requests.userConsumedProductRequest import UserConsumedProductRequest
from app.schemas.responses.userConsumedProductResponse import  UserConsumedProductResponse
from app.schemas.responses.userConsumedProductResponse import  UserConsumedProductListResponse
from sqlalchemy import and_
from datetime import datetime, timedelta

def add_consumed_product(db: Session, data: UserConsumedProductRequest):
    # Try user-specific product first
    product = (
        db.query(UserProduct)
        .filter(UserProduct.userUuid == data.userUuid)
        .filter(UserProduct.produkts.ilike(data.productName.strip()))
        .first()
    )
    if not product:
        product = (
            db.query(ProductProtSep)
            .filter(ProductProtSep.produkts.ilike(data.productName.strip()))
            .first()
        )
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product '{data.productName}' not found."
        )

    factor = data.amount / 100.0

    new_entry = UserConsumedProduct(
        userUuid=data.userUuid,
        productName=data.productName.strip(),
        amount=data.amount,
        kcal=product.kcal * factor,
        fat=product.tauki * factor,
        satFat=product.piesatTauki * factor,
        carbs=product.oglh * factor,
        sugar=product.cukuri * factor,
        protein=product.olbv * factor,
        dairyProtein=product.pienaOlbv * factor,
        animalProtein=product.dzivOlbv * factor,
        plantProtein=product.auguOlbv * factor,
        salt=product.sals * factor,
        cost=product.cena100g * factor,
        date=datetime.now()
    )

    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    return f"Product '{data.productName}' entry added successfully."

def _map_to_response(products) -> UserConsumedProductListResponse:
    """Helper: Convert ORM list -> Pydantic response list"""
    return [
        UserConsumedProductResponse(
            productName=p.productName,
            amount=p.amount,
            kcal=p.kcal,
            fat=p.fat,
            satFat=p.satFat,
            carbs=p.carbs,
            sugar=p.sugar,
            protein=p.protein,
            dairyProtein=p.dairyProtein,
            animalProtein=p.animalProtein,
            plantProtein=p.plantProtein,
            salt=p.salt,
            cost=p.cost,
            createdAt=p.date
        )
        for p in products
    ]

def get_all_consumed_products(db: Session, user_uuid: int) -> UserConsumedProductListResponse:
    products = db.query(UserConsumedProduct).filter(UserConsumedProduct.userUuid == user_uuid).all()
    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No consumed products found.")
    return _map_to_response(products)


def get_consumed_today(db: Session, user_uuid: int) -> UserConsumedProductListResponse:
    today = datetime.now().date()
    products = (
        db.query(UserConsumedProduct)
        .filter(
            and_(
                UserConsumedProduct.userUuid == user_uuid,
                UserConsumedProduct.date >= datetime.combine(today, datetime.min.time()),
                UserConsumedProduct.date <= datetime.combine(today, datetime.max.time())
            )
        )
        .all()
    )
    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No products consumed today.")
    return _map_to_response(products)


def get_consumed_last_7_days(db: Session, user_uuid: int) -> UserConsumedProductListResponse:
    seven_days_ago = datetime.now() - timedelta(days=7)
    products = (
        db.query(UserConsumedProduct)
        .filter(
            and_(
                UserConsumedProduct.userUuid == user_uuid,
                UserConsumedProduct.date >= seven_days_ago
            )
        )
        .all()
    )
    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No products consumed in the last 7 days.")
    return _map_to_response(products)


def get_consumed_last_30_days(db: Session, user_uuid: int) -> UserConsumedProductListResponse:
    thirty_days_ago = datetime.now() - timedelta(days=30)
    products = (
        db.query(UserConsumedProduct)
        .filter(
            and_(
                UserConsumedProduct.userUuid == user_uuid,
                UserConsumedProduct.date >= thirty_days_ago
            )
        )
        .all()
    )
    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No products consumed in the last 30 days.")
    return _map_to_response(products)