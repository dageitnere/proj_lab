from sqlalchemy import Column, BigInteger, String, Float
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(BigInteger, primary_key=True, index=True)
    produkts = Column(String, nullable=True)
    kcal = Column(BigInteger, nullable=True)
    tauki = Column(Float, nullable=True)
    piesatTauki = Column(Float, nullable=True)
    oglh = Column(Float, nullable=True)
    cukuri = Column(Float, nullable=True)
    olbv = Column(Float, nullable=True)
    sals = Column(BigInteger, nullable=True)
    cena1kg = Column(Float, nullable=True)
    cena100g = Column(Float, nullable=True)
