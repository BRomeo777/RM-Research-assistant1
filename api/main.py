from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

# Import configuration
from config.settings import settings

# Import middleware
from api.middleware.cors import setup_cors
from api.middleware.rate_limit import limiter

# Import routes
from api.routes import health
from api.routes import search
from api.routes import extractions  # <-- NEW: Imported the extractions route
# from api.routes import maps, manuscripts, integrity (Placeholder for future phases)

def create_app() -> FastAPI:
    """
    Application factory pattern. 
    This makes the app highly modular and easy to test as the project grows.
    """
    # 1. Initialize the core FastAPI application
    app = FastAPI(
        title=settings.APP_NAME,
        description="Optimized AI Academic Literature Intelligence System",
        version="1.0.0",
        docs_url="/api/docs",   # Swagger UI dashboard
        redoc_url="/api/redoc"  # Alternative API documentation
    )

    # 2. Apply Security & Middleware
    setup_cors(app)
    
    # Attach the rate limiter to the app state to protect against spam
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # 3. Register API Routes
    # The health check route (for Render deployments and system diagnostics)
    app.include_router(health.router, prefix="/api/v1")
    
    # The Phase 2 Seed Intelligence search route
    app.include_router(search.router, prefix="/api/v1/search")
    
    # NEW: Activating the TrialSieve Extraction Route
    app.include_router(extractions.router, prefix="/api/v1/extract")

    return app

# The instance that Uvicorn and Render will run
app = create_app()
