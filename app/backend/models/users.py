from sqlalchemy import Column, Identity, BigInteger, Float, String, Boolean, TIMESTAMP
from app.backend.database import Base

class User(Base):
    __tablename__ = "users"

    uuid = Column(BigInteger, Identity(always=False), primary_key=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    age = Column(BigInteger, nullable=False)
    gender = Column(String, nullable=False)
    weight = Column(BigInteger, nullable=False)
    height = Column(BigInteger, nullable=False)
    bmi = Column(Float, nullable=False)
    bmr = Column(Float, nullable=False)
    calculatedKcal = Column(Float, nullable=True)
    activityFactor = Column(String, nullable=False)
    goal = Column(String, nullable=True, default="MAINTAIN")
    isVegan = Column(Boolean, nullable=False)
    isDairyInt = Column(Boolean, nullable=False)
    isVegetarian = Column(Boolean, nullable=False)
    verificationCode = Column(BigInteger, nullable=True)
    verificationExpiresAt = Column(TIMESTAMP(timezone=True), nullable=True)
    emailVerified = Column(Boolean, nullable=False, default=False)