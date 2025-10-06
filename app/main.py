from fastapi import FastAPI
from app.routers import productRouter

app = FastAPI(
    title="Diet Optimization API",
    description="Backend service"
)

# Include routers
app.include_router(productRouter.router, prefix="/products", tags=["products"])

@app.get("/")
def root():
    return {"message": "Welcome to the Diet Optimization API"}
