from sqlalchemy import Column, BigInteger, String, Float, Boolean
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(BigInteger, primary_key=True, index=True, unique=True)
    productName = Column(String, nullable=False, unique=True, default="")  # table default matches DB
    kcal = Column(BigInteger, nullable=False, default=0)
    fat = Column(Float, nullable=False, default=0.0)
    satFat = Column(Float, nullable=False, default=0.0)
    carbs = Column(Float, nullable=False, default=0.0)
    sugars = Column(Float, nullable=False, default=0.0)
    protein = Column(Float, nullable=False, default=0.0)
    salt = Column(BigInteger, nullable=False, default=0)
    price1kg = Column(Float, nullable=False, default=0.0)
    price100g = Column(Float, nullable=False, default=0.0)
    vegan = Column(Boolean, nullable=False, default=False)
    vegetarian = Column(Boolean, nullable=False, default=False)
    dairyFree = Column(Boolean, nullable=False, default=False)