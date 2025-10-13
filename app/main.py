from fastapi import FastAPI
from app.routers import productRouter
from app.routers import menuRouter
from app.routers import mainPageRouter
from app.routers import userProductRouter
from app.routers import consumedProductRouter
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

@app.get("/")
def root():
    return {"message": "Welcome to the Diet Optimization API"}
