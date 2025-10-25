from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager
from app.routers import productRouter, menuRouter, mainPageRouter, userProductRouter, consumedProductRouter, statisticsRouter, userRouter, recipeRouter
from app.dependencies.firefoxDriver import init_firefox_pool, get_firefox_pool
from app.services.profileService import needs_completion
from app.services.userService import decode_access_token
from app.database import SessionLocal
from app.models.users import User

# Lifespn
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
        Startup and shutdown logic for FastAPI application.
        - Initializes a pool of Firefox drivers for scraping tasks.
        - Ensures proper shutdown of the pool on application exit.
    """
    print("Starting application...")
    init_firefox_pool(pool_size=1, geckodriver_path=None, headless=True)
    print("Application startup complete")
    yield # application runs here
    print("Shutting down application...")
    try:
        pool = get_firefox_pool()
        pool.shutdown()
    except RuntimeError:
        pass # ignore if pool was already shutdown
    print("Application shutdown complete")

# Initialize FastAPI
app = FastAPI(
    title="Diet Optimization API",
    description="Backend service",
    lifespan=lifespan
)

# Authentication & public path config
PUBLIC_PREFIXES = (
    "/auth/login", "/auth/register", "/auth/verify",
    "/auth/verification/start", "/auth/verification/confirm",
    "/auth/forgot-password", "/auth/reset-password",
    "/static", "/docs", "/openapi.json",
)
COOKIE = "access_token"

# Middleware: Redirects & Auth
@app.middleware("http")
async def redirects(request: Request, call_next):
    """
        Middleware to handle:
        - Root path redirection
        - Public vs protected routes
        - Logged-in user restrictions
        - Token validation and session checks
        - Enforcing registration completion
    """
    path = request.url.path
    tok = request.cookies.get(COOKIE)

    # root redirect
    if path == "/":
        return RedirectResponse("/mainPage" if tok else "/auth/login")

    # logged-in user should not access login/register
    if tok and (path.startswith("/auth/login") or path.startswith("/auth/register")):
        return RedirectResponse("/mainPage")

    # allow public paths
    if path.startswith(PUBLIC_PREFIXES):
        return await call_next(request)

    # protect all other routes
    if not tok:
        return RedirectResponse("/auth/login")

    # decode token
    try:
        payload = decode_access_token(tok)
        if payload.get("typ") != "access":
            return RedirectResponse("/auth/login")
        user_uuid = int(payload["sub"])
    except Exception:
        return RedirectResponse("/auth/login")

    # enforce registration completion
    if not path.startswith("/auth/complete"):
        db = SessionLocal()
        try:
            u = db.query(User).get(user_uuid)
            if u and needs_completion(u):
                return RedirectResponse("/auth/complete")
        finally:
            db.close()

    return await call_next(request)

# Include routers
app.include_router(productRouter.product, prefix="/products", tags=["products"])
app.include_router(menuRouter.menu, prefix="/menu", tags=["menu"])
app.include_router(mainPageRouter.mainPage, tags=["main_page"])
app.include_router(userProductRouter.userProduct, prefix="/userProducts", tags=["userProducts"])
app.include_router(consumedProductRouter.consumedProduct, prefix="/consumedProducts", tags=["consumedProducts"])
app.include_router(statisticsRouter.statistics, prefix="/statistics", tags=["statistics"])
app.include_router(userRouter.user, prefix="/auth", tags=["auth"])
app.include_router(recipeRouter.recipes, prefix="/recipes", tags=["recipes"])

# Catch-all routes
@app.get("/{full_path:path}")
async def catch_all(full_path: str, request: Request):
    """
        Redirect any unmatched route to main page or login depending on token presence.
    """
    tok = request.cookies.get(COOKIE)
    return RedirectResponse("/mainPage" if tok else "/auth/login")

@app.get("/")
def root():
    """
        API root: simple welcome message.
    """
    return {"message": "Welcome to the Diet Optimization API"}
