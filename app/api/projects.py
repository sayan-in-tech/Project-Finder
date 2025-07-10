"""
API routes for project generation and management
"""

from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from ..models.schemas import (
    ProjectGenerationRequest,
    ProjectGenerationResponse,
    ProjectRefinementRequest,
    ProjectIdea,
    ErrorResponse
)
from ..services.project_service import ProjectGenerationService
from ..services.company_service import CompanyAnalysisService

router = APIRouter()


@router.post(
    "/generate-projects",
    response_model=ProjectGenerationResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="Generate Projects",
    description="Generate project ideas based on company challenges"
)
async def generate_projects(
    request: ProjectGenerationRequest,
):
    """
    Generate project ideas for a company based on engineering challenges
    """
    try:
        # Initialize services
        company_service = CompanyAnalysisService(request.api_key)
        project_service = ProjectGenerationService(request.api_key)
        
        # Get company profile first
        company_profile = await company_service.analyze_company(request.company_name)
        if not company_profile:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to analyze company: {request.company_name}"
            )
        
        # Convert challenge strings to challenge objects
        challenges = []
        for i, challenge_desc in enumerate(request.challenges):
            from ..models.schemas import EngineeringChallenge
            challenge = EngineeringChallenge(
                id=f"challenge_{i}",
                title=f"Challenge {i+1}",
                description=challenge_desc,
                difficulty="intermediate",
                relevance_score=0.8,
                tech_areas=[]
            )
            challenges.append(challenge)
        
        # Generate projects
        projects = await project_service.generate_projects_for_company(
            company_name=request.company_name,
            company_profile=company_profile,
            challenges=challenges,
            total_ideas=len(request.challenges) * request.ideas_per_challenge,
            user_skills=request.user_skills
        )
        
        # Create response
        response = ProjectGenerationResponse(
            projects=projects,
            total_projects=len(projects)
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.post(
    "/refine-project",
    response_model=ProjectIdea,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="Refine Project",
    description="Refine an existing project idea"
)
async def refine_project(
    request: ProjectRefinementRequest,
):
    """
    Refine an existing project idea with additional context
    """
    try:
        # Initialize services
        company_service = CompanyAnalysisService(request.api_key)
        project_service = ProjectGenerationService(request.api_key)
        
        # Get company profile
        company_profile = await company_service.analyze_company(request.company_name)
        if not company_profile:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to analyze company: {request.company_name}"
            )
        
        # Create challenge object
        from ..models.schemas import EngineeringChallenge
        challenge = EngineeringChallenge(
            id=request.project.challenge_id,
            title=request.project.challenge_title,
            description=request.challenge_description,
            difficulty="intermediate",
            relevance_score=0.8,
            tech_areas=[]
        )
        
        # Refine project
        refined_project = await project_service.refine_project_idea(
            project=request.project,
            company_name=request.company_name,
            company_profile=company_profile,
            challenge=challenge
        )
        
        if not refined_project:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to refine project"
            )
        
        return refined_project
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get(
    "/project-suggestions",
    response_model=List[str],
    responses={
        500: {"model": ErrorResponse}
    },
    summary="Get Project Suggestions",
    description="Get general project suggestions based on user preferences"
)
async def get_project_suggestions(
    user_skills: Optional[List[str]] = None,
    preferred_difficulty: str = "intermediate",
    max_duration: str = "3 months",
):
    """
    Get project suggestions based on user preferences
    """
    try:
        # For now, we'll use a dummy API key since this doesn't need AI
        project_service = ProjectGenerationService("dummy")
        
        suggestions = await project_service.get_project_suggestions(
            user_skills=user_skills or [],
            preferred_difficulty=preferred_difficulty,
            max_duration=max_duration
        )
        
        return suggestions
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.post(
    "/generate-variations/{project_id}",
    response_model=List[ProjectIdea],
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="Generate Project Variations",
    description="Generate variations of an existing project idea"
)
async def generate_project_variations(
    project_id: str,
    base_project: ProjectIdea,
    api_key: str,
    variation_count: int = 3,
):
    """
    Generate variations of an existing project idea
    """
    try:
        project_service = ProjectGenerationService(api_key)
        variations = await project_service.generate_project_variations(
            base_project=base_project,
            company_name="Unknown Company",
            variation_count=variation_count
        )
        
        return variations
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )
