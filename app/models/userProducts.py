from sqlalchemy import Column, BigInteger, Float, String, Boolean, ForeignKey
from app.database import Base

class UserProduct(Base):
    __tablename__ = "userProducts"

    id = Column(BigInteger, primary_key=True, index=True)
    userUuid = Column(BigInteger, ForeignKey("users.uuid"), nullable=False)
    produkts = Column(String, nullable=False)
    kcal = Column(BigInteger)
    tauki = Column(Float)
    piesatTauki = Column(Float)
    oglh = Column(Float)
    cukuri = Column(Float)
    olbv = Column(Float)
    pienaOlbv = Column(Float)
    dzivOlbv = Column(Float)
    auguOlbv = Column(Float)
    sals = Column(BigInteger)
    cena1kg = Column(Float)
    cena100g = Column(Float)
    vegan = Column(Boolean)
    vegetarian = Column(Boolean)
    dairyFree = Column(Boolean)