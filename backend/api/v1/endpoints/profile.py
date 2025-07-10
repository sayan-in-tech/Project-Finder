"""
Profile endpoints for company information.
"""

from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from services.gemini_service import gemini_service
from models.project import Company
import structlog

logger = structlog.get_logger()
router = APIRouter()


@router.get("/")
async def get_company_profile(
    company: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get company profile including industry, tech stack, and recent highlights.
    
    Args:
        company: Company name
        db: Database session
        
    Returns:
        Company profile information
    """
    try:
        # Check if company exists in database
        existing_company = db.query(Company).filter(
            Company.name.ilike(f"%{company}%")
        ).first()
        
        if existing_company:
            logger.info(f"Found existing company profile for {company}")
            return {
                "name": existing_company.name,
                "industry": existing_company.industry,
                "tech_stack": existing_company.tech_stack.split(",") if existing_company.tech_stack else [],
                "recent_highlights": existing_company.recent_highlights.split("|") if existing_company.recent_highlights else [],
                "summary": existing_company.profile_summary
            }
        
        # Get profile from Gemini API
        logger.info(f"Getting company profile for {company} from Gemini API")
        profile = await gemini_service.get_company_profile(company)
        
        # Save to database
        new_company = Company(
            name=profile["name"],
            industry=profile.get("industry", ""),
            tech_stack=",".join(profile.get("tech_stack", [])),
            recent_highlights="|".join(profile.get("recent_highlights", [])),
            profile_summary=profile.get("summary", "")
        )
        
        db.add(new_company)
        db.commit()
        db.refresh(new_company)
        
        logger.info(f"Saved company profile for {company}")
        
        return profile
        
    except Exception as e:
        logger.error(f"Error getting company profile for {company}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get company profile: {str(e)}"
        )


@router.get("/search")
async def search_companies(
    query: str,
    limit: int = 10,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Search for companies by name.
    
    Args:
        query: Search query
        limit: Maximum number of results
        db: Database session
        
    Returns:
        List of matching companies
    """
    try:
        companies = db.query(Company).filter(
            Company.name.ilike(f"%{query}%")
        ).limit(limit).all()
        
        return {
            "companies": [
                {
                    "id": company.id,
                    "name": company.name,
                    "industry": company.industry,
                    "summary": company.profile_summary
                }
                for company in companies
            ],
            "total": len(companies)
        }
        
    except Exception as e:
        logger.error(f"Error searching companies with query '{query}': {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to search companies: {str(e)}"
        ) 