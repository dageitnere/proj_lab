from sqlalchemy import Column, BigInteger, Text, ForeignKey
from app.database import Base

class UserMenuRecipes(Base):
    __tablename__ = "userMenuRecipes"

    userMenuId = Column(BigInteger, ForeignKey("userMenu.id", ondelete="CASCADE"), primary_key=True)
    recipeId = Column(BigInteger, ForeignKey("recipes.id", ondelete="CASCADE"), primary_key=True)
    mealType = Column(Text, primary_key=True)
