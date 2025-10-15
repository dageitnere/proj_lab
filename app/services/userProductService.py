from sqlalchemy.orm import Session
from app.models.userProducts import UserProduct
from app.schemas.requests.addUserProductByRimiUrlRequest import AddUserProductByRimiUrlRequest
from app.schemas.requests.addUserProductRequest import AddUserProductRequest
from fastapi import HTTPException, status
from app.schemas.requests.deleteUserProductRequest import DeleteUserProductRequest
from app.dependencies import scrape_rimi_product

def zero_if_none(value):
    return value if value is not None else 0


def get_user_products(db: Session, userUuid: int):
    return db.query(UserProduct).filter(UserProduct.userUuid == userUuid).order_by(UserProduct.id).all()


def get_user_products_names(db: Session, userUuid: int):
    products = (
        db.query(UserProduct.productName)
        .filter(UserProduct.userUuid == userUuid)
        .distinct()
        .all()
    )
    names = sorted([p[0] for p in products if p[0]])  # flatten tuples and remove None
    return {"products": names}

def add_user_product(db: Session, request: AddUserProductRequest) -> UserProduct:
    # Check if product name already exists (case-insensitive)
    existing = (
        db.query(UserProduct)
        .filter(UserProduct.userUuid == request.userUuid)
        .filter(UserProduct.productName.ilike(request.productName.strip()))
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Product '{request.productName}' already exists in your list."
        )

    new_product = UserProduct(
        userUuid=request.userUuid,
        productName=request.productName.strip(),
        kcal=zero_if_none(request.kcal),
        fat=zero_if_none(request.fat),
        satFat=zero_if_none(request.satFat),
        carbs=zero_if_none(request.carbs),
        sugars=zero_if_none(request.sugars),
        protein=zero_if_none(request.protein),
        dairyProt=zero_if_none(request.dairyProt),
        animalProt=zero_if_none(request.animalProt),
        plantProt=zero_if_none(request.plantProt),
        salt=zero_if_none(request.salt),
        price1kg=zero_if_none(request.price1kg),
        price100g=zero_if_none(request.price100g),
        vegan=request.vegan or False,
        vegetarian=request.vegetarian or False,
        dairyFree=request.dairyFree or False
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

def delete_user_product(db: Session, request: DeleteUserProductRequest):
    product = (
        db.query(UserProduct)
        .filter(UserProduct.userUuid == request.userUuid)
        .filter(UserProduct.productName.ilike(request.productName.strip()))
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product '{request.productName}' not found for this user."
        )

    # Delete the product
    db.delete(product)
    db.commit()

    return {"message": f"Product '{request.productName}' deleted successfully."}


def add_user_product_by_rimi_url(db: Session, request: AddUserProductByRimiUrlRequest):
    # --- Scrape product data ---
    scraped = scrape_rimi_product(request.url, mass_g=request.mass_g)
    print(f"Scraped data: {scraped}")
    if not scraped:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to scrape the product. Please check the URL."
        )

    # --- Use scraped name if not provided ---
    product_name = request.productName.strip() if request.productName else scraped.get("productName")
    if not product_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product name could not be determined from URL."
        )

    # --- Check if product already exists ---
    existing = (
        db.query(UserProduct)
        .filter(UserProduct.userUuid == request.userUuid)
        .filter(UserProduct.productName.ilike(product_name))
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Product '{product_name}' already exists in your list."
        )

    # --- Handle protein assignment ---
    protein_flags = [
        request.dairyProtein,
        request.animalProtein,
        request.plantProtein
    ]
    if sum(bool(flag) for flag in protein_flags) != 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please select exactly one protein type (dairy, animal, or plant)."
        )

    dairyProt = scraped["protein"] if request.dairyProtein else 0
    animalProt = scraped["protein"] if request.animalProtein else 0
    plantProt = scraped["protein"] if request.plantProtein else 0

    # --- Create new product ---
    new_product = UserProduct(
        userUuid=request.userUuid,
        productName=product_name,
        kcal=zero_if_none(scraped.get("kcal")),
        fat=zero_if_none(scraped.get("fat")),
        satFat=zero_if_none(scraped.get("satFat")),
        carbs=zero_if_none(scraped.get("carbs")),
        sugars=zero_if_none(scraped.get("sugars")),
        protein=zero_if_none(scraped.get("protein")),
        dairyProt=dairyProt,
        animalProt=animalProt,
        plantProt=plantProt,
        salt=zero_if_none(scraped.get("salt")),
        price1kg=zero_if_none(scraped.get("price1Kg")),
        price100g=zero_if_none(scraped.get("price100g")),
        vegan=request.vegan or False,
        vegetarian=request.vegetarian or False,
        dairyFree=request.dairyFree or False
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    # --- Warn if nutrition info is incomplete ---
    missing_nutrition = [k for k in ["kcal", "fat", "satFat", "carbs", "sugars", "protein"] if scraped.get(k) is None]
    if missing_nutrition:
        print(f"⚠️ Warning: Nutrition info missing for: {', '.join(missing_nutrition)}")

    return {"message": f"Product {new_product.productName} added successfully."}
