from sqlalchemy import Column, BigInteger, Float, String, Boolean, ForeignKey
from app.database import Base

class UserProduct(Base):
    __tablename__ = "userProducts"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    userUuid = Column(BigInteger, ForeignKey("users.uuid"), nullable=False)
    productName = Column(String, nullable=False, default="")  # DB default
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