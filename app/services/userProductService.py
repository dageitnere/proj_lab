from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.dependencies.scrapeNutriotionValue import get_product_data_from_url
from app.models.products import Product
from app.models.userProducts import UserProduct
from app.schemas.requests.addUserProductByNutritionValueRequest import AddUserProductByNutritionValueUrlRequest
from app.schemas.requests.addUserProductByRimiUrlRequest import AddUserProductByRimiUrlRequest
from app.schemas.requests.addUserProductRequest import AddUserProductRequest
from fastapi import HTTPException, status
from app.schemas.requests.deleteUserProductRequest import DeleteUserProductRequest
from app.dependencies.scrapeRimi import scrape_rimi_product
from app.schemas.requests.updateUserProductRequest import UpdateUserProductRequest


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

def add_user_product(db: Session, request: AddUserProductRequest, userUuid: int) -> UserProduct:
    product_name = request.productName.strip()

    existing_user = (
        db.query(UserProduct)
        .filter(UserProduct.userUuid == userUuid)
        .filter(UserProduct.productName.ilike(product_name))
        .first()
    )

    existing_global = (
        db.query(Product)
        .filter(Product.productName.ilike(product_name))
        .first()
    )

    if existing_user or existing_global:
        raise HTTPException(
            status_code=400,
            detail=f"Product '{product_name}' already exists in your list or in the global products."
        )

    # Calculate price100g from price1kg
    price1kg = zero_if_none(request.price1kg)
    price100g = round(price1kg / 10, 2) if price1kg > 0 else 0

    new_product = UserProduct(
        userUuid=userUuid,
        productName=request.productName.strip().title(),
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
        price1kg=price1kg,
        price100g=price100g,
        vegan=request.vegan or False,
        vegetarian=request.vegetarian or False,
        dairyFree=request.dairyFree or False
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

def delete_user_product(db: Session, request: DeleteUserProductRequest, userUuid: int):
    product = (
        db.query(UserProduct)
        .filter(UserProduct.userUuid == userUuid)
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


def add_user_product_by_rimi_url(db: Session, request: AddUserProductByRimiUrlRequest, userUuid: int):
    # --- Scrape product data ---
    scraped = scrape_rimi_product(request.url, mass_g=request.mass_g)
    print(f"Scraped data: {scraped}")
    if not scraped or "error" in scraped:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to scrape product data from the URL: {scraped.get('error', 'Unknown error')}"
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
        .filter(UserProduct.userUuid == userUuid)
        .filter(UserProduct.URL.ilike(request.url.strip()))
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Product already exists in your list: '{existing.productName}'."
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
        userUuid=userUuid,
        productName=product_name.strip().title(),
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
        dairyFree=request.dairyFree or False,
        URL = request.url.strip()
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    # --- Warn if nutrition info is incomplete ---
    missing_nutrition = [k for k in ["kcal", "fat", "satFat", "carbs", "sugars", "protein"] if scraped.get(k) is None]
    if missing_nutrition:
        print(f"Warning: Nutrition info missing for: {', '.join(missing_nutrition)}")

    return {"message": f"Product {new_product.productName} added successfully."}

def add_user_product_by_nutrition_value_url(db: Session, request: AddUserProductByNutritionValueUrlRequest, userUuid: int):
    # --- Scrape product data ---
    scraped = get_product_data_from_url(request.url)
    if not scraped or "error" in scraped:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to scrape product data from the URL: {scraped.get('error', 'Unknown error')}"
        )

    # --- Use provided product name or scraped one ---
    product_name = request.productName.strip() if request.productName else scraped.get("productName")
    if not product_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product name could not be determined."
        )

    # --- Check if product already exists for this user ---
    existing = (
        db.query(UserProduct)
        .filter(UserProduct.userUuid == userUuid)
        .filter(UserProduct.URL.ilike(request.url.strip()))
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Product already exists in your list: '{existing.productName}'."
        )

    # --- Handle price logic ---
    price1kg = request.price1kg
    price100g = None

    if request.pricePerUnit is not None:
        if request.massPerUnit is None or request.massPerUnit <= 0 or price1kg is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="If price per unit is provided, mass per unit must also be specified and greater than 0, furthermore - do not provide price per 1kg with price per unit."
            )

        # Calculate price1kg and price100g based on massPerUnit (grams)
        price1kg = (request.pricePerUnit / request.massPerUnit) * 1000
        price100g = price1kg / 10
    elif price1kg is not None:
        price100g = price1kg / 10

    # --- Protein type control ---
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

    # --- Create and save new product ---
    new_product = UserProduct(
        userUuid=userUuid,
        productName=product_name.strip().title(),
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
        price1kg=round(zero_if_none(price1kg), 2),
        price100g=round(zero_if_none(price100g), 2),
        vegan=request.vegan,
        vegetarian=request.vegetarian,
        dairyFree=request.dairyFree,
        URL = request.url.strip()
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    # --- Optional: warn if missing nutritional values ---
    missing_nutrition = [k for k in ["kcal", "fat", "satFat", "carbs", "sugars", "protein"] if scraped.get(k) is None]
    if missing_nutrition:
        print(f"⚠️ Missing nutrition info for: {', '.join(missing_nutrition)}")

    return {"message": f"Product '{new_product.productName}' added successfully."}


def update_user_product(db: Session, request: UpdateUserProductRequest, userUuid: int):
    """
    Update an existing user product - PROTEIN TYPE IS OPTIONAL.
    If no protein type selected, scales existing distribution.
    """
    # Find the product to update
    product_to_update = (
        db.query(UserProduct)
        .filter(UserProduct.userUuid == userUuid)
        .filter(UserProduct.productName.ilike(request.oldProductName.strip()))
        .first()
    )

    if not product_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product '{request.oldProductName}' not found for this user."
        )

    # Check name conflicts if changing name
    if request.productName and request.productName.strip() != request.oldProductName.strip():
        new_name = request.productName.strip()
        name_conflict_user = (
            db.query(UserProduct)
            .filter(UserProduct.userUuid == userUuid)
            .filter(UserProduct.productName.ilike(new_name))
            .first()
        )
        if name_conflict_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Product name '{new_name}' already exists."
            )

    updated_fields = False

    # **1. UPDATE BASIC FIELDS**
    if request.productName is not None:
        product_to_update.productName = request.productName.strip().title()
        updated_fields = True

    if request.kcal is not None:
        product_to_update.kcal = zero_if_none(request.kcal)
        updated_fields = True

    if request.fat is not None:
        product_to_update.fat = zero_if_none(request.fat)
        updated_fields = True

    if request.satFat is not None:
        product_to_update.satFat = zero_if_none(request.satFat)
        updated_fields = True

    if request.carbs is not None:
        product_to_update.carbs = zero_if_none(request.carbs)
        updated_fields = True

    if request.sugars is not None:
        product_to_update.sugars = zero_if_none(request.sugars)
        updated_fields = True

    if request.salt is not None:
        product_to_update.salt = zero_if_none(request.salt)
        updated_fields = True

    if request.price1kg is not None:
        product_to_update.price1kg = zero_if_none(request.price1kg)
        product_to_update.price100g = round(product_to_update.price1kg / 10, 2) if product_to_update.price1kg > 0 else 0
        updated_fields = True

    if request.vegan is not None:
        product_to_update.vegan = request.vegan
        updated_fields = True

    if request.vegetarian is not None:
        product_to_update.vegetarian = request.vegetarian
        updated_fields = True

    if request.dairyFree is not None:
        product_to_update.dairyFree = request.dairyFree
        updated_fields = True

    if request.URL is not None:
        product_to_update.URL = request.URL.strip() if request.URL.strip() else None
        updated_fields = True

    # **2. PROTEIN HANDLING - COMPLETELY OPTIONAL**
    protein_change_detected = (
            request.protein is not None or
            request.dairyProtein is not None or
            request.animalProtein is not None or
            request.plantProtein is not None
    )

    if protein_change_detected:
        updated_fields = True

        # Get new protein value (use existing if not provided)
        new_protein_value = zero_if_none(request.protein) if request.protein is not None else product_to_update.protein

        # Count explicitly provided protein types (ignoring None values)
        provided_types = []
        if request.dairyProtein is not None:
            provided_types.append(request.dairyProtein)
        if request.animalProtein is not None:
            provided_types.append(request.animalProtein)
        if request.plantProtein is not None:
            provided_types.append(request.plantProtein)

        selected_count = sum(1 for x in provided_types if x is True)

        # **VALIDATION: Only one protein type can be selected**
        if selected_count > 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only one protein type can be selected."
            )

        # **CASE 1: Exactly one protein type explicitly provided**
        if selected_count == 1:
            # Reset all protein types
            product_to_update.dairyProt = 0
            product_to_update.animalProt = 0
            product_to_update.plantProt = 0

            # Assign full amount to selected type
            if request.dairyProtein == True:
                product_to_update.dairyProt = new_protein_value
            elif request.animalProtein == True:
                product_to_update.animalProt = new_protein_value
            elif request.plantProtein == True:
                product_to_update.plantProt = new_protein_value

        # **CASE 2: No protein type explicitly provided (or all False)**
        else:
            # Keep existing protein type distribution, scale if protein amount changed
            total_existing_protein = (
                    product_to_update.dairyProt +
                    product_to_update.animalProt +
                    product_to_update.plantProt
            )

            if total_existing_protein > 0 and request.protein is not None:
                # Scale existing distribution proportionally
                scale_factor = new_protein_value / total_existing_protein
                product_to_update.dairyProt *= scale_factor
                product_to_update.animalProt *= scale_factor
                product_to_update.plantProt *= scale_factor
            elif total_existing_protein == 0 and request.protein is not None:
                # No existing distribution - default to dairy
                product_to_update.dairyProt = new_protein_value

        # Always update total protein
        product_to_update.protein = new_protein_value

    # **FINAL VALIDATION**
    if not updated_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one field must be provided to update."
        )

    db.commit()
    db.refresh(product_to_update)
    return {"message": f"Product '{product_to_update.productName}' updated successfully."}