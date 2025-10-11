from sqlalchemy.orm import Session
from app.models.productsProtSep import ProductProtSep


def getAllProducts(db: Session):
    return db.query(ProductProtSep).all()

def getProductsNames(db: Session):
    products = db.query(ProductProtSep.produkts).distinct().all()
    names = sorted([p[0] for p in products if p[0]])  # flatten tuples and remove None
    return {"products": names}
