from sqlalchemy import Column, BigInteger, String, Float, Boolean
from app.backend.database import Base


class ProductProtSep(Base):
    __tablename__ = "productsProtSep"

    id = Column(BigInteger, primary_key=True, index=True)
    productName = Column(String, nullable=False, unique=True, default="")  # matches DB
    kcal = Column(BigInteger, nullable=False, default=0)
    fat = Column(Float, nullable=False, default=0.0)
    satFat = Column(Float, nullable=False, default=0.0)
    carbs = Column(Float, nullable=False, default=0.0)
    sugars = Column(Float, nullable=False, default=0.0)
    protein = Column(Float, nullable=False, default=0.0)
    dairyProt = Column(Float, nullable=False, default=0.0)
    animalProt = Column(Float, nullable=False, default=0.0)
    plantProt = Column(Float, nullable=False, default=0.0)
    salt = Column(BigInteger, nullable=False, default=0)
    price1kg = Column(Float, nullable=False, default=0.0)
    price100g = Column(Float, nullable=False, default=0.0)
    vegan = Column(Boolean, nullable=False, default=False)
    vegetarian = Column(Boolean, nullable=False, default=False)
    dairyFree = Column(Boolean, nullable=False, default=False)
