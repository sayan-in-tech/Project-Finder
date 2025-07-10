"""
Challenges endpoints for engineering challenges.
"""

from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from services.gemini_service import gemini_service
from models.project import Company, Challenge
import structlog

logger = structlog.get_logger()
router = APIRouter()


@router.get("/")
async def get_engineering_challenges(
    company: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get engineering challenges for a company.
    
    Args:
        company: Company name
        db: Database session
        
    Returns:
        List of engineering challenges
    """
    try:
        # Get company from database
        company_obj = db.query(Company).filter(
            Company.name.ilike(f"%{company}%")
        ).first()
        
        if not company_obj:
            raise HTTPException(
                status_code=404,
                detail=f"Company '{company}' not found. Please get company profile first."
            )
        
        # Check if challenges already exist
        existing_challenges = db.query(Challenge).filter(
            Challenge.company_id == company_obj.id
        ).all()
        
        if existing_challenges:
            logger.info(f"Found existing challenges for {company}")
            return {
                "company": company_obj.name,
                "challenges": [
                    {
                        "id": challenge.id,
                        "title": challenge.title,
                        "description": challenge.description,
                        "category": challenge.category,
                        "difficulty": challenge.difficulty
                    }
                    for challenge in existing_challenges
                ]
            }
        
        # Get company profile for context
        profile = {
            "name": company_obj.name,
            "industry": company_obj.industry,
            "tech_stack": company_obj.tech_stack.split(",") if company_obj.tech_stack else [],
            "recent_highlights": company_obj.recent_highlights.split("|") if company_obj.recent_highlights else [],
            "summary": company_obj.profile_summary
        }
        
        # Get challenges from Gemini API
        logger.info(f"Getting engineering challenges for {company} from Gemini API")
        challenges_data = await gemini_service.get_engineering_challenges(company, profile)
        
        # Save challenges to database
        challenges = []
        for challenge_data in challenges_data:
            challenge = Challenge(
                company_id=company_obj.id,
                title=challenge_data["title"],
                description=challenge_data["description"],
                category=challenge_data.get("category", "general"),
                difficulty=challenge_data.get("difficulty", "medium")
            )
            db.add(challenge)
            challenges.append(challenge)
        
        db.commit()
        
        # Refresh to get IDs
        for challenge in challenges:
            db.refresh(challenge)
        
        logger.info(f"Saved {len(challenges)} challenges for {company}")
        
        return {
            "company": company_obj.name,
            "challenges": [
                {
                    "id": challenge.id,
                    "title": challenge.title,
                    "description": challenge.description,
                    "category": challenge.category,
                    "difficulty": challenge.difficulty
                }
                for challenge in challenges
            ]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting challenges for {company}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get engineering challenges: {str(e)}"
        )


@router.get("/by-company/{company_id}")
async def get_challenges_by_company(
    company_id: int,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get challenges for a specific company by ID.
    
    Args:
        company_id: Company ID
        db: Database session
        
    Returns:
        List of challenges for the company
    """
    try:
        company = db.query(Company).filter(Company.id == company_id).first()
        if not company:
            raise HTTPException(
                status_code=404,
                detail=f"Company with ID {company_id} not found"
            )
        
        challenges = db.query(Challenge).filter(
            Challenge.company_id == company_id
        ).all()
        
        return {
            "company": {
                "id": company.id,
                "name": company.name,
                "industry": company.industry
            },
            "challenges": [
                {
                    "id": challenge.id,
                    "title": challenge.title,
                    "description": challenge.description,
                    "category": challenge.category,
                    "difficulty": challenge.difficulty
                }
                for challenge in challenges
            ]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting challenges for company ID {company_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get challenges: {str(e)}"
        ) 