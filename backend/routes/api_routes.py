"""
API routes for the Project Finder backend
"""

from flask import Flask, request, jsonify
from typing import List, Optional
import logging
from ..models.models import (
    CompanyAnalysisRequest,
    CompanyAnalysisResponse,
    ProjectGenerationRequest,
    ProjectGenerationResponse,
    CompanyProfile,
    EngineeringChallenge,
    ProjectIdea
)
from ..services.company_analysis_service import CompanyAnalysisService
from ..services.project_generation_service import ProjectGenerationService

logger = logging.getLogger(__name__)

def create_app(api_key: str = ""):
    """Create Flask app with API routes"""
    app = Flask(__name__)
    
    @app.route('/api/analyze-company', methods=['POST'])
    def analyze_company():
        """Analyze a company and return comprehensive profile"""
        try:
            data = request.get_json()
            if not data or 'company_name' not in data:
                return jsonify({'error': 'company_name is required'}), 400
            
            # Get API key from request
            request_api_key = data.get('api_key')
            if not request_api_key:
                return jsonify({'error': 'api_key is required'}), 400
            
            company_name = data['company_name']
            user_skills = data.get('user_skills', [])
            focus_areas = data.get('focus_areas', [])
            
            # Initialize services with API key from request
            company_service = CompanyAnalysisService(request_api_key)
            project_service = ProjectGenerationService(request_api_key)
            
            # Analyze company
            company_profile = company_service.analyze_company(company_name)
            if not company_profile:
                return jsonify({'error': f'Failed to analyze company: {company_name}'}), 500
            
            # Get engineering challenges
            challenges = company_service.get_engineering_challenges(company_name, company_profile)
            
            # Generate project ideas
            projects = project_service.generate_projects_for_company(
                company_name=company_name,
                company_profile=company_profile,
                challenges=challenges,
                total_ideas=data.get('total_ideas', 4),
                user_skills=user_skills
            )
            
            # Create response
            response = CompanyAnalysisResponse(
                company_profile=company_profile,
                engineering_challenges=challenges,
                project_ideas=projects
            )
            
            return jsonify(response.dict()), 200
            
        except Exception as e:
            logger.error(f"Error in analyze_company: {str(e)}")
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/generate-projects', methods=['POST'])
    def generate_projects():
        """Generate project ideas for a company"""
        try:
            data = request.get_json()
            if not data or 'company_name' not in data or 'challenges' not in data:
                return jsonify({'error': 'company_name and challenges are required'}), 400
            
            # Get API key from request
            request_api_key = data.get('api_key')
            if not request_api_key:
                return jsonify({'error': 'api_key is required'}), 400
            
            # Initialize service with API key from request
            project_service = ProjectGenerationService(request_api_key)
            
            # Create request object
            request_obj = ProjectGenerationRequest(
                company_name=data['company_name'],
                challenges=data['challenges'],
                ideas_per_challenge=data.get('ideas_per_challenge', 4),
                user_skills=data.get('user_skills', [])
            )
            
            # Generate projects
            response = project_service.generate_projects_from_request(request_obj)
            
            return jsonify(response.dict()), 200
            
        except Exception as e:
            logger.error(f"Error in generate_projects: {str(e)}")
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/company-profile/<company_name>', methods=['GET'])
    def get_company_profile(company_name: str):
        """Get company profile only"""
        try:
            # Get API key from query parameters
            request_api_key = request.args.get('api_key')
            if not request_api_key:
                return jsonify({'error': 'api_key is required'}), 400
            
            # Initialize service with API key from request
            company_service = CompanyAnalysisService(request_api_key)
            
            company_profile = company_service.analyze_company(company_name)
            if not company_profile:
                return jsonify({'error': f'Failed to analyze company: {company_name}'}), 500
            
            return jsonify(company_profile.dict()), 200
            
        except Exception as e:
            logger.error(f"Error in get_company_profile: {str(e)}")
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/engineering-challenges/<company_name>', methods=['GET'])
    def get_engineering_challenges(company_name: str):
        """Get engineering challenges for a company"""
        try:
            # Get API key from query parameters
            request_api_key = request.args.get('api_key')
            if not request_api_key:
                return jsonify({'error': 'api_key is required'}), 400
            
            # Initialize service with API key from request
            company_service = CompanyAnalysisService(request_api_key)
            
            # First get company profile
            company_profile = company_service.analyze_company(company_name)
            if not company_profile:
                return jsonify({'error': f'Failed to analyze company: {company_name}'}), 500
            
            # Get challenges
            challenges = company_service.get_engineering_challenges(company_name, company_profile)
            
            return jsonify([challenge.dict() for challenge in challenges]), 200
            
        except Exception as e:
            logger.error(f"Error in get_engineering_challenges: {str(e)}")
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/refine-project', methods=['POST'])
    def refine_project():
        """Refine an existing project idea"""
        try:
            data = request.get_json()
            if not data or 'project' not in data or 'company_name' not in data:
                return jsonify({'error': 'project and company_name are required'}), 400
            
            # Get API key from request
            request_api_key = data.get('api_key')
            if not request_api_key:
                return jsonify({'error': 'api_key is required'}), 400
            
            # Initialize services with API key from request
            company_service = CompanyAnalysisService(request_api_key)
            project_service = ProjectGenerationService(request_api_key)
            
            # Parse project data
            project_data = data['project']
            project = ProjectIdea(**project_data)
            
            # Get company profile
            company_profile = company_service.analyze_company(data['company_name'])
            if not company_profile:
                return jsonify({'error': f'Failed to analyze company: {data["company_name"]}'}), 500
            
            # Create challenge object
            challenge = EngineeringChallenge(
                id=project.challenge_id,
                title="Challenge",
                description=data.get('challenge_description', ''),
                difficulty="intermediate",
                relevance_score=0.8,
                tech_areas=[]
            )
            
            # Refine project
            refined_project = project_service.refine_project_idea(
                project=project,
                company_name=data['company_name'],
                company_profile=company_profile,
                challenge=challenge
            )
            
            if not refined_project:
                return jsonify({'error': 'Failed to refine project'}), 500
            
            return jsonify(refined_project.dict()), 200
            
        except Exception as e:
            logger.error(f"Error in refine_project: {str(e)}")
            return jsonify({'error': str(e)}), 500
    
    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        return jsonify({'status': 'healthy', 'message': 'Project Finder API is running'}), 200
    
    return app 