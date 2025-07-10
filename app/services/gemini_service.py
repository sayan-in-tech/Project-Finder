"""
Gemini API service for AI-powered features
"""

import google.generativeai as genai
from typing import List, Optional, Dict, Any
import json


class GeminiService:
    """Service for interacting with Google's Gemini AI API"""
    
    def __init__(self, api_key: str):
        """Initialize the Gemini service with user-provided API key"""
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def analyze_company(self, company_name: str) -> Dict[str, Any]:
        """
        Analyze a company and return its profile
        """
        try:
            prompt = f"""
            Analyze the company "{company_name}" and provide the following information in JSON format:
            {{
                "name": "Company name",
                "industry": "Technology/Finance/Healthcare/etc",
                "size": "startup/medium/enterprise",
                "description": "Brief company description",
                "tech_stack": {{
                    "backend": ["tech1", "tech2"],
                    "frontend": ["tech1", "tech2"],
                    "databases": ["db1", "db2"],
                    "cloud": ["aws", "gcp", "azure"]
                }},
                "engineering_challenges": [
                    {{
                        "title": "Challenge title",
                        "description": "Detailed description",
                        "difficulty": "beginner/intermediate/advanced",
                        "tech_areas": ["area1", "area2"]
                    }}
                ]
            }}
            
            Focus on real engineering challenges that this company might face.
            """
            
            response = self.model.generate_content(prompt)
            result = json.loads(response.text)
            return result
            
        except Exception as e:
            print(f"Error analyzing company {company_name}: {e}")
            return self._get_default_company_profile(company_name)
    
    def generate_project_ideas(
        self, 
        company_name: str, 
        challenges: List[Dict[str, Any]], 
        user_skills: Optional[List[str]] = None,
        total_ideas: int = 4
    ) -> List[Dict[str, Any]]:
        """
        Generate project ideas based on company challenges
        """
        try:
            skills_text = f"User skills: {', '.join(user_skills or [])}" if user_skills else "No specific skills mentioned"
            challenges_text = "\n".join([f"- {c['title']}: {c['description']}" for c in challenges])
            
            prompt = f"""
            Generate {total_ideas} project ideas for {company_name} based on these engineering challenges:
            
            {challenges_text}
            
            {skills_text}
            
            Return as JSON array:
            [
                {{
                    "title": "Project title",
                    "description": "Detailed project description",
                    "difficulty": "beginner/intermediate/advanced",
                    "estimated_duration": "2-3 months",
                    "tech_stack": ["tech1", "tech2"],
                    "learning_outcomes": ["outcome1", "outcome2"],
                    "challenge_id": "challenge_1",
                    "challenge_title": "Original challenge title"
                }}
            ]
            
            Make projects practical and achievable.
            """
            
            response = self.model.generate_content(prompt)
            result = json.loads(response.text)
            return result
            
        except Exception as e:
            print(f"Error generating project ideas: {e}")
            return self._get_default_project_ideas(company_name, total_ideas)
    
    def refine_project_idea(
        self, 
        project: Dict[str, Any], 
        company_name: str, 
        challenge: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Refine an existing project idea with additional context
        """
        try:
            prompt = f"""
            Refine this project idea for {company_name}:
            
            Current project: {project['title']}
            Description: {project['description']}
            
            Challenge context: {challenge['title']} - {challenge['description']}
            
            Provide an improved version with:
            - More detailed technical implementation
            - Specific technologies to use
            - Step-by-step development plan
            - Success metrics
            
            Return as JSON with the same structure as the original project.
            """
            
            response = self.model.generate_content(prompt)
            result = json.loads(response.text)
            return result
            
        except Exception as e:
            print(f"Error refining project idea: {e}")
            return project
    
    def _get_default_company_profile(self, company_name: str) -> Dict[str, Any]:
        """Fallback company profile when AI analysis fails"""
        return {
            "name": company_name,
            "industry": "Technology",
            "size": "medium",
            "description": f"{company_name} is a technology company focused on innovation.",
            "tech_stack": {
                "backend": ["Python", "Node.js", "Java"],
                "frontend": ["React", "Vue.js", "Angular"],
                "databases": ["PostgreSQL", "MongoDB"],
                "cloud": ["AWS", "Google Cloud"]
            },
            "engineering_challenges": [
                {
                    "title": "Scalability Challenges",
                    "description": "Building systems that can handle growing user base",
                    "difficulty": "intermediate",
                    "tech_areas": ["Backend", "Infrastructure"]
                },
                {
                    "title": "Data Processing",
                    "description": "Efficiently processing and analyzing large datasets",
                    "difficulty": "advanced",
                    "tech_areas": ["Data Engineering", "Machine Learning"]
                }
            ]
        }
    
    def _get_default_project_ideas(self, company_name: str, total_ideas: int) -> List[Dict[str, Any]]:
        """Fallback project ideas when AI generation fails"""
        default_projects = [
            {
                "title": "Real-time Analytics Dashboard",
                "description": "Build a dashboard to visualize company metrics in real-time",
                "difficulty": "intermediate",
                "estimated_duration": "2-3 months",
                "tech_stack": ["React", "Node.js", "WebSocket", "Chart.js"],
                "learning_outcomes": ["Real-time data handling", "Dashboard design", "WebSocket implementation"],
                "challenge_id": "challenge_1",
                "challenge_title": "Data Visualization"
            },
            {
                "title": "API Gateway Service",
                "description": "Create a centralized API gateway for microservices",
                "difficulty": "advanced",
                "estimated_duration": "3-4 months",
                "tech_stack": ["Python", "FastAPI", "Redis", "Docker"],
                "learning_outcomes": ["Microservices architecture", "API design", "Service discovery"],
                "challenge_id": "challenge_2",
                "challenge_title": "System Architecture"
            }
        ]
        
        return default_projects[:total_ideas] 