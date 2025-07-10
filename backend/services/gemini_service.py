"""
Gemini AI service for generating company profiles, challenges, and project ideas.
"""

import json
import asyncio
from typing import List, Dict, Any, Optional
import google.generativeai as genai
import structlog
import traceback

from core.config import settings
from core.cache import cache_decorator

logger = structlog.get_logger()

# Configure Gemini with error handling
def initialize_gemini():
    """Initialize Gemini AI with comprehensive error handling."""
    try:
        if not settings.GEMINI_API_KEY or settings.GEMINI_API_KEY == "your_api_key_here":
            raise ValueError("GEMINI_API_KEY not configured")
        
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel(settings.GEMINI_MODEL)
        
        # Test the configuration
        test_response = asyncio.run(asyncio.to_thread(
            model.generate_content,
            "Hello",
            generation_config=genai.types.GenerationConfig(
                temperature=0.1,
                max_output_tokens=10,
            )
        ))
        
        logger.info("Gemini AI initialized successfully", 
                   model=settings.GEMINI_MODEL,
                   temperature=settings.TEMPERATURE,
                   max_tokens=settings.MAX_TOKENS)
        
        return model
        
    except ValueError as e:
        logger.error("Gemini configuration error", 
                    error=str(e),
                    file="gemini_service.py",
                    function="initialize_gemini")
        raise RuntimeError(f"Gemini configuration failed: {str(e)}")
    except Exception as e:
        logger.error("Gemini initialization error", 
                    error=str(e),
                    file="gemini_service.py",
                    function="initialize_gemini")
        raise RuntimeError(f"Gemini initialization failed: {str(e)}")

# Initialize Gemini
try:
    model = initialize_gemini()
except Exception as e:
    logger.error("Critical: Failed to initialize Gemini", error=str(e))
    raise


