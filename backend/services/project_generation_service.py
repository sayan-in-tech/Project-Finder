"""
Service for generating project ideas based on company analysis
"""

import json
import logging
from typing import List, Optional, Dict, Any
import google.generativeai as genai
from ..models.models import (
    ProjectIdea, 
    CompanyProfile, 
    EngineeringChallenge,
    ProjectGenerationRequest,
    ProjectGenerationResponse
)
from ..prompts.project_generation import PROJECT_GENERATION_PROMPT, PROJECT_REFINEMENT_PROMPT

logger = logging.getLogger(__name__)

class ProjectGenerationService:
    """Service for generating project ideas based on company analysis"""
    
    def __init__(self, api_key: str):
        """Initialize the service with Gemini API key"""
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def generate_projects_for_company(
        self, 
        company_name: str,
        company_profile: CompanyProfile,
        challenges: List[EngineeringChallenge],
        total_ideas: int = 4,
        user_skills: Optional[List[str]] = None
    ) -> List[ProjectIdea]:
        """
        Generate project ideas for a company based on its challenges
        
        Args:
            company_name: Name of the target company
            company_profile: Analyzed company profile
            challenges: List of engineering challenges
            total_ideas: Total number of ideas to generate (exact count)
            user_skills: Optional list of user's technical skills
            
        Returns:
            List of ProjectIdea objects
        """
        all_projects = []
        
        # Generate exactly total_ideas projects, cycling through challenges
        for i in range(total_ideas):
            # Cycle through challenges
            challenge = challenges[i % len(challenges)]
            
            try:
                projects = self._generate_projects_for_challenge(
                    company_name=company_name,
                    company_profile=company_profile,
                    challenge=challenge,
                    ideas_per_challenge=1,  # Generate 1 project at a time
                    user_skills=user_skills
                )
                all_projects.extend(projects)
                
            except Exception as e:
                logger.error(f"Error generating projects for challenge {challenge.id}: {str(e)}")
                continue
        
        return all_projects
    
    def generate_projects_from_request(self, request: ProjectGenerationRequest) -> ProjectGenerationResponse:
        """
        Generate projects from a structured request
        
        Args:
            request: ProjectGenerationRequest object
            
        Returns:
            ProjectGenerationResponse object
        """
        # This would typically use the company analysis service to get profile and challenges
        # For now, we'll assume they're provided in the request
        projects = []
        
        for challenge in request.challenges:
            # Create a mock challenge object for compatibility
            challenge_obj = EngineeringChallenge(
                id=f"challenge_{len(projects) + 1}",
                title=challenge,
                description=challenge,
                difficulty="intermediate",
                relevance_score=0.8,
                tech_areas=[]
            )
            
            # Generate projects for this challenge
            challenge_projects = self._generate_projects_for_challenge(
                company_name=request.company_name,
                company_profile=None,  # Would be provided in real implementation
                challenge=challenge_obj,
                ideas_per_challenge=request.ideas_per_challenge,
                user_skills=request.user_skills
            )
            
            projects.extend(challenge_projects)
        
        return ProjectGenerationResponse(
            projects=projects,
            total_projects=len(projects)
        )
    
    def refine_project_idea(
        self, 
        project: ProjectIdea, 
        company_name: str, 
        company_profile: CompanyProfile,
        challenge: EngineeringChallenge
    ) -> Optional[ProjectIdea]:
        """
        Refine an existing project idea to make it more impressive
        
        Args:
            project: Original project idea
            company_name: Target company name
            company_profile: Company profile
            challenge: Related engineering challenge
            
        Returns:
            Refined ProjectIdea or None if refinement fails
        """
        try:
            # Format company profile for prompt
            profile_text = self._format_profile_for_prompt(company_profile)
            
            # Generate refinement prompt
            prompt = PROJECT_REFINEMENT_PROMPT.format(
                company_name=company_name,
                project_title=project.title,
                project_description=project.description,
                tech_stack=', '.join(project.tech_stack),
                company_profile=profile_text,
                challenge=challenge.description
            )
            
            # Get response from Gemini
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Extract JSON from response
            json_data = self._extract_json_from_response(response_text)
            
            if not json_data:
                logger.error(f"Failed to extract JSON from refinement response")
                return None
            
            # Create refined project
            refined_project = ProjectIdea(
                title=json_data.get('title', project.title),
                description=json_data.get('description', project.description),
                tech_stack=json_data.get('tech_stack', '').split(', '),
                demo_hook=json_data.get('demo_hook', project.demo_hook),
                difficulty=json_data.get('difficulty', project.difficulty),
                estimated_duration=json_data.get('estimated_duration', project.estimated_duration),
                challenge_id=project.challenge_id,
                company_name=project.company_name
            )
            
            return refined_project
            
        except Exception as e:
            logger.error(f"Error refining project idea: {str(e)}")
            return None
    
    def _generate_projects_for_challenge(
        self,
        company_name: str,
        company_profile: Optional[CompanyProfile],
        challenge: EngineeringChallenge,
        ideas_per_challenge: int,
        user_skills: Optional[List[str]] = None
    ) -> List[ProjectIdea]:
        """Generate projects for a specific challenge"""
        try:
            # Format inputs for prompt
            profile_text = self._format_profile_for_prompt(company_profile) if company_profile else "Company information not available"
            skills_text = ', '.join(user_skills) if user_skills else "Not specified"
            
            # Generate prompt
            prompt = PROJECT_GENERATION_PROMPT.format(
                company_name=company_name,
                challenge=challenge.description,
                company_profile=profile_text,
                user_skills=skills_text,
                ideas_per_challenge=ideas_per_challenge
            )
            
            # Get response from Gemini
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Extract JSON from response
            json_data = self._extract_json_from_response(response_text)
            
            if not json_data or not isinstance(json_data, list):
                logger.error(f"Failed to extract projects JSON for challenge {challenge.id}")
                return []
            
            # Parse projects
            projects = []
            for project_data in json_data:
                try:
                    project = ProjectIdea(
                        title=project_data.get('title', 'Untitled Project'),
                        description=project_data.get('description', ''),
                        tech_stack=project_data.get('tech_stack', '').split(', '),
                        demo_hook=project_data.get('demo_hook', ''),
                        difficulty=project_data.get('difficulty', 'intermediate'),
                        estimated_duration=project_data.get('estimated_duration', '1-2 months'),
                        challenge_id=challenge.id,
                        challenge_title=challenge.title,
                        company_name=company_name
                    )
                    projects.append(project)
                except Exception as e:
                    logger.error(f"Error parsing project: {str(e)}")
                    continue
            
            return projects
            
        except Exception as e:
            logger.error(f"Error generating projects for challenge {challenge.id}: {str(e)}")
            return []
    
    def _extract_json_from_response(self, response_text: str) -> Optional[Dict[str, Any]]:
        """Extract JSON from Gemini response text"""
        try:
            # Try to find JSON in code blocks
            if '```json' in response_text:
                json_start = response_text.find('```json') + 7
                json_end = response_text.find('```', json_start)
                json_text = response_text[json_start:json_end]
            elif '```' in response_text:
                json_start = response_text.find('```') + 3
                json_end = response_text.find('```', json_start)
                json_text = response_text[json_start:json_end]
            else:
                # Try to find JSON array or object
                json_start = response_text.find('[')
                if json_start == -1:
                    json_start = response_text.find('{')
                if json_start == -1:
                    return None
                
                # Find matching closing bracket/brace
                if response_text[json_start] == '[':
                    bracket_count = 0
                    for i in range(json_start, len(response_text)):
                        if response_text[i] == '[':
                            bracket_count += 1
                        elif response_text[i] == ']':
                            bracket_count -= 1
                            if bracket_count == 0:
                                json_end = i + 1
                                break
                else:  # Object
                    bracket_count = 0
                    for i in range(json_start, len(response_text)):
                        if response_text[i] == '{':
                            bracket_count += 1
                        elif response_text[i] == '}':
                            bracket_count -= 1
                            if bracket_count == 0:
                                json_end = i + 1
                                break
                
                json_text = response_text[json_start:json_end]
            
            return json.loads(json_text)
            
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Failed to parse JSON: {str(e)}")
            return None
    
    def _format_profile_for_prompt(self, profile: CompanyProfile) -> str:
        """Format company profile for use in prompts"""
        if not profile:
            return "Company information not available"
        
        return f"""
Company: {profile.name}
Industry: {profile.industry.value}
Size: {profile.size.value}
Business Focus: {profile.business_focus}
Description: {profile.description}
Recent Highlights: {', '.join(profile.recent_highlights)}
Tech Stack: {self._format_tech_stack(profile.tech_stack)}
"""
    
    def _format_tech_stack(self, tech_stack) -> str:
        """Format tech stack for display"""
        if not tech_stack:
            return "Not specified"
        
        sections = []
        if tech_stack.frontend:
            sections.append(f"Frontend: {', '.join(tech_stack.frontend)}")
        if tech_stack.backend:
            sections.append(f"Backend: {', '.join(tech_stack.backend)}")
        if tech_stack.database:
            sections.append(f"Database: {', '.join(tech_stack.database)}")
        if tech_stack.cloud:
            sections.append(f"Cloud: {', '.join(tech_stack.cloud)}")
        if tech_stack.devops:
            sections.append(f"DevOps: {', '.join(tech_stack.devops)}")
        if tech_stack.ai_ml:
            sections.append(f"AI/ML: {', '.join(tech_stack.ai_ml)}")
        if tech_stack.mobile:
            sections.append(f"Mobile: {', '.join(tech_stack.mobile)}")
        if tech_stack.other:
            sections.append(f"Other: {', '.join(tech_stack.other)}")
        
        return '; '.join(sections) if sections else "Not specified" 