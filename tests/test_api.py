"""
API tests for Project Finder backend.
"""

import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch, MagicMock

from backend.main import app
from backend.core.database import get_db
from backend.models.project import Base
from backend.services.gemini_service import gemini_service


# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def client():
    """Create test client."""
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Clean up
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def mock_gemini_service():
    """Mock Gemini service responses."""
    with patch('backend.services.gemini_service.gemini_service') as mock:
        # Mock company profile
        mock.get_company_profile.return_value = {
            "name": "Test Company",
            "industry": "Technology",
            "tech_stack": ["Python", "React", "PostgreSQL"],
            "recent_highlights": ["Recent funding round", "New product launch"],
            "summary": "A test technology company"
        }
        
        # Mock challenges
        mock.get_engineering_challenges.return_value = [
            {
                "title": "Scalability Challenge",
                "description": "Handling high traffic",
                "category": "backend",
                "difficulty": "medium",
                "relevance": "Important for growth"
            },
            {
                "title": "Data Processing",
                "description": "Real-time data analysis",
                "category": "data",
                "difficulty": "hard",
                "relevance": "Core business need"
            }
        ]
        
        # Mock project ideas
        mock.get_project_ideas.return_value = [
            {
                "title": "Real-time Dashboard",
                "description": "Build a real-time monitoring dashboard",
                "tech_stack": ["React", "Node.js", "Socket.io"],
                "demo_hook": "Live data updates and charts",
                "difficulty": "medium",
                "estimated_duration": "2-3 weeks",
                "challenge_category": "backend",
                "key_features": ["Real-time updates", "Interactive charts"]
            },
            {
                "title": "API Gateway",
                "description": "Create a scalable API gateway",
                "tech_stack": ["Python", "FastAPI", "Redis"],
                "demo_hook": "Rate limiting and authentication demo",
                "difficulty": "medium",
                "estimated_duration": "3-4 weeks",
                "challenge_category": "backend",
                "key_features": ["Rate limiting", "Authentication"]
            }
        ]
        
        yield mock


class TestHealthCheck:
    """Test health check endpoint."""
    
    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "timestamp" in data


class TestCompanyProfile:
    """Test company profile endpoints."""
    
    def test_get_company_profile_success(self, client, mock_gemini_service):
        """Test successful company profile retrieval."""
        response = client.get("/api/v1/profile/", params={"company": "Test Company"})
        assert response.status_code == 200
        
        data = response.json()
        assert data["name"] == "Test Company"
        assert data["industry"] == "Technology"
        assert "tech_stack" in data
        assert "recent_highlights" in data
    
    def test_get_company_profile_missing_company(self, client):
        """Test company profile with missing company parameter."""
        response = client.get("/api/v1/profile/")
        assert response.status_code == 422  # Validation error
    
    def test_search_companies(self, client):
        """Test company search endpoint."""
        response = client.get("/api/v1/profile/search", params={"query": "Test"})
        assert response.status_code == 200
        
        data = response.json()
        assert "companies" in data
        assert "total" in data


class TestEngineeringChallenges:
    """Test engineering challenges endpoints."""
    
    def test_get_challenges_success(self, client, mock_gemini_service):
        """Test successful challenges retrieval."""
        # First create a company profile
        client.get("/api/v1/profile/", params={"company": "Test Company"})
        
        # Then get challenges
        response = client.get("/api/v1/challenges/", params={"company": "Test Company"})
        assert response.status_code == 200
        
        data = response.json()
        assert "company" in data
        assert "challenges" in data
        assert len(data["challenges"]) > 0
    
    def test_get_challenges_company_not_found(self, client):
        """Test challenges for non-existent company."""
        response = client.get("/api/v1/challenges/", params={"company": "NonExistent Company"})
        assert response.status_code == 404
    
    def test_get_challenges_by_company_id(self, client, mock_gemini_service):
        """Test getting challenges by company ID."""
        # First create a company profile
        client.get("/api/v1/profile/", params={"company": "Test Company"})
        
        # Get challenges by company ID
        response = client.get("/api/v1/challenges/by-company/1")
        assert response.status_code == 200
        
        data = response.json()
        assert "company" in data
        assert "challenges" in data


