"""
Projects endpoints for managing saved projects.
"""

from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from models.project import Project, Company
import structlog

logger = structlog.get_logger()
router = APIRouter()


@router.get("/")
async def get_saved_projects(
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get all saved projects.
    
    Args:
        db: Database session
        
    Returns:
        List of saved projects
    """
    try:
        projects = db.query(Project).filter(Project.is_saved == True).all()
        
        return {
            "projects": [
                {
                    "id": project.id,
                    "title": project.title,
                    "description": project.description,
                    "tech_stack": project.tech_stack.split(",") if project.tech_stack else [],
                    "demo_hook": project.demo_hook,
                    "difficulty": project.difficulty,
                    "estimated_duration": project.estimated_duration,
                    "company": project.company.name if project.company else None,
                    "user_notes": project.user_notes,
                    "created_at": project.created_at.isoformat() if project.created_at else None
                }
                for project in projects
            ],
            "total": len(projects)
        }
        
    except Exception as e:
        logger.error(f"Error getting saved projects: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get saved projects: {str(e)}"
        )


@router.post("/save/{project_id}")
async def save_project(
    project_id: int,
    notes: str = None,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Save a project to workspace.
    
    Args:
        project_id: Project ID
        notes: Optional user notes
        db: Database session
        
    Returns:
        Saved project information
    """
    try:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(
                status_code=404,
                detail=f"Project with ID {project_id} not found"
            )
        
        project.is_saved = True
        if notes:
            project.user_notes = notes
        
        db.commit()
        db.refresh(project)
        
        logger.info(f"Saved project {project_id}")
        
        return {
            "id": project.id,
            "title": project.title,
            "description": project.description,
            "tech_stack": project.tech_stack.split(",") if project.tech_stack else [],
            "demo_hook": project.demo_hook,
            "difficulty": project.difficulty,
            "estimated_duration": project.estimated_duration,
            "company": project.company.name if project.company else None,
            "user_notes": project.user_notes,
            "is_saved": project.is_saved
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error saving project {project_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save project: {str(e)}"
        )


@router.delete("/{project_id}")
async def delete_saved_project(
    project_id: int,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Remove a project from saved workspace.
    
    Args:
        project_id: Project ID
        db: Database session
        
    Returns:
        Success message
    """
    try:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(
                status_code=404,
                detail=f"Project with ID {project_id} not found"
            )
        
        project.is_saved = False
        project.user_notes = None
        
        db.commit()
        
        logger.info(f"Removed project {project_id} from saved workspace")
        
        return {
            "message": f"Project '{project.title}' removed from saved workspace"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error removing project {project_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to remove project: {str(e)}"
        )


@router.delete("/clear")
async def clear_saved_projects(
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Clear all saved projects from workspace.
    
    Args:
        db: Database session
        
    Returns:
        Success message
    """
    try:
        saved_projects = db.query(Project).filter(Project.is_saved == True).all()
        count = len(saved_projects)
        
        for project in saved_projects:
            project.is_saved = False
            project.user_notes = None
        
        db.commit()
        
        logger.info(f"Cleared {count} saved projects")
        
        return {
            "message": f"Cleared {count} projects from saved workspace"
        }
        
    except Exception as e:
        logger.error(f"Error clearing saved projects: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to clear saved projects: {str(e)}"
        )


@router.put("/{project_id}/notes")
async def update_project_notes(
    project_id: int,
    notes: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Update user notes for a saved project.
    
    Args:
        project_id: Project ID
        notes: New notes
        db: Database session
        
    Returns:
        Updated project information
    """
    try:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(
                status_code=404,
                detail=f"Project with ID {project_id} not found"
            )
        
        if not project.is_saved:
            raise HTTPException(
                status_code=400,
                detail="Can only update notes for saved projects"
            )
        
        project.user_notes = notes
        db.commit()
        db.refresh(project)
        
        logger.info(f"Updated notes for project {project_id}")
        
        return {
            "id": project.id,
            "title": project.title,
            "user_notes": project.user_notes,
            "updated_at": project.updated_at.isoformat() if project.updated_at else None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating notes for project {project_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update project notes: {str(e)}"
        )


@router.get("/by-company/{company_name}")
async def get_projects_by_company(
    company_name: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get all projects for a specific company.
    
    Args:
        company_name: Company name
        db: Database session
        
    Returns:
        List of projects for the company
    """
    try:
        company = db.query(Company).filter(
            Company.name.ilike(f"%{company_name}%")
        ).first()
        
        if not company:
            raise HTTPException(
                status_code=404,
                detail=f"Company '{company_name}' not found"
            )
        
        projects = db.query(Project).filter(Project.company_id == company.id).all()
        
        return {
            "company": {
                "id": company.id,
                "name": company.name,
                "industry": company.industry
            },
            "projects": [
                {
                    "id": project.id,
                    "title": project.title,
                    "description": project.description,
                    "tech_stack": project.tech_stack.split(",") if project.tech_stack else [],
                    "demo_hook": project.demo_hook,
                    "difficulty": project.difficulty,
                    "estimated_duration": project.estimated_duration,
                    "is_saved": project.is_saved,
                    "user_notes": project.user_notes
                }
                for project in projects
            ],
            "total": len(projects)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting projects for company {company_name}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get projects: {str(e)}"
        ) 