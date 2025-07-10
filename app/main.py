"""
Main FastAPI application
"""

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import os

from .core.config import settings
from .api.companies import router as companies_router
from .api.projects import router as projects_router
from .models.schemas import HealthResponse

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="app/templates")

# Include API routes
app.include_router(
    companies_router, 
    prefix=f"{settings.API_V1_STR}/companies", 
    tags=["companies"]
)
app.include_router(
    projects_router, 
    prefix=f"{settings.API_V1_STR}/projects", 
    tags=["projects"]
)

# Root endpoint - serves the main application
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serve the main application page"""
    return templates.TemplateResponse("index.html", {"request": request})

# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        message="Project Finder API is running"
    )

# API info endpoint
@app.get(f"{settings.API_V1_STR}/info")
async def get_api_info():
    """Get API information"""
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "description": settings.PROJECT_DESCRIPTION,
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }

# Catch-all for SPA routing
@app.get("/{path:path}", response_class=HTMLResponse)
async def catch_all(request: Request, path: str):
    """Catch-all route for SPA routing"""
    # For API routes, return 404
    if path.startswith("api/"):
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Not found")
    
    # For all other routes, serve the main app
    return templates.TemplateResponse("index.html", {"request": request})
