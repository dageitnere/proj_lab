from sqlalchemy import Column, BigInteger, Text, Integer, ForeignKey
from app.backend.database import Base

class UserMenuRecipes(Base):
    __tablename__ = "userMenuRecipes"

    userMenuId = Column(BigInteger, ForeignKey("userMenu.id", ondelete="CASCADE"), primary_key=True)
    recipeId = Column(BigInteger, ForeignKey("recipes.id", ondelete="CASCADE"), primary_key=True)
    mealType = Column(Text, nullable=False)
    recipeBatch = Column(Integer, nullable=False, default=1)