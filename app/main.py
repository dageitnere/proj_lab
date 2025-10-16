from fastapi import FastAPI
from app.routers import productRouter
from app.routers import menuRouter
from app.routers import mainPageRouter
from app.routers import userProductRouter
from app.routers import consumedProductRouter
from app.routers import statisticsRouter
from app.routers import userRouter
app = FastAPI(
    title="Diet Optimization API",
    description="Backend service"
)

# Include routers
app.include_router(productRouter.product, prefix="/products", tags=["products"])
app.include_router(menuRouter.menu, prefix ="/menu", tags=["menu"])
app.include_router(mainPageRouter.mainPage, tags=["main_page"])
app.include_router(userProductRouter.userProduct, prefix="/userProducts", tags=["userProducts"])
app.include_router(consumedProductRouter.consumedProduct, prefix="/consumedProducts", tags=["consumedProducts"])
app.include_router(statisticsRouter.statistics, prefix="/statistics", tags=["statistics"])
app.include_router(userRouter.router, prefix="/auth", tags=["auth"])

# testesanai - lai izvada hashotu paroli, kas registracija saglabatos db
#from passlib.context import CryptContext
#pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
#hashed = pwd.hash("fitness")
#print(hashed)

# btw bcrypt un passlib vjg kka ieinstalet, lai viens otra versijas atbalsta
# pip install --upgrade passlib[bcrypt]
# pip install --force-reinstall bcrypt==4.1.3
# ta to var izdarit, todo pachekot kada versija tad ir passlib un pielikt requirements
# man bail aiztikt georgijs dusmigs paliks vel :(

@app.get("/")
def root():
    return {"message": "Welcome to the Diet Optimization API"}
