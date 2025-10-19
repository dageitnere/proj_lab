from sqlalchemy import Column, BigInteger, String, Float, Text
from app.database import Base

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    instructions = Column(Text, nullable=False)
    pictureBase64 = Column(Text, nullable=True)
    calories = Column(Float, nullable=True)
