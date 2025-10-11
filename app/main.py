from fastapi import FastAPI
from app.routers import productRouter
from app.routers import algorithmRouter
from app.routers import mainPageRouter

app = FastAPI(
    title="Diet Optimization API",
    description="Backend service"
)

# Include routers
app.include_router(productRouter.showProducts, prefix="/products", tags=["products"])
app.include_router(productRouter.productsNames, prefix="/products", tags=["products"])
app.include_router(algorithmRouter.generateMenu, prefix ="/menu", tags=["menu"])
app.include_router(algorithmRouter.showMenuForm, prefix="/menu", tags=["menu"])
app.include_router(mainPageRouter.showMainPage, tags=["main_page"])

@app.get("/")
def root():
    return {"message": "Welcome to the Diet Optimization API"}
