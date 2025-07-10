"""
Main API router for v1 endpoints.
"""

from fastapi import APIRouter

from api.v1.endpoints import profile, challenges, ideas, projects

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(profile.router, prefix="/profile", tags=["profile"])
api_router.include_router(challenges.router, prefix="/challenges", tags=["challenges"])
api_router.include_router(ideas.router, prefix="/ideas", tags=["ideas"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"]) 