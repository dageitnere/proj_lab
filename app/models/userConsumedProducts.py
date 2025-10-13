from sqlalchemy import Column, BigInteger, String, Float, DateTime, ForeignKey, func
from app.database import Base

class UserConsumedProduct(Base):
    __tablename__ = "userConsumedProducts"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    userUuid = Column(BigInteger, ForeignKey("users.uuid"), nullable=False)
    productName = Column(String, nullable=False)
    amount = Column(Float, nullable=False)  # grams

    kcal = Column(Float, nullable=False)
    fat = Column(Float, nullable=False)
    satFat = Column(Float, nullable=False)
    carbs = Column(Float, nullable=False)
    sugar = Column(Float, nullable=False)
    protein = Column(Float, nullable=False)
    dairyProtein = Column(Float, default=0)
    animalProtein = Column(Float, default=0)
    plantProtein = Column(Float, default=0)
    salt = Column(Float, nullable=False)
    cost = Column(Float, nullable=False)

    date = Column(DateTime(timezone=False), nullable=False)