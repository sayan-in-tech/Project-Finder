"""
Service for company analysis and profiling
"""

import json
import logging
from typing import List, Optional, Dict, Any
import google.generativeai as genai
from ..models.models import (
    CompanyProfile, 
    EngineeringChallenge, 
    IndustryType, 
    CompanySize, 
    TechStack
)
from ..prompts.prompts import COMPANY_PROFILE_PROMPT, ENGINEERING_CHALLENGES_PROMPT

logger = logging.getLogger(__name__)

class CompanyAnalysisService:
    """Service for analyzing companies and extracting relevant information"""
    
    def __init__(self, api_key: str):
        """Initialize the service with Gemini API key"""
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def analyze_company(self, company_name: str) -> Optional[CompanyProfile]:
        """
        Analyze a company and return a comprehensive profile
        
        Args:
            company_name: Name of the company to analyze
            
        Returns:
            CompanyProfile object or None if analysis fails
        """
        try:
            # Generate prompt for company analysis
            prompt = COMPANY_PROFILE_PROMPT.format(company_name=company_name)
            
            # Get response from Gemini
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Extract JSON from response
            json_data = self._extract_json_from_response(response_text)
            
            if not json_data:
                logger.error(f"Failed to extract JSON from response for {company_name}")
                return None
            
            # Parse and validate the company profile
            profile = self._parse_company_profile(json_data, company_name)
            return profile
            
        except Exception as e:
            logger.error(f"Error analyzing company {company_name}: {str(e)}")
            return None
    
    def get_engineering_challenges(self, company_name: str, company_profile: CompanyProfile) -> List[EngineeringChallenge]:
        """
        Get engineering challenges for a company based on its profile
        
        Args:
            company_name: Name of the company
            company_profile: Analyzed company profile
            
        Returns:
            List of EngineeringChallenge objects
        """
        try:
            # Format company profile for prompt
            profile_text = self._format_profile_for_prompt(company_profile)
            
            # Generate prompt for engineering challenges
            prompt = ENGINEERING_CHALLENGES_PROMPT.format(
                company_name=company_name,
                company_profile=profile_text
            )
            
            # Get response from Gemini
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Extract JSON from response
            json_data = self._extract_json_from_response(response_text)
            
            if not json_data or not isinstance(json_data, list):
                logger.error(f"Failed to extract challenges JSON for {company_name}")
                return []
            
            # Parse and validate the challenges
            challenges = self._parse_engineering_challenges(json_data, company_name)
            return challenges
            
        except Exception as e:
            logger.error(f"Error getting engineering challenges for {company_name}: {str(e)}")
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
                json_start = response_text.find('{')
                if json_start == -1:
                    json_start = response_text.find('[')
                if json_start == -1:
                    return None
                
                # Find matching closing bracket/brace
                if response_text[json_start] == '{':
                    bracket_count = 0
                    for i in range(json_start, len(response_text)):
                        if response_text[i] == '{':
                            bracket_count += 1
                        elif response_text[i] == '}':
                            bracket_count -= 1
                            if bracket_count == 0:
                                json_end = i + 1
                                break
                else:  # Array
                    bracket_count = 0
                    for i in range(json_start, len(response_text)):
                        if response_text[i] == '[':
                            bracket_count += 1
                        elif response_text[i] == ']':
                            bracket_count -= 1
                            if bracket_count == 0:
                                json_end = i + 1
                                break
                
                json_text = response_text[json_start:json_end]
            
            return json.loads(json_text)
            
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Failed to parse JSON: {str(e)}")
            return None
    
    def _parse_company_profile(self, json_data: Dict[str, Any], company_name: str) -> CompanyProfile:
        """Parse JSON data into CompanyProfile object"""
        try:
            # Parse industry
            industry_str = json_data.get('industry', 'other').lower()
            industry = IndustryType(industry_str) if industry_str in [e.value for e in IndustryType] else IndustryType.OTHER
            
            # Parse size
            size_str = json_data.get('size', 'unknown').lower()
            size = CompanySize(size_str) if size_str in [e.value for e in CompanySize] else CompanySize.UNKNOWN
            
            # Parse tech stack
            tech_stack_data = json_data.get('tech_stack', {})
            tech_stack = TechStack(
                frontend=tech_stack_data.get('frontend', []),
                backend=tech_stack_data.get('backend', []),
                database=tech_stack_data.get('database', []),
                cloud=tech_stack_data.get('cloud', []),
                devops=tech_stack_data.get('devops', []),
                ai_ml=tech_stack_data.get('ai_ml', []),
                mobile=tech_stack_data.get('mobile', []),
                other=tech_stack_data.get('other', [])
            )
            
            return CompanyProfile(
                name=company_name,
                industry=industry,
                size=size,
                description=json_data.get('description', ''),
                tech_stack=tech_stack,
                recent_highlights=json_data.get('recent_highlights', []),
                business_focus=json_data.get('business_focus', ''),
                challenges=[]  # Will be populated later
            )
            
        except Exception as e:
            logger.error(f"Error parsing company profile: {str(e)}")
            raise
    
    def _parse_engineering_challenges(self, json_data: List[Dict[str, Any]], company_name: str) -> List[EngineeringChallenge]:
        """Parse JSON data into EngineeringChallenge objects"""
        challenges = []
        
        for i, challenge_data in enumerate(json_data):
            try:
                challenge = EngineeringChallenge(
                    id=challenge_data.get('id', f'challenge_{i+1}'),
                    title=challenge_data.get('title', ''),
                    description=challenge_data.get('description', ''),
                    difficulty=challenge_data.get('difficulty', 'intermediate'),
                    relevance_score=float(challenge_data.get('relevance_score', 0.75)),
                    tech_areas=challenge_data.get('tech_areas', [])
                )
                challenges.append(challenge)
            except Exception as e:
                logger.error(f"Error parsing challenge {i}: {str(e)}")
                continue
        
        return challenges
    
    def _format_profile_for_prompt(self, profile: CompanyProfile) -> str:
        """Format company profile for use in prompts"""
        return f"""
Company: {profile.name}
Industry: {profile.industry.value}
Size: {profile.size.value}
Business Focus: {profile.business_focus}
Description: {profile.description}
Recent Highlights: {', '.join(profile.recent_highlights)}
Tech Stack: {self._format_tech_stack(profile.tech_stack)}
"""
    
    def _format_tech_stack(self, tech_stack: TechStack) -> str:
        """Format tech stack for display"""
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