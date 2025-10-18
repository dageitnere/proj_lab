from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.userConsumedProducts import UserConsumedProduct
from app.models.userProducts import UserProduct
from app.models.productsProtSep import ProductProtSep
from app.schemas.requests.addUserConsumedProductRequest import AddUserConsumedProductRequest
from app.schemas.requests.deleteConsumedProductRequest import DeleteConsumedProductRequest
from app.schemas.requests.getConsumedProductByDateRequest import GetConsumedProductByDateRequest
from app.schemas.responses.userConsumedProductResponse import  UserConsumedProductResponse
from app.schemas.responses.userConsumedProductResponse import  UserConsumedProductListResponse
from sqlalchemy import and_
from datetime import datetime, timedelta

def add_consumed_product(db: Session, request: AddUserConsumedProductRequest, userUuid: int):
    # Try user-specific product first
    product = (
        db.query(UserProduct)
        .filter(UserProduct.userUuid == userUuid)
        .filter(UserProduct.productName.ilike(request.productName.strip()))
        .first()
    )
    if not product:
        product = (
            db.query(ProductProtSep)
            .filter(ProductProtSep.productName.ilike(request.productName.strip()))
            .first()
        )
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product '{request.productName}' not found."
        )

    factor = request.amount / 100.0

    new_entry = UserConsumedProduct(
        userUuid=userUuid,
        productName=request.productName.strip(),
        amount=request.amount,
        kcal=product.kcal * factor,
        fat=product.fat * factor,
        satFat=product.satFat * factor,
        carbs=product.carbs * factor,
        sugar=product.sugars * factor,
        protein=product.protein * factor,
        dairyProtein=product.dairyProt * factor,
        animalProtein=product.animalProt * factor,
        plantProtein=product.plantProt * factor,
        salt=product.salt * factor,
        cost=product.price100g * factor,
        date=datetime.now()
    )

    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    return f"Product '{request.productName}' entry added successfully."

def delete_consumed_product(db: Session, request: DeleteConsumedProductRequest):
    """
    Delete a single consumed product row by its ID for the given user.
    """
    product = (
        db.query(UserConsumedProduct)
        .filter(
            UserConsumedProduct.id == request.productId,
        )
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No consumed product found with ID {request.productId} for user."
        )

    db.delete(product)
    db.commit()

    return {"message": f"Product deleted successfully."}

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

def get_all_consumed_products(db: Session, userUuid: int) -> UserConsumedProductListResponse:
    products = db.query(UserConsumedProduct).filter(UserConsumedProduct.userUuid == userUuid).all()
    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No consumed products found.")
    return _map_to_response(products)


def get_consumed_today(db: Session, userUuid: int) -> UserConsumedProductListResponse:
    today = datetime.now().date()
    products = (
        db.query(UserConsumedProduct)
        .filter(
            and_(
                UserConsumedProduct.userUuid == userUuid,
                UserConsumedProduct.date >= datetime.combine(today, datetime.min.time()),
                UserConsumedProduct.date <= datetime.combine(today, datetime.max.time())
            )
        )
        .all()
    )
    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No products consumed today.")
    return _map_to_response(products)


def get_consumed_last_7_days(db: Session, userUuid: int) -> UserConsumedProductListResponse:
    seven_days_ago = datetime.now() - timedelta(days=7)
    products = (
        db.query(UserConsumedProduct)
        .filter(
            and_(
                UserConsumedProduct.userUuid == userUuid,
                UserConsumedProduct.date >= seven_days_ago
            )
        )
        .all()
    )
    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No products consumed in the last 7 days.")
    return _map_to_response(products)


def get_consumed_last_30_days(db: Session, userUuid: int) -> UserConsumedProductListResponse:
    thirty_days_ago = datetime.now() - timedelta(days=30)
    products = (
        db.query(UserConsumedProduct)
        .filter(
            and_(
                UserConsumedProduct.userUuid == userUuid,
                UserConsumedProduct.date >= thirty_days_ago
            )
        )
        .all()
    )
    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No products consumed in the last 30 days.")
    return _map_to_response(products)

def get_consumed_by_date(db: Session, request: GetConsumedProductByDateRequest, userUuid: int) -> UserConsumedProductListResponse:
    start_of_day = datetime.combine(request.date, datetime.min.time())
    end_of_day = datetime.combine(request.date, datetime.max.time())

    products = (
        db.query(UserConsumedProduct)
        .filter(
            and_(
                UserConsumedProduct.userUuid == userUuid,
                UserConsumedProduct.date >= start_of_day,
                UserConsumedProduct.date <= end_of_day
            )
        )
        .all()
    )

    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No products consumed on {request.date}."
        )

    return _map_to_response(products)