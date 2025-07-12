"""
API routes for company analysis
"""

from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from ..models.schemas import (
    CompanyAnalysisRequest,
    CompanyAnalysisResponse,
    CompanyProfile,
    EngineeringChallenge,
    ErrorResponse
)
from ..services.company_service import CompanyAnalysisService
from ..services.website_parser import crawl_summarize_and_preview_tokens

router = APIRouter()


@router.post(
    "/analyze-company",
    response_model=CompanyAnalysisResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="Analyze Company",
    description="Analyze a company and generate engineering challenges and project ideas"
)
async def analyze_company(
    request: CompanyAnalysisRequest,
):
    """
    Analyze a company and return comprehensive analysis including:
    - Company profile
    - Engineering challenges
    - Project ideas
    """
    try:
        # Initialize services
        from ..services.project_service import ProjectGenerationService
        company_service = CompanyAnalysisService(request.api_key)
        project_service = ProjectGenerationService(request.api_key)
        
        # Analyze company
        company_profile = await company_service.analyze_company(request.company_name, request.additional_info, request.website_url)
        if not company_profile:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to analyze company: {request.company_name}"
            )
        
        # Get engineering challenges
        challenges = await company_service.get_engineering_challenges(
            request.company_name, 
            company_profile
        )
        
        # Generate project ideas
        projects = await project_service.generate_projects_for_company(
            company_name=request.company_name,
            company_profile=company_profile,
            challenges=challenges,
            total_ideas=request.total_ideas,
            user_skills=request.user_skills
        )
        
        # Create response
        response = CompanyAnalysisResponse(
            company_profile=company_profile,
            engineering_challenges=challenges,
            project_ideas=projects
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
    "/preview-tokens",
    response_model=dict,
    summary="Preview Gemini Token Usage",
    description="Preview the summary and Gemini token count before generating company analysis."
)
async def preview_tokens(
    request: CompanyAnalysisRequest,
):
    """
    Preview the summary and Gemini token count that would be sent to Gemini for company analysis.
    """
    try:
        if not request.website_url:
            return {"summary": None, "token_count": 0}
        preview = crawl_summarize_and_preview_tokens(
            start_url=request.website_url,
            api_key=request.api_key
        )
        return preview
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get(
    "/company-profile/{company_name}",
    response_model=CompanyProfile,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="Get Company Profile",
    description="Get detailed profile information for a specific company"
)
async def get_company_profile(
    company_name: str,
    api_key: str,
):
    """
    Get company profile information only
    """
    try:
        company_service = CompanyAnalysisService(api_key)
        company_profile = await company_service.analyze_company(company_name)
        
        if not company_profile:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to analyze company: {company_name}"
            )
        
        return company_profile
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get(
    "/engineering-challenges/{company_name}",
    response_model=List[EngineeringChallenge],
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="Get Engineering Challenges",
    description="Get engineering challenges for a specific company"
)
async def get_engineering_challenges(
    company_name: str,
    api_key: str,
):
    """
    Get engineering challenges for a company
    """
    try:
        company_service = CompanyAnalysisService(api_key)
        
        # First get company profile
        company_profile = await company_service.analyze_company(company_name)
        if not company_profile:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to analyze company: {company_name}"
            )
        
        # Get challenges
        challenges = await company_service.get_engineering_challenges(
            company_name, 
            company_profile
        )
        
        return challenges
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get(
    "/company-insights/{company_name}",
    response_model=dict,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="Get Company Insights",
    description="Get additional insights and analytics for a company"
)
async def get_company_insights(
    company_name: str,
    api_key: str,
):
    """
    Get additional insights about a company
    """
    try:
        company_service = CompanyAnalysisService(api_key)
        insights = await company_service.get_company_insights(company_name)
        
        return insights
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )
