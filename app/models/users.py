from sqlalchemy import Column, BigInteger, Float, String, Boolean, TIMESTAMP
from app.database import Base

class User(Base):
    __tablename__ = "users"

    uuid = Column(BigInteger, primary_key=True, index=True)
    username = Column(String, nullable=True)
    email = Column(String, nullable=True)
    password = Column(String, nullable=True)
    age = Column(BigInteger, nullable=True)
    gender = Column(String, nullable=True)
    weight = Column(BigInteger, nullable=True)
    height = Column(BigInteger, nullable=True)
    bmi = Column(Float, nullable=True)
    bmr = Column(Float, nullable=True)
    calculatedKcal = Column(Float, nullable=True)
    activityFactor = Column(String, nullable=True)
    goal = Column(String, nullable=True)
    isVegan = Column(Boolean, nullable=True)
    isDairyInt = Column(Boolean, nullable=True)
    isVegetarian = Column(Boolean, nullable=True)
    verificationCode = Column(BigInteger, nullable=True)
    verificationExpiresAt = Column(TIMESTAMP(timezone=True), nullable=True)
    emailVerified = Column(Boolean, nullable=True)