class TestProjectIdeas:
    """Test project ideas endpoints."""
    
    def test_get_project_ideas_success(self, client, mock_gemini_service):
        """Test successful project ideas retrieval."""
        # First create a company profile and challenges
        client.get("/api/v1/profile/", params={"company": "Test Company"})
        client.get("/api/v1/challenges/", params={"company": "Test Company"})
        
        # Then get project ideas
        response = client.get("/api/v1/ideas/", params={"company": "Test Company"})
        assert response.status_code == 200
        
        data = response.json()
        assert "company" in data
        assert "projects" in data
        assert len(data["projects"]) > 0
    
    def test_get_project_ideas_company_not_found(self, client):
        """Test project ideas for non-existent company."""
        response = client.get("/api/v1/ideas/", params={"company": "NonExistent Company"})
        assert response.status_code == 404
    
    def test_get_project_ideas_no_challenges(self, client, mock_gemini_service):
        """Test project ideas when no challenges exist."""
        # Create company but no challenges
        client.get("/api/v1/profile/", params={"company": "Test Company"})
        
        response = client.get("/api/v1/ideas/", params={"company": "Test Company"})
        assert response.status_code == 404
    
    def test_regenerate_ideas(self, client, mock_gemini_service):
        """Test regenerating project ideas."""
        # First create a company profile and challenges
        client.get("/api/v1/profile/", params={"company": "Test Company"})
        client.get("/api/v1/challenges/", params={"company": "Test Company"})
        client.get("/api/v1/ideas/", params={"company": "Test Company"})
        
        # Regenerate ideas
        response = client.post("/api/v1/ideas/regenerate", params={"company": "Test Company"})
        assert response.status_code == 200
        
        data = response.json()
        assert "company" in data
        assert "projects" in data


class TestSavedProjects:
    """Test saved projects endpoints."""
    
    def test_get_saved_projects_empty(self, client):
        """Test getting saved projects when none exist."""
        response = client.get("/api/v1/projects/")
        assert response.status_code == 200
        
        data = response.json()
        assert data["total"] == 0
        assert len(data["projects"]) == 0
    
    def test_save_project(self, client, mock_gemini_service):
        """Test saving a project to workspace."""
        # First create a project
        client.get("/api/v1/profile/", params={"company": "Test Company"})
        client.get("/api/v1/challenges/", params={"company": "Test Company"})
        client.get("/api/v1/ideas/", params={"company": "Test Company"})
        
        # Save a project
        response = client.post("/api/v1/projects/save/1")
        assert response.status_code == 200
        
        data = response.json()
        assert data["is_saved"] == True
    
    def test_save_project_with_notes(self, client, mock_gemini_service):
        """Test saving a project with notes."""
        # First create a project
        client.get("/api/v1/profile/", params={"company": "Test Company"})
        client.get("/api/v1/challenges/", params={"company": "Test Company"})
        client.get("/api/v1/ideas/", params={"company": "Test Company"})
        
        # Save a project with notes
        response = client.post("/api/v1/projects/save/1", params={"notes": "Test notes"})
        assert response.status_code == 200
        
        data = response.json()
        assert data["user_notes"] == "Test notes"
    
    def test_delete_saved_project(self, client, mock_gemini_service):
        """Test removing a project from workspace."""
        # First create and save a project
        client.get("/api/v1/profile/", params={"company": "Test Company"})
        client.get("/api/v1/challenges/", params={"company": "Test Company"})
        client.get("/api/v1/ideas/", params={"company": "Test Company"})
        client.post("/api/v1/projects/save/1")
        
        # Remove the project
        response = client.delete("/api/v1/projects/1")
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
    
    def test_clear_saved_projects(self, client, mock_gemini_service):
        """Test clearing all saved projects."""
        # First create and save some projects
        client.get("/api/v1/profile/", params={"company": "Test Company"})
        client.get("/api/v1/challenges/", params={"company": "Test Company"})
        client.get("/api/v1/ideas/", params={"company": "Test Company"})
        client.post("/api/v1/projects/save/1")
        client.post("/api/v1/projects/save/2")
        
        # Clear all projects
        response = client.delete("/api/v1/projects/clear")
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
    
    def test_update_project_notes(self, client, mock_gemini_service):
        """Test updating project notes."""
        # First create and save a project
        client.get("/api/v1/profile/", params={"company": "Test Company"})
        client.get("/api/v1/challenges/", params={"company": "Test Company"})
        client.get("/api/v1/ideas/", params={"company": "Test Company"})
        client.post("/api/v1/projects/save/1")
        
        # Update notes
        response = client.put("/api/v1/projects/1/notes", params={"notes": "Updated notes"})
        assert response.status_code == 200
        
        data = response.json()
        assert data["user_notes"] == "Updated notes"


class TestErrorHandling:
    """Test error handling."""
    
    def test_invalid_endpoint(self, client):
        """Test invalid endpoint returns 404."""
        response = client.get("/api/v1/invalid/")
        assert response.status_code == 404
    
    def test_missing_required_parameters(self, client):
        """Test missing required parameters."""
        response = client.get("/api/v1/profile/")
        assert response.status_code == 422
    
    @patch('backend.services.gemini_service.gemini_service.get_company_profile')
    def test_gemini_api_error(self, mock_get_profile, client):
        """Test handling of Gemini API errors."""
        mock_get_profile.side_effect = Exception("API Error")
        
        response = client.get("/api/v1/profile/", params={"company": "Test Company"})
        assert response.status_code == 500


if __name__ == "__main__":
    pytest.main([__file__]) 