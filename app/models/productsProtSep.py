from sqlalchemy import Column, BigInteger, String, Float, Boolean
from app.database import Base


class ProductProtSep(Base):
    __tablename__ = "productsProtSep"

    id = Column(BigInteger, primary_key=True, index=True)
    produkts = Column(String, nullable=False, unique=True, default="")  # matches DB
    kcal = Column(BigInteger, nullable=False, default=0)
    tauki = Column(Float, nullable=False, default=0.0)
    piesatTauki = Column(Float, nullable=False, default=0.0)
    oglh = Column(Float, nullable=False, default=0.0)
    cukuri = Column(Float, nullable=False, default=0.0)
    olbv = Column(Float, nullable=False, default=0.0)
    pienaOlbv = Column(Float, nullable=False, default=0.0)
    dzivOlbv = Column(Float, nullable=False, default=0.0)
    auguOlbv = Column(Float, nullable=False, default=0.0)
    sals = Column(BigInteger, nullable=False, default=0)
    cena1kg = Column(Float, nullable=False, default=0.0)
    cena100g = Column(Float, nullable=False, default=0.0)
    vegan = Column(Boolean, nullable=False, default=False)
    vegetarian = Column(Boolean, nullable=False, default=False)
    dairyFree = Column(Boolean, nullable=False, default=False)
