from sqlalchemy.orm import Session
from app.backend.models.productsProtSep import ProductProtSep

def get_all_products(db: Session):
    """Fetch and return all base products from the global product table."""
    return db.query(ProductProtSep).all()

def get_products_names(db: Session):
    """
    Return a sorted list of all unique product names.
    Used for auto-complete or search suggestions.
    """
    products = db.query(ProductProtSep.productName).distinct().all()
    names = sorted([p[0] for p in products if p[0]])  # Flatten tuples and remove None values
    return {"products": names}
