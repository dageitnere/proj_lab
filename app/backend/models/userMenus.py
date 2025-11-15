from sqlalchemy import Column, BigInteger, Float, JSON, ForeignKey, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.backend.database import Base

class UserMenu(Base):
    __tablename__ = "userMenu"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    userUuid = Column(BigInteger, ForeignKey("users.uuid"), nullable=False)
    name = Column(String, nullable=False)
    totalKcal = Column(Float, nullable=False)
    totalCost = Column(Float, nullable=False)
    totalFat = Column(Float, nullable=False)
    totalCarbs = Column(Float, nullable=False)
    totalProtein = Column(Float, nullable=False)
    totalDairyProtein = Column(Float, nullable=False)
    totalAnimalProtein = Column(Float, nullable=False)
    totalPlantProtein = Column(Float, nullable=False)
    totalSugar = Column(Float, nullable=False)
    totalSatFat = Column(Float, nullable=False)
    totalSalt = Column(Float, nullable=False)
    date = Column(DateTime(timezone=False), nullable=False)
    plan = Column(JSON, nullable=False)
    vegan = Column(Boolean, default=False, nullable=False)
    vegetarian = Column(Boolean, default=False, nullable=False)
    dairyFree = Column(Boolean, default=False, nullable=False)
    restrictions = Column(JSON, nullable=True)

recipes = relationship("Recipe", secondary="userMenuRecipes")
