from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from enum import Enum
from datetime import datetime

class IndustryType(str, Enum):
    """Enum for different industry types"""
    TECHNOLOGY = "technology"
    FINANCE = "finance"
    HEALTHCARE = "healthcare"
    ECOMMERCE = "ecommerce"
    EDUCATION = "education"
    ENTERTAINMENT = "entertainment"
    TRANSPORTATION = "transportation"
    REAL_ESTATE = "real_estate"
    MANUFACTURING = "manufacturing"
    CONSULTING = "consulting"
    OTHER = "other"

class CompanySize(str, Enum):
    """Enum for company size categories"""
    STARTUP = "startup"
    SCALEUP = "scaleup"
    ENTERPRISE = "enterprise"
    UNKNOWN = "unknown"

class TechStack(BaseModel):
    """Model for technology stack information"""
    frontend: List[str] = Field(default_factory=list, description="Frontend technologies")
    backend: List[str] = Field(default_factory=list, description="Backend technologies")
    database: List[str] = Field(default_factory=list, description="Database technologies")
    cloud: List[str] = Field(default_factory=list, description="Cloud platforms")
    devops: List[str] = Field(default_factory=list, description="DevOps tools")
    ai_ml: List[str] = Field(default_factory=list, description="AI/ML technologies")
    mobile: List[str] = Field(default_factory=list, description="Mobile technologies")
    other: List[str] = Field(default_factory=list, description="Other technologies")

class CompanyProfile(BaseModel):
    """Comprehensive company profile model"""
    name: str = Field(..., description="Company name")
    industry: IndustryType = Field(..., description="Primary industry")
    size: CompanySize = Field(default=CompanySize.UNKNOWN, description="Company size")
    description: str = Field(..., description="Company description")
    tech_stack: TechStack = Field(default_factory=TechStack, description="Technology stack")
    recent_highlights: List[str] = Field(default_factory=list, description="Recent company highlights")
    business_focus: str = Field(..., description="Main business focus")
    challenges: List[str] = Field(default_factory=list, description="Engineering challenges")
    created_at: datetime = Field(default_factory=datetime.now, description="When profile was created")

class EngineeringChallenge(BaseModel):
    """Model for engineering challenges"""
    id: str = Field(..., description="Unique challenge identifier")
    title: str = Field(..., description="Challenge title")
    description: str = Field(..., description="Detailed description")
    difficulty: str = Field(..., description="Difficulty level")
    relevance_score: float = Field(..., description="Relevance score (0-1)")
    tech_areas: List[str] = Field(default_factory=list, description="Related technology areas")

class ProjectIdea(BaseModel):
    """Model for project ideas"""
    title: str = Field(..., description="Project title")
    description: str = Field(..., description="Project description")
    tech_stack: List[str] = Field(default_factory=list, description="Technologies to use")
    demo_hook: str = Field(..., description="What to demonstrate in interview")
    difficulty: str = Field(..., description="Project difficulty level")
    estimated_duration: str = Field(..., description="Estimated time to complete")
    challenge_id: str = Field(..., description="Related engineering challenge ID")
    company_name: str = Field(..., description="Target company name")
    created_at: datetime = Field(default_factory=datetime.now, description="When idea was created")

class CompanyAnalysisRequest(BaseModel):
    """Request model for company analysis"""
    company_name: str = Field(..., description="Company to analyze")
    user_skills: Optional[List[str]] = Field(default=None, description="User's technical skills")
    focus_areas: Optional[List[str]] = Field(default=None, description="Areas of interest")

class CompanyAnalysisResponse(BaseModel):
    """Response model for company analysis"""
    company_profile: CompanyProfile
    engineering_challenges: List[EngineeringChallenge]
    project_ideas: List[ProjectIdea]
    analysis_timestamp: datetime = Field(default_factory=datetime.now)

class ProjectGenerationRequest(BaseModel):
    """Request model for project generation"""
    company_name: str = Field(..., description="Target company")
    challenges: List[str] = Field(..., description="Engineering challenges")
    ideas_per_challenge: int = Field(default=4, description="Number of ideas per challenge")
    user_skills: Optional[List[str]] = Field(default=None, description="User's skills")

class ProjectGenerationResponse(BaseModel):
    """Response model for project generation"""
    projects: List[ProjectIdea]
    total_projects: int = Field(..., description="Total number of projects generated")
    generation_timestamp: datetime = Field(default_factory=datetime.now)