from sqlalchemy import Column, BigInteger, String, Float, Boolean
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(BigInteger, primary_key=True, index=True, unique=True)
    produkts = Column(String, nullable=False, unique=True, default="")  # table default matches DB
    kcal = Column(BigInteger, nullable=False, default=0)
    tauki = Column(Float, nullable=False, default=0.0)
    piesatTauki = Column(Float, nullable=False, default=0.0)
    oglh = Column(Float, nullable=False, default=0.0)
    cukuri = Column(Float, nullable=False, default=0.0)
    olbv = Column(Float, nullable=False, default=0.0)
    sals = Column(BigInteger, nullable=False, default=0)
    cena1kg = Column(Float, nullable=False, default=0.0)
    cena100g = Column(Float, nullable=False, default=0.0)
    vegan = Column(Boolean, nullable=False, default=False)
    vegetarian = Column(Boolean, nullable=False, default=False)
    dairyFree = Column(Boolean, nullable=False, default=False)