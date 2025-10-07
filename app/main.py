from fastapi import FastAPI
from app.routers import productRouter
from app.routers import algorithmRouter

app = FastAPI(
    title="Diet Optimization API",
    description="Backend service"
)

# Include routers
app.include_router(productRouter.router, prefix="/products", tags=["products"])
app.include_router(algorithmRouter.router, tags=["menu"])

@app.get("/")
def root():
    return {"message": "Welcome to the Diet Optimization API"}
