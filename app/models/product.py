from sqlalchemy import Column, BigInteger, String, Float
from app.database import Base

class Product(Base):
    __tablename__ = "Products"

    ID = Column(BigInteger, primary_key=True, index=True)
    Produkts = Column(String, nullable=True)
    kcal = Column(BigInteger, nullable=True)
    Tauki = Column(Float, nullable=True)
    Piesat_Tauki = Column("Piesat. Tauki", Float, nullable=True)
    Oglh = Column("Oglh.", Float, nullable=True)
    Cukuri = Column(Float, nullable=True)
    Olb_v = Column("Olb.v", Float, nullable=True)
    Sals = Column(BigInteger, nullable=True)
    Cena_1kg = Column("Cena 1kg", Float, nullable=True)
    Cena_100g = Column("Cena 100g", Float, nullable=True)
