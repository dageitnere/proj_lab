from sqlalchemy.orm import Session
from app.models.userProducts import UserProduct


def getAllUserProducts(db: Session, user_uuid: int):
    return db.query(UserProduct).filter(UserProduct.userUuid == user_uuid).all()


def getUserProductsNames(db: Session, user_uuid: int):
    products = (
        db.query(UserProduct.produkts)
        .filter(UserProduct.userUuid == user_uuid)
        .distinct()
        .all()
    )
    names = sorted([p[0] for p in products if p[0]])  # flatten tuples and remove None
    return {"products": names}
