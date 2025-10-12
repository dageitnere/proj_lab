from sqlalchemy.orm import Session
from app.models.userProducts import UserProduct
from app.schemas.requests.addUserProductRequest import AddUserProductRequest


def getAllUserProducts(db: Session, user_uuid: int):
    return db.query(UserProduct).filter(UserProduct.userUuid == user_uuid).order_by(UserProduct.id).all()


def getUserProductsNames(db: Session, user_uuid: int):
    products = (
        db.query(UserProduct.produkts)
        .filter(UserProduct.userUuid == user_uuid)
        .distinct()
        .all()
    )
    names = sorted([p[0] for p in products if p[0]])  # flatten tuples and remove None
    return {"products": names}

def add_user_product(db: Session, user_uuid: int, product: AddUserProductRequest) -> UserProduct:
    def zero_if_none(value):
        return value if value is not None else 0

    new_product = UserProduct(
        userUuid=user_uuid,
        produkts=product.produkts,
        kcal=zero_if_none(product.kcal),
        tauki=zero_if_none(product.tauki),
        piesatTauki=zero_if_none(product.piesatTauki),
        oglh=zero_if_none(product.oglh),
        cukuri=zero_if_none(product.cukuri),
        olbv=zero_if_none(product.olbv),
        pienaOlbv=zero_if_none(product.pienaOlbv),
        dzivOlbv=zero_if_none(product.dzivOlbv),
        auguOlbv=zero_if_none(product.auguOlbv),
        sals=zero_if_none(product.sals),
        cena1kg=zero_if_none(product.cena1kg),
        cena100g=zero_if_none(product.cena100g),
        vegan=product.vegan or False,
        vegetarian=product.vegetarian or False,
        dairyFree=product.dairyFree or False
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product