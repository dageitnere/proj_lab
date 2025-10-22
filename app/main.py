from fastapi import FastAPI, Request
from app.routers import productRouter
from app.routers import menuRouter
from app.routers import mainPageRouter
from app.routers import userProductRouter
from app.routers import consumedProductRouter
from app.routers import statisticsRouter
from app.routers import userRouter
from contextlib import asynccontextmanager
from app.routers import recipeRouter
from app.dependencies.firefoxDriver import init_firefox_pool, get_firefox_pool
from fastapi.responses import RedirectResponse
from app.services.userService import decode_access_token

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

PUBLIC_PREFIXES = ("/auth/login", "/auth/register", "/static", "/docs", "/openapi.json")
COOKIE = "access_token"

@app.middleware("http")
async def redirects(request: Request, call_next):
    path = request.url.path
    tok = request.cookies.get(COOKIE)

    # root redirect
    if path == "/":
        return RedirectResponse("/mainPage" if tok else "/auth/login")

    # if logged-in user tries to access login/register, redirect to mainPage
    if tok and (path.startswith("/auth/login") or path.startswith("/auth/register")):
        return RedirectResponse("/mainPage")

    # public paths
    if path.startswith(PUBLIC_PREFIXES):
        return await call_next(request)

    # protect everything else
    if not tok:
        return RedirectResponse("/auth/login")

    try:
        payload = decode_access_token(tok)
        if payload.get("typ") != "access":
            return RedirectResponse("/auth/login")
    except Exception:
        return RedirectResponse("/auth/login")

    return await call_next(request)

# Include routers
app.include_router(productRouter.product, prefix="/products", tags=["products"])
app.include_router(menuRouter.menu, prefix ="/menu", tags=["menu"])
app.include_router(mainPageRouter.mainPage, tags=["main_page"])
app.include_router(userProductRouter.userProduct, prefix="/userProducts", tags=["userProducts"])
app.include_router(consumedProductRouter.consumedProduct, prefix="/consumedProducts", tags=["consumedProducts"])
app.include_router(statisticsRouter.statistics, prefix="/statistics", tags=["statistics"])
app.include_router(userRouter.user, prefix="/auth", tags=["auth"])
app.include_router(recipeRouter.recipes, prefix="/recipes", tags=["recipes"])


# --- Catch-all route for unmatched URLs ---
@app.get("/{full_path:path}")
async def catch_all(full_path: str, request: Request):
    tok = request.cookies.get(COOKIE)
    # Redirect based on auth state
    return RedirectResponse("/mainPage" if tok else "/auth/login")

# testesanai - lai izvada hashotu paroli, kas registracija saglabatos db
#from passlib.context import CryptContext
#pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
#hashed = pwd.hash("fitness")
#print(hashed)

@app.get("/")
def root():
    return {"message": "Welcome to the Diet Optimization API"}
