from sqlalchemy import Column, BigInteger, Float, String, Boolean, ForeignKey
from app.database import Base

class UserProduct(Base):
    __tablename__ = "userProducts"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    userUuid = Column(BigInteger, ForeignKey("users.uuid"), nullable=False)
    produkts = Column(String, nullable=False, default="")  # DB default
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