class GeminiService:
    """Service for interacting with Google Gemini AI."""
    
    def __init__(self):
        self.model = model
        self.temperature = settings.TEMPERATURE
        self.max_tokens = settings.MAX_TOKENS
    
    @cache_decorator(ttl=3600)  # Cache for 1 hour
    async def get_company_profile(self, company_name: str) -> Dict[str, Any]:
        """
        Get a concise company profile including industry, tech stack, and recent highlights.
        
        Args:
            company_name: Name of the company
            
        Returns:
            Dictionary containing company profile information
        """
        try:
            logger.info("Generating company profile", company=company_name)
            
            prompt = f"""
            Get a concise profile for {company_name}: industry, tech stack hints, and recent news items.
            
            Please provide the information in the following JSON format:
            {{
                "name": "{company_name}",
                "industry": "industry name",
                "tech_stack": ["technology1", "technology2", "technology3"],
                "recent_highlights": ["highlight1", "highlight2", "highlight3"],
                "summary": "brief company description"
            }}
            
            Focus on:
            1. Primary industry and business model
            2. Common technologies they likely use
            3. Recent news, funding, or product launches
            4. Engineering challenges they might face
            """
            
            response = await self._generate_response(prompt)
            result = self._parse_json_response(response)
            
            logger.info("Company profile generated successfully", 
                       company=company_name,
                       industry=result.get("industry"),
                       tech_stack_count=len(result.get("tech_stack", [])))
            
            return result
            
        except Exception as e:
            logger.error("Error getting company profile", 
                        error=str(e),
                        company=company_name,
                        file="gemini_service.py",
                        function="get_company_profile")
            return self._get_fallback_profile(company_name)
    
    @cache_decorator(ttl=3600)  # Cache for 1 hour
    async def get_engineering_challenges(self, company_name: str, profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Get engineering challenges based on company profile.
        
        Args:
            company_name: Name of the company
            profile: Company profile information
            
        Returns:
            List of engineering challenges
        """
        try:
            logger.info("Generating engineering challenges", 
                       company=company_name,
                       industry=profile.get("industry"))
            
            profile_summary = f"Industry: {profile.get('industry', 'Unknown')}, Tech Stack: {', '.join(profile.get('tech_stack', []))}"
            
            prompt = f"""
            Based on this profile for {company_name}: {profile_summary}
            
            List 3 common engineering challenges or product areas the team might face.
            
            Please provide the information in the following JSON format:
            [
                {{
                    "title": "Challenge Title",
                    "description": "Detailed description of the challenge",
                    "category": "backend|frontend|data|mobile|devops",
                    "difficulty": "easy|medium|hard",
                    "relevance": "Why this challenge is relevant to the company"
                }}
            ]
            
            Focus on:
            1. Scalability challenges
            2. Performance optimization
            3. Data processing and analytics
            4. User experience improvements
            5. Security and compliance
            6. Integration challenges
            """
            
            response = await self._generate_response(prompt)
            result = self._parse_json_response(response)
            
            logger.info("Engineering challenges generated successfully", 
                       company=company_name,
                       challenge_count=len(result))
            
            return result
            
        except Exception as e:
            logger.error("Error getting engineering challenges", 
                        error=str(e),
                        company=company_name,
                        file="gemini_service.py",
                        function="get_engineering_challenges")
            return self._get_fallback_challenges(company_name)
    
    @cache_decorator(ttl=1800)  # Cache for 30 minutes
    async def get_project_ideas(self, company_name: str, challenges: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Generate project ideas for each challenge.
        
        Args:
            company_name: Name of the company
            challenges: List of engineering challenges
            
        Returns:
            List of project ideas
        """
        try:
            logger.info("Generating project ideas", 
                       company=company_name,
                       challenge_count=len(challenges))
            
            challenges_text = "\n".join([
                f"- {challenge['title']}: {challenge['description']}"
                for challenge in challenges
            ])
            
            prompt = f"""
            For {company_name}, based on these challenges:
            {challenges_text}
            
            For each challenge, propose 3-5 side-projects someone could build to showcase relevant skills.
            
            Please provide the information in the following JSON format:
            [
                {{
                    "title": "Project Title",
                    "description": "Detailed project description",
                    "tech_stack": ["technology1", "technology2", "technology3"],
                    "demo_hook": "Specific demo feature that would impress an interviewer",
                    "difficulty": "easy|medium|hard",
                    "estimated_duration": "time estimate (e.g., '2-3 weeks')",
                    "challenge_category": "category this project addresses",
                    "key_features": ["feature1", "feature2", "feature3"]
                }}
            ]
            
            Requirements for each project:
            1. Must be realistic and buildable
            2. Should demonstrate relevant technical skills
            3. Include a clear demo hook
            4. Use modern, relevant technologies
            5. Focus on practical, interview-worthy projects
            """
            
            response = await self._generate_response(prompt)
            result = self._parse_json_response(response)
            
            logger.info("Project ideas generated successfully", 
                       company=company_name,
                       idea_count=len(result))
            
            return result
            
        except Exception as e:
            logger.error("Error getting project ideas", 
                        error=str(e),
                        company=company_name,
                        file="gemini_service.py",
                        function="get_project_ideas")
            return self._get_fallback_ideas(company_name)
    
    async def _generate_response(self, prompt: str) -> str:
        """Generate response from Gemini model with comprehensive error handling."""
        try:
            logger.debug("Generating Gemini response", prompt_length=len(prompt))
            
            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=self.temperature,
                    max_output_tokens=self.max_tokens,
                )
            )
            
            if not response.text:
                raise RuntimeError("Empty response from Gemini API")
            
            logger.debug("Gemini response generated", 
                        response_length=len(response.text),
                        usage_metadata=response.usage_metadata)
            
            return response.text
            
        except genai.types.BlockedPromptException as e:
            logger.error("Gemini blocked prompt", 
                        error=str(e),
                        file="gemini_service.py",
                        function="_generate_response")
            raise RuntimeError(f"Gemini blocked the prompt: {str(e)}")
            
        except genai.types.GenerationException as e:
            logger.error("Gemini generation error", 
                        error=str(e),
                        file="gemini_service.py",
                        function="_generate_response")
            raise RuntimeError(f"Gemini generation failed: {str(e)}")
            
        except Exception as e:
            logger.error("Unexpected Gemini API error", 
                        error=str(e),
                        error_type=type(e).__name__,
                        file="gemini_service.py",
                        function="_generate_response")
            raise RuntimeError(f"Gemini API error: {str(e)}")
    
    def _parse_json_response(self, response: str) -> Any:
        """Parse JSON response from Gemini with comprehensive error handling."""
        try:
            logger.debug("Parsing JSON response", response_length=len(response))
            
            # Clean up the response to extract JSON
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.endswith("```"):
                response = response[:-3]
            
            parsed = json.loads(response.strip())
            
            logger.debug("JSON response parsed successfully", 
                        parsed_type=type(parsed).__name__)
            
            return parsed
            
        except json.JSONDecodeError as e:
            logger.error("Failed to parse JSON response", 
                        error=str(e),
                        response_preview=response[:200],
                        file="gemini_service.py",
                        function="_parse_json_response")
            raise RuntimeError(f"Failed to parse JSON response: {str(e)}")
            
        except Exception as e:
            logger.error("Unexpected error parsing JSON response", 
                        error=str(e),
                        file="gemini_service.py",
                        function="_parse_json_response")
            raise RuntimeError(f"JSON parsing error: {str(e)}")
    
    def _get_fallback_profile(self, company_name: str) -> Dict[str, Any]:
        """Fallback company profile when API fails."""
        logger.warning("Using fallback company profile", company=company_name)
        
        return {
            "name": company_name,
            "industry": "Technology",
            "tech_stack": ["Python", "JavaScript", "React", "Node.js", "AWS"],
            "recent_highlights": [
                "Growing technology company",
                "Focus on innovation and scalability",
                "Modern tech stack and development practices"
            ],
            "summary": f"{company_name} is a technology company focused on innovation and growth."
        }
    
    def _get_fallback_challenges(self, company_name: str) -> List[Dict[str, Any]]:
        """Fallback engineering challenges when API fails."""
        logger.warning("Using fallback engineering challenges", company=company_name)
        
        return [
            {
                "title": "Scalable Backend Architecture",
                "description": "Design and implement a scalable backend system that can handle high traffic and data processing requirements.",
                "category": "backend",
                "difficulty": "medium",
                "relevance": "Most tech companies need robust backend systems to handle their growing user base and data requirements."
            },
            {
                "title": "Real-time Data Processing",
                "description": "Build a real-time data processing pipeline for analytics and user insights.",
                "category": "data",
                "difficulty": "hard",
                "relevance": "Data-driven decision making is crucial for modern companies."
            },
            {
                "title": "User Experience Optimization",
                "description": "Create an intuitive and responsive user interface that improves user engagement and satisfaction.",
                "category": "frontend",
                "difficulty": "medium",
                "relevance": "User experience is a key differentiator in competitive markets."
            }
        ]
    
    def _get_fallback_ideas(self, company_name: str) -> List[Dict[str, Any]]:
        """Fallback project ideas when API fails."""
        logger.warning("Using fallback project ideas", company=company_name)
        
        return [
            {
                "title": "API Gateway with Rate Limiting",
                "description": "Build a scalable API gateway with rate limiting, authentication, and monitoring capabilities.",
                "tech_stack": ["Node.js", "Express", "Redis", "Docker", "Prometheus"],
                "demo_hook": "Real-time dashboard showing API usage and rate limiting in action",
                "difficulty": "medium",
                "estimated_duration": "2-3 weeks",
                "challenge_category": "backend",
                "key_features": ["Rate limiting", "Authentication", "Monitoring", "Load balancing"]
            },
            {
                "title": "Real-time Analytics Dashboard",
                "description": "Create a real-time analytics dashboard that processes and visualizes streaming data.",
                "tech_stack": ["React", "WebSocket", "Python", "FastAPI", "PostgreSQL"],
                "demo_hook": "Live data visualization with real-time updates and interactive charts",
                "difficulty": "medium",
                "estimated_duration": "3-4 weeks",
                "challenge_category": "data",
                "key_features": ["Real-time updates", "Interactive charts", "Data processing", "WebSocket communication"]
            },
            {
                "title": "Progressive Web App",
                "description": "Build a progressive web app with offline capabilities and push notifications.",
                "tech_stack": ["React", "Service Workers", "IndexedDB", "PWA", "Firebase"],
                "demo_hook": "Offline functionality and push notifications working seamlessly",
                "difficulty": "easy",
                "estimated_duration": "2-3 weeks",
                "challenge_category": "frontend",
                "key_features": ["Offline support", "Push notifications", "Responsive design", "App-like experience"]
            }
        ]


# Create service instance
gemini_service = GeminiService() 