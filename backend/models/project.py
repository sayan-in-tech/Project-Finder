"""
Database models for the Project Finder application.
"""

from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.sql import func

Base = declarative_base()


class Company(Base):
    """Company model for storing company information."""
    
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    industry = Column(String(255), nullable=True)
    tech_stack = Column(Text, nullable=True)  # JSON string of tech stack
    recent_highlights = Column(Text, nullable=True)
    profile_summary = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    challenges: Mapped[List["Challenge"]] = relationship("Challenge", back_populates="company")
    projects: Mapped[List["Project"]] = relationship("Project", back_populates="company")
    
    def __repr__(self):
        return f"<Company(id={self.id}, name='{self.name}')>"


class Challenge(Base):
    """Challenge model for storing engineering challenges."""
    
    __tablename__ = "challenges"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=True)  # e.g., "backend", "frontend", "data"
    difficulty = Column(String(50), nullable=True)  # e.g., "easy", "medium", "hard"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    company: Mapped["Company"] = relationship("Company", back_populates="challenges")
    projects: Mapped[List["Project"]] = relationship("Project", back_populates="challenge")
    
    def __repr__(self):
        return f"<Challenge(id={self.id}, title='{self.title}', company_id={self.company_id})>"


class Project(Base):
    """Project model for storing generated project ideas."""
    
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    challenge_id = Column(Integer, ForeignKey("challenges.id"), nullable=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    tech_stack = Column(Text, nullable=False)  # JSON string of tech stack
    demo_hook = Column(Text, nullable=False)
    difficulty = Column(String(50), nullable=True)
    estimated_duration = Column(String(100), nullable=True)  # e.g., "2-3 weeks"
    is_saved = Column(Boolean, default=False)
    user_notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    company: Mapped["Company"] = relationship("Company", back_populates="projects")
    challenge: Mapped[Optional["Challenge"]] = relationship("Challenge", back_populates="projects")
    
    def __repr__(self):
        return f"<Project(id={self.id}, title='{self.title}', company_id={self.company_id})>"


class CacheEntry(Base):
    """Cache model for storing API responses."""
    
    __tablename__ = "cache_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(255), unique=True, index=True, nullable=False)
    value = Column(Text, nullable=False)  # JSON string
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<CacheEntry(id={self.id}, key='{self.key}')>"


class UserSession(Base):
    """User session model for storing user preferences and state."""
    
    __tablename__ = "user_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(255), unique=True, index=True, nullable=False)
    user_preferences = Column(JSON, nullable=True)  # JSON object
    saved_projects = Column(JSON, nullable=True)  # JSON array of project IDs
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<UserSession(id={self.id}, session_id='{self.session_id}')>" 