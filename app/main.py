from fastapi import FastAPI
from app.routers import productRouter
from app.routers import menuRouter
from app.routers import mainPageRouter
from app.routers import userProductRouter

app = FastAPI(
    title="Diet Optimization API",
    description="Backend service"
)

# Include routers
app.include_router(productRouter.showProducts, prefix="/products", tags=["products"])
app.include_router(productRouter.productsNames, prefix="/products", tags=["products"])
app.include_router(menuRouter.generateMenu, prefix ="/menu", tags=["menu"])
app.include_router(menuRouter.showMenuForm, prefix="/menu", tags=["menu"])
app.include_router(menuRouter.saveMenu, prefix="/menu", tags=["menu"])
app.include_router(menuRouter.getUserMenus, prefix="/menu", tags=["menu"])
app.include_router(menuRouter.getSingleUserMenu, prefix="/menu", tags=["menu"])
app.include_router(mainPageRouter.showMainPage, tags=["main_page"])
app.include_router(userProductRouter.showUserProducts, prefix="/userProducts", tags=["userProducts"])
app.include_router(userProductRouter.userProductsNames, prefix="/userProducts", tags=["userProducts"])
app.include_router(userProductRouter.addUserProduct, prefix="/userProducts", tags=["userProducts"])
app.include_router(userProductRouter.getUserProducts, prefix="/userProducts", tags=["userProducts"])

@app.get("/")
def root():
    return {"message": "Welcome to the Diet Optimization API"}
