from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager
from app.routers import productRouter, menuRouter, mainPageRouter, userProductRouter, consumedProductRouter, statisticsRouter, userRouter, recipeRouter
from app.dependencies.firefoxDriver import init_firefox_pool, get_firefox_pool
from app.services.profileService import needs_completion
from app.services.userService import decode_access_token
from app.database import SessionLocal
from app.models.users import User
from fastapi.middleware.cors import CORSMiddleware


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

# Enable CORS for React frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
    - Redirecting auth pages for logged-in users
    """
    path = request.url.path
    tok = request.cookies.get(COOKIE)

    # root redirect
    if path == "/":
        return RedirectResponse("/mainPage" if tok else "/auth/login")

    # pages for anonymous users only
    ANON_ONLY_PATHS = ("/auth/login", "/auth/register", "/auth/forgot-password", "/auth/reset-password", "/auth/verify")

    # logged-in user accessing login/register/forgot/reset → redirect to main
    if tok and path.startswith(ANON_ONLY_PATHS):
        return RedirectResponse("/mainPage")

    # allow all public prefixes (e.g. static, assets)
    if path.startswith(PUBLIC_PREFIXES):
        return await call_next(request)

    # protected pages: require token
    if not tok:
        return RedirectResponse("/auth/login")

    # decode & validate token
    try:
        payload = decode_access_token(tok)
        if payload.get("typ") != "access":
            return RedirectResponse("/auth/login")
        user_uuid = int(payload["sub"])
    except Exception:
        return RedirectResponse("/auth/login")

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
