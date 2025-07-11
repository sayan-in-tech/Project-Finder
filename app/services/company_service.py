"""
Company analysis service for the FastAPI application
"""

import asyncio
import sys
import os
from typing import List, Optional

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.models.schemas import CompanyProfile, EngineeringChallenge, IndustryType, CompanySize, TechStack
from .gemini_service import GeminiService
from app.services.website_parser import crawl_and_summarize_website


class CompanyAnalysisService:
    """Service for analyzing companies and generating engineering challenges"""
    
    def __init__(self, api_key: str):
        self.gemini_service = GeminiService(api_key)
        self.api_key = api_key
    
    async def analyze_company(self, company_name: str, additional_info: Optional[str] = None, website_url: Optional[str] = None) -> Optional[CompanyProfile]:
        """
        Analyze a company and return its profile
        """
        try:
            # If website_url is provided, crawl and summarize the website
            if website_url:
                website_summary = crawl_and_summarize_website(website_url)
                if website_summary:
                    if additional_info:
                        additional_info = f"{additional_info}\n\nWebsite Summary:\n{website_summary}"
                    else:
                        additional_info = f"Website Summary:\n{website_summary}"
            # Run the Gemini service in a thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            company_data = await loop.run_in_executor(
                None, 
                self.gemini_service.analyze_company, 
                company_name
            )
            # Attach additional_info to the company_data if provided
            if additional_info:
                company_data['additional_info'] = additional_info
            # Convert the raw data to CompanyProfile model
            return self._convert_to_company_profile(company_data)
        except Exception as e:
            print(f"Error analyzing company {company_name}: {e}")
            return None
    
    async def get_engineering_challenges(
        self, 
        company_name: str, 
        company_profile: CompanyProfile
    ) -> List[EngineeringChallenge]:
        """
        Get engineering challenges for a company
        """
        try:
            # Run the Gemini service in a thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            company_data = await loop.run_in_executor(
                None, 
                self.gemini_service.analyze_company, 
                company_name
            )
            
            # Extract challenges from the company data
            challenges = company_data.get('engineering_challenges', [])
            return [self._convert_to_engineering_challenge(challenge, i) for i, challenge in enumerate(challenges)]
            
        except Exception as e:
            print(f"Error getting engineering challenges for {company_name}: {e}")
            return []
    
    async def get_company_insights(self, company_name: str) -> dict:
        """
        Get additional insights about a company
        """
        try:
            # This could be expanded to include more detailed analysis
            company_profile = await self.analyze_company(company_name)
            if not company_profile:
                return {}
            
            challenges = await self.get_engineering_challenges(company_name, company_profile)
            
            return {
                "total_challenges": len(challenges),
                "primary_tech_areas": company_profile.tech_stack.backend + company_profile.tech_stack.frontend,
                "difficulty_distribution": {
                    challenge.difficulty: len([c for c in challenges if c.difficulty == challenge.difficulty])
                    for challenge in challenges
                },
                "industry_focus": company_profile.industry.value,
                "company_size": company_profile.size.value
            }
        except Exception as e:
            print(f"Error getting company insights for {company_name}: {e}")
            return {}
    
    def _convert_to_company_profile(self, data: dict) -> CompanyProfile:
        """Convert raw company data to CompanyProfile model"""
        tech_stack_data = data.get('tech_stack', {})
        tech_stack = TechStack(
            backend=tech_stack_data.get('backend', []),
            frontend=tech_stack_data.get('frontend', []),
            database=tech_stack_data.get('database', []),
            cloud=tech_stack_data.get('cloud', [])
        )
        return CompanyProfile(
            name=data.get('name', 'Unknown Company'),
            industry=IndustryType(data.get('industry', 'technology')),
            size=CompanySize(data.get('size', 'scaleup')),
            description=data.get('description', ''),
            business_focus=data.get('business_focus', 'Technology innovation and digital transformation'),
            tech_stack=tech_stack,
            additional_info=data.get('additional_info', None)
        )
    
    def _convert_to_engineering_challenge(self, data: dict, index: int) -> EngineeringChallenge:
        """Convert raw challenge data to EngineeringChallenge model"""
        return EngineeringChallenge(
            id=f"challenge_{index}",
            title=data.get('title', f'Challenge {index + 1}'),
            description=data.get('description', ''),
            difficulty=data.get('difficulty', 'intermediate'),
            relevance_score=0.8,  # Default relevance score
            tech_areas=data.get('tech_areas', [])
        )
