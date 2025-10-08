from sqlalchemy import Column, BigInteger, String, Float
from app.database import Base


class ProductProtSep(Base):
    __tablename__ = "ProductsProtSep"

    ID = Column(BigInteger, primary_key=True)
    Produkts = Column(String)
    kcal = Column(Float)
    Tauki = Column(Float)
    Piesat_Tauki = Column("Piesat. Tauki", Float)
    Oglh = Column("Oglh.", Float)
    Cukuri = Column(Float)
    Olb_v = Column("Olb.v", Float, nullable=True)
    Piena_olb_v = Column("Piena olb.v", Float)
    Dzivnieku_olb_v = Column("Dzīvnieku olb.v", Float)
    Augu_olb_v = Column("Augu olb.v", Float)
    Sals = Column(Float)
    Cena_1kg = Column("Cena 1kg", Float)
    Cena_100g = Column("Cena 100g", Float)
