"""
Project Finder - Modular Streamlit Frontend
A clean frontend that uses the backend API for all business logic
"""

import streamlit as st
import requests
import json
import csv
import io
from typing import List, Dict, Optional
from datetime import datetime
import time

# Configure Streamlit page
st.set_page_config(
    page_title="Project Finder",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Configuration
API_BASE_URL = "http://localhost:5000"  # Default Flask API URL

# Custom CSS for modern UI
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styles */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Header styles */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        margin-bottom: 2rem;
        color: white;
    }
    
    .main-title {
        font-family: 'Inter', sans-serif;
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.2rem;
        font-weight: 400;
        opacity: 0.9;
    }
    
    /* Project card styles */
    .project-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        border: 1px solid #e0e7ff;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .project-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
    }
    
    .project-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    
    .project-title {
        font-family: 'Inter', sans-serif;
        font-size: 1.3rem;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    
    .project-challenge {
        background: #f3f4f6;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-size: 0.9rem;
        color: #6b7280;
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
    }
    
    .project-section {
        margin-bottom: 1rem;
    }
    
    .project-label {
        font-weight: 600;
        color: #374151;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.3rem;
    }
    
    .project-content {
        color: #4b5563;
        line-height: 1.6;
    }
    
    .tech-stack {
        background: #eff6ff;
        color: #1e40af;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        display: inline-block;
        margin: 0.2rem 0.2rem 0.2rem 0;
    }
    
    .demo-hook {
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-radius: 8px;
        padding: 0.8rem;
        color: #166534;
        font-style: italic;
    }
    
    /* Company section styles */
    .company-header {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 2rem 0 1rem 0;
        border-left: 6px solid #667eea;
    }
    
    .company-name {
        font-family: 'Inter', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    
    /* Stats and metrics */
    .stats-container {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        border: 1px solid #e5e7eb;
    }
    
    .stat-item {
        text-align: center;
        padding: 1rem;
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
        display: block;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Button styles */
    .stButton > button {
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s ease;
        border: none;
        font-family: 'Inter', sans-serif;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    /* Sidebar styles */
    .css-1d391kg {
        background: #f8fafc;
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    
    /* Export section */
    .export-container {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 2rem 0;
        border: 1px solid #f59e0b;
    }
    
    /* Regenerate button */
    .regenerate-btn {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: white !important;
    }
    
    /* Success/Warning/Error messages */
    .stSuccess {
        border-radius: 12px;
    }
    
    .stWarning {
        border-radius: 12px;
    }
    
    .stError {
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'projects' not in st.session_state:
    st.session_state.projects = []
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""
if 'processing' not in st.session_state:
    st.session_state.processing = False

class APIClient:
    """Client for interacting with the backend API"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
    
    def analyze_company(self, company_name: str, api_key: str, user_skills: List[str] = None, total_ideas: int = 4) -> Dict:
        """Analyze a company using the backend API"""
        url = f"{self.base_url}/api/analyze-company"
        payload = {
            "company_name": company_name,
            "api_key": api_key,
            "user_skills": user_skills or [],
            "ideas_per_challenge": total_ideas
        }
        
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    
    def get_company_profile(self, company_name: str) -> Dict:
        """Get company profile only"""
        url = f"{self.base_url}/api/company-profile/{company_name}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    
    def get_engineering_challenges(self, company_name: str) -> List[Dict]:
        """Get engineering challenges for a company"""
        url = f"{self.base_url}/api/engineering-challenges/{company_name}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    
    def generate_projects(self, company_name: str, challenges: List[str], user_skills: List[str] = None, ideas_per_challenge: int = 4) -> Dict:
        """Generate projects for a company"""
        url = f"{self.base_url}/api/generate-projects"
        payload = {
            "company_name": company_name,
            "challenges": challenges,
            "user_skills": user_skills or [],
            "ideas_per_challenge": ideas_per_challenge
        }
        
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    
    def refine_project(self, project: Dict, company_name: str, challenge_description: str) -> Dict:
        """Refine an existing project idea"""
        url = f"{self.base_url}/api/refine-project"
        payload = {
            "project": project,
            "company_name": company_name,
            "challenge_description": challenge_description
        }
        
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    
    def health_check(self) -> bool:
        """Check if the API is healthy"""
        try:
            url = f"{self.base_url}/health"
            response = requests.get(url, timeout=5)
            return response.status_code == 200
        except:
            return False

def setup_api_key():
    """Handle API key setup with modal popup"""
    
    # Check if API key is already set
    if st.session_state.api_key:
        return st.session_state.api_key
    
    # Create a modal-like experience using columns and containers
    with st.container():
        # Overlay effect
        st.markdown("""
        <style>
        .modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            z-index: 1000;
        }
        .modal-content {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: white;
            padding: 2rem;
            border-radius: 16px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
            z-index: 1001;
            max-width: 500px;
            width: 90%;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Modal content
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        border-radius: 16px; color: white; margin-bottom: 2rem;">
                <h2 style="margin: 0; color: white;">🔑 API Key Required</h2>
                <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Enter your Gemini API key to get started</p>
            </div>
            """, unsafe_allow_html=True)
            
            # API key input
            api_key = st.text_input(
                "🔐 Enter your Gemini API Key:",
                type="password",
                placeholder="Your API key here...",
                help="Get your API key from Google AI Studio"
            )
            
            if api_key:
                st.session_state.api_key = api_key
                st.success("✅ API key saved successfully!")
                st.rerun()
            
            # Help section
            with st.expander("❓ Need help getting an API key?", expanded=False):
                st.markdown("""
                **Quick Steps:**
                1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
                2. Sign in with your Google account
                3. Click "Create API Key"
                4. Copy and paste it above
                
                **It's completely free!** 🎉
                """)
            
            # Get API key button
            if st.button("🔑 Get Free API Key", type="secondary", use_container_width=True):
                st.markdown("""
                <script>
                window.open('https://makersuite.google.com/app/apikey', '_blank');
                </script>
                """, unsafe_allow_html=True)
                st.info("Opening Google AI Studio in a new tab...")
    
    return st.session_state.api_key

def main():
    """Main application function"""
    
    # Modern Header
    st.markdown("""
    <div class="main-header">
        <div class="main-title">🚀 Project Finder</div>
        <div class="main-subtitle">Discover AI-powered side projects tailored for your dream companies</div>
    </div>
    """, unsafe_allow_html=True)
    
    # API Key Setup
    api_key = setup_api_key()
    
    if not api_key:
        # The modal will handle the API key input, so we just return here
        return
    
    # Initialize API client
    api_client = APIClient(API_BASE_URL)
    
    # Check API health
    if not api_client.health_check():
        st.error("❌ Backend API is not available. Please ensure the backend server is running.")
        st.info("💡 Start the backend server with: `python -m backend.server`")
        return
    
    # Main controls section
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); 
                padding: 2rem; border-radius: 16px; margin: 2rem 0; border: 1px solid #cbd5e0;">
        <h3 style="margin: 0; color: #2d3748; text-align: center;">🎯 Project Settings</h3>
        <p style="margin: 0.5rem 0 0 0; color: #718096; text-align: center; font-size: 0.9rem;">Customize your project generation</p>
    </div>
    """, unsafe_allow_html=True)
    
    # API Key status and change button
    col1, col2 = st.columns([3, 1])
    with col1:
        if api_key:
            st.success("✅ API Key: Configured")
        else:
            st.error("❌ API Key: Not configured")
    
    with col2:
        if st.button("🔑 Change API Key", type="secondary", use_container_width=True):
            st.session_state.api_key = ""
            st.rerun()
    
    # Project settings in columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Generation Settings")
        
        # Number of ideas selector with radio buttons
        ideas_count = st.radio(
            "💡 Ideas per challenge:",
            options=[2, 4, 6, 8, 10, 12],
            index=1,  # Default to 4 (now index 1 since 2 is at index 0)
            help="Choose how many project ideas to generate for each engineering challenge",
            horizontal=True
        )
        
        # Show total expected projects (literal count)
        st.info(f"📈 Expected output: {ideas_count} projects per company ({ideas_count} ideas total)")
    
    with col2:
        st.markdown("### 🏢 Target Company")
        company_name = st.text_input(
            "Enter company name:",
            placeholder="Google, Microsoft, OpenAI, Netflix, Uber, Spotify",
            help="Enter the company you're interested in working for"
        )
        
        # Company indicator
        if company_name.strip():
            st.success(f"🎯 Company: {company_name}")
    
    # Skills section
    st.markdown("### 🛠️ Your Skills")
    user_skills = st.text_input(
        "Your technical skills (optional):",
        placeholder="Python, React, Machine Learning, AWS, Docker",
        help="This will help tailor project suggestions to your strengths"
    )
    
    # Skills preview
    if user_skills.strip():
        skills_list = [skill.strip() for skill in user_skills.split(',') if skill.strip()]
        st.info(f"🔧 {len(skills_list)} skills detected: {', '.join(skills_list[:3])}{'...' if len(skills_list) > 3 else ''}")
    
    # Action buttons
    st.markdown("### 🚀 Actions")
    
    # Disable generate button if no company or no API key
    can_generate = bool(api_key and company_name.strip())
    
    col1, col2 = st.columns(2)
    
    with col1:
        generate_btn = st.button(
            "🔍 Generate Ideas", 
            type="primary", 
            use_container_width=True,
            disabled=not can_generate,
            help="Generate AI-powered project ideas" if can_generate else "Enter company and API key first"
        )
    
    with col2:
        clear_btn = st.button(
            "🗑️ Clear All", 
            use_container_width=True,
            help="Clear all generated projects"
        )
    
    # Show generation info
    if can_generate and company_name.strip():
        st.markdown(f"""
        <div style="background: #e6fffa; padding: 1rem; border-radius: 8px; border-left: 4px solid #38b2ac; margin-top: 1rem;">
            <strong style="color: #2c7a7b;">Ready to Generate!</strong><br>
            <span style="color: #285e61; font-size: 0.9rem;">
                🎯 {company_name}<br>
                📊 {ideas_count} total projects<br>
                ⏱️ ~30s estimated time
            </span>
        </div>
        """, unsafe_allow_html=True)
    
    # Process company
    if generate_btn and company_name.strip():
        company = company_name.strip()
        
        if company:
            st.session_state.processing = True
            st.session_state.projects = []
            
            # Modern progress tracking
            st.markdown("### 🔄 Generating Your Custom Projects")
            
            progress_container = st.container()
            with progress_container:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Create a beautiful status card
                status_card = st.empty()
            
            try:
                # Update status card
                status_card.markdown(f"""
                <div style="background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); 
                            padding: 1.5rem; border-radius: 12px; border: 1px solid #93c5fd; margin: 1rem 0;">
                    <div style="display: flex; align-items: center; justify-content: space-between;">
                        <div>
                            <h4 style="color: #1e40af; margin: 0;">Processing {company}</h4>
                            <p style="color: #3730a3; margin: 0.5rem 0 0 0;">Analyzing company and generating ideas</p>
                        </div>
                        <div style="font-size: 2rem;">🏢</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Step 1: Analyze company
                status_text.markdown(f"**Step 1/2:** 📊 Analyzing {company} company profile...")
                progress_bar.progress(0.3)
                
                # Parse skills
                skills_list = [skill.strip() for skill in user_skills.split(',') if skill.strip()] if user_skills else []
                
                # Call API to analyze company
                analysis_result = api_client.analyze_company(
                    company_name=company,
                    api_key=api_key,
                    user_skills=skills_list,
                    total_ideas=ideas_count
                )
                
                progress_bar.progress(0.6)
                
                # Step 2: Process results
                status_text.markdown(f"**Step 2/2:** 🚀 Processing generated ideas...")
                progress_bar.progress(0.8)
                
                # Convert API response to our format
                projects = []
                if 'project_ideas' in analysis_result:
                    for project in analysis_result['project_ideas']:
                        # Convert to the format expected by the frontend
                        frontend_project = {
                            'title': project.get('title', 'Untitled Project'),
                            'description': project.get('description', ''),
                            'tech_stack': ', '.join(project.get('tech_stack', [])),
                            'demo_hook': project.get('demo_hook', ''),
                            'company': company,
                            'challenge': project.get('challenge_id', 'Unknown Challenge'),
                            'difficulty': project.get('difficulty', 'intermediate'),
                            'estimated_duration': project.get('estimated_duration', '1-2 months')
                        }
                        projects.append(frontend_project)
                
                st.session_state.projects = projects
                progress_bar.progress(1.0)
                
                # Success feedback
                status_text.markdown(f"✅ **Completed {company}** - Generated {len(projects)} projects!")
                
            except Exception as e:
                st.error(f"❌ Error processing {company}: {str(e)}")
            
            # Clear progress elements
            progress_bar.empty()
            status_text.empty()
            status_card.empty()
            st.session_state.processing = False
            
            if st.session_state.projects:
                st.balloons()  # Celebration animation!
                st.success(f"🎉 Successfully generated {len(st.session_state.projects)} project ideas for {company}!")
            else:
                st.warning("⚠️ No projects were generated. Please try again or check your company name.")
    
    # Clear all projects
    if clear_btn:
        st.session_state.projects = []
        st.success("✨ All projects cleared! Ready for new ideas.")
    
    # Display stats if we have projects
    if st.session_state.projects:
        # Calculate stats
        total_projects = len(st.session_state.projects)
        unique_techs = len(set(tech.strip() for project in st.session_state.projects 
                              for tech in project.get('tech_stack', '').split(',')))
        
        # Stats display
        st.markdown("""
        <div class="stats-container">
            <div style="text-align: center; margin-bottom: 1rem;">
                <h3 style="color: #374151; margin: 0;">📊 Generation Summary</h3>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="stat-item">
                <span class="stat-number">{total_projects}</span>
                <span class="stat-label">Projects Generated</span>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="stat-item">
                <span class="stat-number">1</span>
                <span class="stat-label">Company Analyzed</span>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="stat-item">
                <span class="stat-number">{unique_techs}</span>
                <span class="stat-label">Technologies Suggested</span>
            </div>
            """, unsafe_allow_html=True)
    
    # Display results
    if st.session_state.projects:
        # Group projects by company
        companies_projects = {}
        for project in st.session_state.projects:
            company = project['company']
            if company not in companies_projects:
                companies_projects[company] = []
            companies_projects[company].append(project)
        
        # Display projects for each company
        for company, projects in companies_projects.items():
            # Company header with regenerate option
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"""
                <div class="company-header">
                    <div class="company-name">🏢 {company}</div>
                    <div style="color: #6b7280; font-size: 1rem;">{len(projects)} project ideas generated</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)  # Spacing
                if st.button(f"🔄 Regenerate", key=f"regen_{company}", help=f"Generate new ideas for {company}"):
                    # Regenerate for this company
                    with st.spinner(f"Regenerating ideas for {company}..."):
                        try:
                            # Parse skills
                            skills_list = [skill.strip() for skill in user_skills.split(',') if skill.strip()] if user_skills else []
                            
                            # Call API to regenerate
                            analysis_result = api_client.analyze_company(
                                company_name=company,
                                api_key=api_key,
                                user_skills=skills_list,
                                total_ideas=ideas_count
                            )
                            
                            # Convert and update projects
                            new_projects = []
                            if 'project_ideas' in analysis_result:
                                for project in analysis_result['project_ideas']:
                                    frontend_project = {
                                        'title': project.get('title', 'Untitled Project'),
                                        'description': project.get('description', ''),
                                        'tech_stack': ', '.join(project.get('tech_stack', [])),
                                        'demo_hook': project.get('demo_hook', ''),
                                        'company': company,
                                        'challenge': project.get('challenge_id', 'Unknown Challenge'),
                                        'difficulty': project.get('difficulty', 'intermediate'),
                                        'estimated_duration': project.get('estimated_duration', '1-2 months')
                                    }
                                    new_projects.append(frontend_project)
                            
                            # Replace projects for this company
                            st.session_state.projects = [p for p in st.session_state.projects if p['company'] != company]
                            st.session_state.projects.extend(new_projects)
                            
                            st.success(f"✨ Generated {len(new_projects)} new ideas for {company}!")
                            st.rerun()
                            
                        except Exception as e:
                            st.error(f"Error regenerating for {company}: {str(e)}")
            
            # Display projects in a modern grid
            for i in range(0, len(projects), 2):
                col1, col2 = st.columns(2, gap="large")
                
                for j, col in enumerate([col1, col2]):
                    if i + j < len(projects):
                        project = projects[i + j]
                        
                        # Parse tech stack for better display
                        tech_items = [tech.strip() for tech in project.get('tech_stack', '').split(',')]
                        tech_badges = ''.join([f'<span class="tech-stack">{tech}</span>' for tech in tech_items if tech])
                        
                        with col:
                            st.markdown(f"""
                            <div class="project-card">
                                <div class="project-title">{project.get('title', 'Untitled Project')}</div>
                                
                                <div class="project-challenge">
                                    <strong>Challenge:</strong> {project.get('challenge', 'N/A')}
                                </div>
                                
                                <div class="project-section">
                                    <div class="project-label">Description</div>
                                    <div class="project-content">{project.get('description', 'No description available')}</div>
                                </div>
                                
                                <div class="project-section">
                                    <div class="project-label">Tech Stack</div>
                                    <div>{tech_badges}</div>
                                </div>
                                
                                <div class="project-section">
                                    <div class="project-label">Demo Hook</div>
                                    <div class="demo-hook">
                                        💡 {project.get('demo_hook', 'No demo hook provided')}
                                    </div>
                                </div>
                                
                                <div class="project-section">
                                    <div class="project-label">Difficulty & Duration</div>
                                    <div class="project-content">
                                        <strong>Difficulty:</strong> {project.get('difficulty', 'intermediate').title()}<br>
                                        <strong>Duration:</strong> {project.get('estimated_duration', '1-2 months')}
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
            
            st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Export options with modern design
        st.markdown("""
        <div class="export-container">
            <h3 style="color: #92400e; margin-bottom: 1rem; text-align: center;">💾 Export Your Ideas</h3>
            <p style="color: #a16207; text-align: center; margin-bottom: 1.5rem;">
                Save your generated projects for future reference and portfolio planning
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            # JSON export
            json_data = json.dumps(st.session_state.projects, indent=2)
            st.download_button(
                label="📁 Download JSON",
                data=json_data,
                file_name=f"project_ideas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        with col2:
            # CSV export
            csv_buffer = io.StringIO()
            fieldnames = ['company', 'title', 'description', 'tech_stack', 'demo_hook', 'challenge', 'difficulty', 'estimated_duration']
            writer = csv.DictWriter(csv_buffer, fieldnames=fieldnames)
            writer.writeheader()
            
            for project in st.session_state.projects:
                writer.writerow({
                    'company': project.get('company', ''),
                    'title': project.get('title', ''),
                    'description': project.get('description', ''),
                    'tech_stack': project.get('tech_stack', ''),
                    'demo_hook': project.get('demo_hook', ''),
                    'challenge': project.get('challenge', ''),
                    'difficulty': project.get('difficulty', ''),
                    'estimated_duration': project.get('estimated_duration', '')
                })
            
            st.download_button(
                label="📊 Download CSV",
                data=csv_buffer.getvalue(),
                file_name=f"project_ideas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col3:
            # Generate README for selected projects
            readme_content = f"""# My Project Ideas - Generated on {datetime.now().strftime('%B %d, %Y')}

Generated using Project Finder - AI-powered project discovery tool.

## Company Analyzed
{company}

## Project Summary
Total Projects: {len(st.session_state.projects)}

"""
            for project in st.session_state.projects:
                readme_content += f"\n## {project.get('title', 'Untitled')}\n\n"
                readme_content += f"**Challenge:** {project.get('challenge', 'N/A')}\n\n"
                readme_content += f"**Description:** {project.get('description', 'N/A')}\n\n"
                readme_content += f"**Tech Stack:** {project.get('tech_stack', 'N/A')}\n\n"
                readme_content += f"**Demo Hook:** {project.get('demo_hook', 'N/A')}\n\n"
                readme_content += f"**Difficulty:** {project.get('difficulty', 'N/A')}\n\n"
                readme_content += f"**Duration:** {project.get('estimated_duration', 'N/A')}\n\n"
                readme_content += "---\n\n"
            
            st.download_button(
                label="📝 Download README",
                data=readme_content,
                file_name=f"PROJECT_IDEAS_{datetime.now().strftime('%Y%m%d')}.md",
                mime="text/markdown",
                use_container_width=True
            )
    
    # Footer with modern design
    st.markdown("""
    <div style="margin-top: 4rem; padding: 2rem; background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); 
                border-radius: 16px; text-align: center; border: 1px solid #e5e7eb;">
        <h4 style="color: #374151; margin-bottom: 1rem;">🎯 Pro Tips for Success</h4>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem; margin-top: 1rem;">
            <div style="background: white; padding: 1rem; border-radius: 8px; border-left: 4px solid #10b981;">
                <strong style="color: #059669;">💼 Portfolio Strategy:</strong><br>
                <span style="color: #6b7280;">Pick 2-3 projects that showcase different skills and build them incrementally.</span>
            </div>
            <div style="background: white; padding: 1rem; border-radius: 8px; border-left: 4px solid #3b82f6;">
                <strong style="color: #1d4ed8;">🚀 Demo Excellence:</strong><br>
                <span style="color: #6b7280;">Focus on live demos, clear documentation, and measurable results.</span>
            </div>
            <div style="background: white; padding: 1rem; border-radius: 8px; border-left: 4px solid #f59e0b;">
                <strong style="color: #d97706;">🎯 Interview Prep:</strong><br>
                <span style="color: #6b7280;">Prepare to explain your technical choices and project impact.</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 