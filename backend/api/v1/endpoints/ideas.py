"""
Ideas endpoints for project ideas generation.
"""

from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from services.gemini_service import gemini_service
from models.project import Company, Challenge, Project
import structlog

logger = structlog.get_logger()
router = APIRouter()


@router.get("/")
async def get_project_ideas(
    company: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get project ideas for a company based on their engineering challenges.
    
    Args:
        company: Company name
        db: Database session
        
    Returns:
        List of project ideas
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
        
        # Get challenges for the company
        challenges = db.query(Challenge).filter(
            Challenge.company_id == company_obj.id
        ).all()
        
        if not challenges:
            raise HTTPException(
                status_code=404,
                detail=f"No challenges found for {company}. Please get challenges first."
            )
        
        # Check if projects already exist
        existing_projects = db.query(Project).filter(
            Project.company_id == company_obj.id
        ).all()
        
        if existing_projects:
            logger.info(f"Found existing projects for {company}")
            return {
                "company": company_obj.name,
                "projects": [
                    {
                        "id": project.id,
                        "title": project.title,
                        "description": project.description,
                        "tech_stack": project.tech_stack.split(",") if project.tech_stack else [],
                        "demo_hook": project.demo_hook,
                        "difficulty": project.difficulty,
                        "estimated_duration": project.estimated_duration,
                        "challenge_category": project.challenge.category if project.challenge else None
                    }
                    for project in existing_projects
                ]
            }
        
        # Convert challenges to format expected by Gemini
        challenges_data = [
            {
                "title": challenge.title,
                "description": challenge.description,
                "category": challenge.category,
                "difficulty": challenge.difficulty
            }
            for challenge in challenges
        ]
        
        # Get project ideas from Gemini API
        logger.info(f"Getting project ideas for {company} from Gemini API")
        projects_data = await gemini_service.get_project_ideas(company, challenges_data)
        
        # Save projects to database
        projects = []
        for project_data in projects_data:
            # Find corresponding challenge
            challenge = next(
                (c for c in challenges if c.title == project_data.get("challenge_category", "")),
                None
            )
            
            project = Project(
                company_id=company_obj.id,
                challenge_id=challenge.id if challenge else None,
                title=project_data["title"],
                description=project_data["description"],
                tech_stack=",".join(project_data.get("tech_stack", [])),
                demo_hook=project_data["demo_hook"],
                difficulty=project_data.get("difficulty", "medium"),
                estimated_duration=project_data.get("estimated_duration", "2-3 weeks")
            )
            db.add(project)
            projects.append(project)
        
        db.commit()
        
        # Refresh to get IDs
        for project in projects:
            db.refresh(project)
        
        logger.info(f"Saved {len(projects)} projects for {company}")
        
        return {
            "company": company_obj.name,
            "projects": [
                {
                    "id": project.id,
                    "title": project.title,
                    "description": project.description,
                    "tech_stack": project.tech_stack.split(",") if project.tech_stack else [],
                    "demo_hook": project.demo_hook,
                    "difficulty": project.difficulty,
                    "estimated_duration": project.estimated_duration,
                    "challenge_category": project.challenge.category if project.challenge else None
                }
                for project in projects
            ]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting project ideas for {company}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get project ideas: {str(e)}"
        )


@router.get("/by-challenge/{challenge_id}")
async def get_ideas_by_challenge(
    challenge_id: int,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get project ideas for a specific challenge.
    
    Args:
        challenge_id: Challenge ID
        db: Database session
        
    Returns:
        List of project ideas for the challenge
    """
    try:
        challenge = db.query(Challenge).filter(Challenge.id == challenge_id).first()
        if not challenge:
            raise HTTPException(
                status_code=404,
                detail=f"Challenge with ID {challenge_id} not found"
            )
        
        projects = db.query(Project).filter(
            Project.challenge_id == challenge_id
        ).all()
        
        return {
            "challenge": {
                "id": challenge.id,
                "title": challenge.title,
                "description": challenge.description,
                "category": challenge.category,
                "difficulty": challenge.difficulty
            },
            "projects": [
                {
                    "id": project.id,
                    "title": project.title,
                    "description": project.description,
                    "tech_stack": project.tech_stack.split(",") if project.tech_stack else [],
                    "demo_hook": project.demo_hook,
                    "difficulty": project.difficulty,
                    "estimated_duration": project.estimated_duration
                }
                for project in projects
            ]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting ideas for challenge ID {challenge_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get project ideas: {str(e)}"
        )


@router.post("/regenerate")
async def regenerate_ideas(
    company: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Regenerate project ideas for a company.
    
    Args:
        company: Company name
        db: Database session
        
    Returns:
        New list of project ideas
    """
    try:
        # Delete existing projects for the company
        company_obj = db.query(Company).filter(
            Company.name.ilike(f"%{company}%")
        ).first()
        
        if not company_obj:
            raise HTTPException(
                status_code=404,
                detail=f"Company '{company}' not found"
            )
        
        # Delete existing projects
        db.query(Project).filter(Project.company_id == company_obj.id).delete()
        db.commit()
        
        # Get new ideas
        return await get_project_ideas(company, db)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error regenerating ideas for {company}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to regenerate project ideas: {str(e)}"
        ) 