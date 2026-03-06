from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from config.settings import settings
from api.middleware.cors import setup_cors
from api.middleware.rate_limit import limiter
from api.routes import health

def create_app() -> FastAPI:
    # Initialize the core application
    app = FastAPI(
        title=settings.APP_NAME,
        description="Optimized AI Academic Literature Intelligence System",
        version="1.0.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc"
    )

    # Apply Security & Middleware
    setup_cors(app)
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # Register API Routes
    app.include_router(health.router, prefix="/api/v1")
    
    # Placeholder for future routes (we will uncomment these soon)
    # app.include_router(search.router, prefix="/api/v1/search")
    # app.include_router(extractions.router, prefix="/api/v1/extract")

    return app

# The instance Uvicorn/Render will run
app = create_app()
