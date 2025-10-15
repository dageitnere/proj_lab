from sqlalchemy.orm import Session
from app.models.productsProtSep import ProductProtSep


def get_all_products(db: Session):
    return db.query(ProductProtSep).all()

def get_products_names(db: Session):
    products = db.query(ProductProtSep.productName).distinct().all()
    names = sorted([p[0] for p in products if p[0]])  # flatten tuples and remove None
    return {"products": names}
