from fastapi import FastAPI
from app.routers import productRouter
from app.routers import menuRouter
from app.routers import mainPageRouter
from app.routers import userProductRouter
from app.routers import consumedProductRouter
from app.routers import statisticsRouter
from app.routers import userRouter
from contextlib import asynccontextmanager
from app.dependencies.firefoxDriver import init_firefox_pool, get_firefox_pool


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application lifecycle:
    - Startup: Initialize webdriver pool
    - Shutdown: Close all drivers
    """
    # Startup
    print("Starting application...")
    init_firefox_pool(
        pool_size=1,  # Number of concurrent scrapers
        geckodriver_path=None,  # Set to path if needed, e.g., r"C:\path\to\geckodriver.exe"
        headless=True  # Run Firefox in headless mode
    )
    print("Application startup complete")

    yield

    # Shutdown
    print("Shutting down application...")
    try:
        pool = get_firefox_pool()
        pool.shutdown()
    except RuntimeError:
        pass
    print("Application shutdown complete")

app = FastAPI(
    title="Diet Optimization API",
    description="Backend service",
    lifespan=lifespan
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

@app.get("/")
def root():
    return {"message": "Welcome to the Diet Optimization API"}
