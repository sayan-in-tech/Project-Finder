"""
Project generation service for the FastAPI application
"""

import asyncio
import sys
import os
from typing import List, Optional

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.models.schemas import ProjectIdea, CompanyProfile, EngineeringChallenge
from .gemini_service import GeminiService


class ProjectGenerationService:
    """Service for generating and refining project ideas"""
    
    def __init__(self, api_key: str):
        self.gemini_service = GeminiService(api_key)
        self.api_key = api_key
    
    async def generate_projects_for_company(
        self,
        company_name: str,
        company_profile: CompanyProfile,
        challenges: List[EngineeringChallenge],
        total_ideas: int = 4,
        user_skills: Optional[List[str]] = None
    ) -> List[ProjectIdea]:
        """
        Generate project ideas for a company
        """
        try:
            # Convert challenges to dict format for Gemini service
            challenges_data = [
                {
                    'title': challenge.title,
                    'description': challenge.description,
                    'difficulty': challenge.difficulty,
                    'tech_areas': challenge.tech_areas
                }
                for challenge in challenges
            ]
            
            # Run the Gemini service in a thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            projects_data = await loop.run_in_executor(
                None, 
                self.gemini_service.generate_project_ideas,
                company_name,
                challenges_data,
                user_skills,
                total_ideas
            )
            
            # Convert the raw data to ProjectIdea models
            return [self._convert_to_project_idea(project_data) for project_data in projects_data]
            
        except Exception as e:
            print(f"Error generating projects for {company_name}: {e}")
            return []
    
    async def refine_project_idea(
        self,
        project: ProjectIdea,
        company_name: str,
        company_profile: CompanyProfile,
        challenge: EngineeringChallenge
    ) -> Optional[ProjectIdea]:
        """
        Refine an existing project idea
        """
        try:
            # Convert project and challenge to dict format
            project_data = {
                'title': project.title,
                'description': project.description,
                'difficulty': project.difficulty,
                'estimated_duration': project.estimated_duration,
                'tech_stack': project.tech_stack,
                'learning_outcomes': project.learning_outcomes,
                'challenge_id': project.challenge_id,
                'challenge_title': project.challenge_title
            }
            
            challenge_data = {
                'title': challenge.title,
                'description': challenge.description,
                'difficulty': challenge.difficulty,
                'tech_areas': challenge.tech_areas
            }
            
            # Run the Gemini service in a thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            refined_project_data = await loop.run_in_executor(
                None, 
                self.gemini_service.refine_project_idea,
                project_data,
                company_name,
                challenge_data
            )
            
            # Convert the refined data back to ProjectIdea model
            return self._convert_to_project_idea(refined_project_data)
            
        except Exception as e:
            print(f"Error refining project {project.title}: {e}")
            return None
    
    async def generate_project_variations(
        self,
        base_project: ProjectIdea,
        company_name: str,
        variation_count: int = 3
    ) -> List[ProjectIdea]:
        """
        Generate variations of a base project idea
        """
        try:
            # This could be implemented to create slight variations
            # For now, return empty list as placeholder
            return []
        except Exception as e:
            print(f"Error generating variations for {base_project.title}: {e}")
            return []
    
    async def get_project_suggestions(
        self,
        user_skills: List[str],
        preferred_difficulty: str = "intermediate",
        max_duration: str = "3 months"
    ) -> List[str]:
        """
        Get project suggestions based on user preferences
        """
        try:
            # This could be expanded to provide personalized suggestions
            # For now, return some general suggestions
            suggestions = [
                "Build a full-stack web application",
                "Create a mobile app with React Native",
                "Develop a machine learning model",
                "Build a microservices architecture",
                "Create a real-time chat application"
            ]
            return suggestions
        except Exception as e:
            print(f"Error getting project suggestions: {e}")
            return []
    
    def _convert_to_project_idea(self, data: dict) -> ProjectIdea:
        """Convert raw project data to ProjectIdea model"""
        return ProjectIdea(
            id=data.get('id', 'project_1'),
            title=data.get('title', 'Project Title'),
            description=data.get('description', 'Project description'),
            difficulty=data.get('difficulty', 'intermediate'),
            estimated_duration=data.get('estimated_duration', '2-3 months'),
            tech_stack=data.get('tech_stack', []),
            learning_outcomes=data.get('learning_outcomes', []),
            challenge_id=data.get('challenge_id', 'challenge_1'),
            challenge_title=data.get('challenge_title', 'Challenge Title')
        )
