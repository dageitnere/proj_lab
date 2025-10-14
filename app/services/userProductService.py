from sqlalchemy.orm import Session
from app.models.userProducts import UserProduct
from app.schemas.requests.addUserProductRequest import AddUserProductRequest
from fastapi import HTTPException, status
from app.schemas.requests.deleteUserProductRequest import DeleteUserProductRequest


def zero_if_none(value):
    return value if value is not None else 0


def get_user_products(db: Session, userUuid: int):
    return db.query(UserProduct).filter(UserProduct.userUuid == userUuid).order_by(UserProduct.id).all()


def get_user_products_names(db: Session, userUuid: int):
    products = (
        db.query(UserProduct.produkts)
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
        .filter(UserProduct.produkts.ilike(request.produkts.strip()))
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Product '{request.produkts}' already exists in your list."
        )

    new_product = UserProduct(
        userUuid=request.userUuid,
        produkts=request.produkts.strip(),
        kcal=zero_if_none(request.kcal),
        tauki=zero_if_none(request.tauki),
        piesatTauki=zero_if_none(request.piesatTauki),
        oglh=zero_if_none(request.oglh),
        cukuri=zero_if_none(request.cukuri),
        olbv=zero_if_none(request.olbv),
        pienaOlbv=zero_if_none(request.pienaOlbv),
        dzivOlbv=zero_if_none(request.dzivOlbv),
        auguOlbv=zero_if_none(request.auguOlbv),
        sals=zero_if_none(request.sals),
        cena1kg=zero_if_none(request.cena1kg),
        cena100g=zero_if_none(request.cena100g),
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
        .filter(UserProduct.produkts.ilike(request.produkts.strip()))
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product '{request.produkts}' not found for this user."
        )

    # Delete the product
    db.delete(product)
    db.commit()

    return {"message": f"Product '{request.produkts}' deleted successfully."}