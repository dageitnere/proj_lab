from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime, timedelta
from app.backend.models.userConsumedProducts import UserConsumedProduct
from app.backend.models.userProducts import UserProduct
from app.backend.models.productsProtSep import ProductProtSep
from app.backend.schemas.requests.postUserConsumedProductRequest import PostUserConsumedProductRequest
from app.backend.schemas.requests.deleteConsumedProductRequest import DeleteConsumedProductRequest
from app.backend.schemas.requests.getConsumedProductByDateRequest import GetConsumedProductByDateRequest
from app.backend.schemas.responses.userConsumedProductResponse import UserConsumedProductResponse, UserConsumedProductListResponse


def add_consumed_product(db: Session, request: PostUserConsumedProductRequest, userUuid: int):
    """
    Add a new consumed product entry for a user.

    - Looks up the product by name (first in user’s products, then in global DB)
    - Calculates nutritional values proportionally to the consumed amount
    - Stores the record in `UserConsumedProduct`
    """
    # Try to find the product in user's custom list
    product = (
        db.query(UserProduct)
        .filter(UserProduct.userUuid == userUuid)
        .filter(UserProduct.productName.ilike(request.productName.strip()))
        .first()
    )

    # Fall back to global products if not found in user's list
    if not product:
        product = (
            db.query(ProductProtSep)
            .filter(ProductProtSep.productName.ilike(request.productName.strip()))
            .first()
        )

    # Product not found at all
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product '{request.productName}' not found."
        )

    # Scale nutrients according to user-entered amount (base = per 100g)
    factor = request.amount / 100.0

    new_entry = UserConsumedProduct(
        userUuid=userUuid,
        productName=request.productName.strip().title(),
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
        date=request.date if request.date else datetime.now()
    )

    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    return f"Product '{request.productName}' entry added successfully."


def delete_consumed_product(db: Session, request: DeleteConsumedProductRequest):
    """Delete a consumed product entry by its ID."""
    product = db.query(UserConsumedProduct).filter(UserConsumedProduct.id == request.productId).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No consumed product found with ID {request.productId} for user.")

    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully."}


def _map_to_response(products) -> UserConsumedProductListResponse:
    """Map DB model objects to response schema objects."""
    return [
        UserConsumedProductResponse(
            id=p.id,
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
    """Return all consumed products for a given user."""
    products = db.query(UserConsumedProduct).filter(UserConsumedProduct.userUuid == userUuid).all()
    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No consumed products found.")
    return _map_to_response(products)


def get_consumed_today(db: Session, userUuid: int) -> UserConsumedProductListResponse:
    """Return all products consumed today."""
    today = datetime.now().date()
    products = (
        db.query(UserConsumedProduct)
        .filter(
            and_(
                UserConsumedProduct.userUuid == userUuid,
                UserConsumedProduct.date >= datetime.combine(today, datetime.min.time()),
                UserConsumedProduct.date <= datetime.combine(today, datetime.max.time())
            )
        ).all()
    )
    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No products consumed today.")
    return _map_to_response(products)


def get_consumed_last_7_days(db: Session, userUuid: int):
    """Return all consumed products within the past 7 days."""
    seven_days_ago = datetime.now() - timedelta(days=7)
    products = db.query(UserConsumedProduct).filter(
        and_(UserConsumedProduct.userUuid == userUuid, UserConsumedProduct.date >= seven_days_ago)
    ).all()
    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No products consumed in the last 7 days.")
    return _map_to_response(products)


def get_consumed_last_30_days(db: Session, userUuid: int):
    """Return all consumed products within the past 30 days."""
    thirty_days_ago = datetime.now() - timedelta(days=30)
    products = db.query(UserConsumedProduct).filter(
        and_(UserConsumedProduct.userUuid == userUuid, UserConsumedProduct.date >= thirty_days_ago)
    ).all()
    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No products consumed in the last 30 days.")
    return _map_to_response(products)


def get_consumed_by_date(db: Session, request: GetConsumedProductByDateRequest, userUuid: int):
    """Return all products consumed on a specific date."""
    start_of_day = datetime.combine(request.date, datetime.min.time())
    end_of_day = datetime.combine(request.date, datetime.max.time())
    products = db.query(UserConsumedProduct).filter(
        and_(
            UserConsumedProduct.userUuid == userUuid,
            UserConsumedProduct.date >= start_of_day,
            UserConsumedProduct.date <= end_of_day
        )
    ).all()

    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No products consumed on {request.date}.")
    return _map_to_response(products)