"""
Project Finder - AI-Powered Side Project Generator
A Streamlit app that helps users discover custom side projects for target companies
using Google's Gemini API to showcase relevant skills and win interviews.
"""

import streamlit as st
import google.generativeai as genai
import json
import csv
import io
import os
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

class GeminiService:
    """Service class for interacting with Google Gemini API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def get_company_profile(self, company_name: str) -> str:
        """Get a concise company profile including industry, tech stack, and recent highlights"""
        prompt = f"""
        Provide a concise profile for the company "{company_name}". Include:
        1. Industry domain and business focus
        2. Likely tech stack and technologies they use
        3. Recent highlights, products, or news (if known)
        
        Keep it under 200 words and focus on information relevant for a job seeker.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            st.error(f"Error getting company profile: {str(e)}")
            return ""
    
    def get_engineering_challenges(self, company_name: str, profile: str) -> List[str]:
        """Identify 3 common engineering challenges for the company"""
        prompt = f"""
        Based on this company profile for {company_name}:
        
        {profile}
        
        List exactly 3 common engineering challenges or product areas this company likely faces.
        Format as a numbered list. Keep each challenge description concise (1-2 sentences).
        Focus on technical challenges that would be relevant for software engineers.
        """
        
        try:
            response = self.model.generate_content(prompt)
            challenges = []
            lines = response.text.strip().split('\n')
            for line in lines:
                if line.strip() and (line.strip().startswith(tuple('123456789')) or line.strip().startswith('*') or line.strip().startswith('-')):
                    # Clean up the challenge text
                    challenge = line.strip()
                    # Remove numbering and bullet points
                    challenge = challenge.lstrip('123456789.*- ')
                    if challenge:
                        challenges.append(challenge)
            return challenges[:3]  # Ensure we only return 3 challenges
        except Exception as e:
            st.error(f"Error getting engineering challenges: {str(e)}")
            return []
    
    def generate_project_ideas(self, company_name: str, challenges: List[str], ideas_per_challenge: int = 4) -> List[Dict]:
        """Generate customizable number of project ideas for each challenge"""
        all_projects = []
        
        for i, challenge in enumerate(challenges, 1):
            prompt = f"""
            For the company "{company_name}" and this engineering challenge:
            
            Challenge {i}: {challenge}
            
            Generate exactly {ideas_per_challenge} concrete side project ideas that someone could build to demonstrate relevant skills.
            
            For each project, provide:
            - Title: A clear, catchy project name
            - Description: Brief description (2-3 sentences)
            - Tech Stack: Specific technologies/frameworks to use
            - Demo Hook: What to show in an interview that would impress
            
            Format as JSON array like this:
            [
                {{
                    "title": "Project Title",
                    "description": "Brief description here",
                    "tech_stack": "Technology, Framework, Database",
                    "demo_hook": "What to demonstrate"
                }}
            ]
            """
            
            try:
                response = self.model.generate_content(prompt)
                response_text = response.text.strip()
                
                # Extract JSON from response
                if '```json' in response_text:
                    json_start = response_text.find('```json') + 7
                    json_end = response_text.find('```', json_start)
                    json_text = response_text[json_start:json_end]
                elif '[' in response_text and ']' in response_text:
                    json_start = response_text.find('[')
                    json_end = response_text.rfind(']') + 1
                    json_text = response_text[json_start:json_end]
                else:
                    json_text = response_text
                
                try:
                    projects = json.loads(json_text)
                    for project in projects:
                        project['company'] = company_name
                        project['challenge'] = challenge
                        project['challenge_number'] = i
                    all_projects.extend(projects)
                except json.JSONDecodeError:
                    # Fallback: parse manually if JSON parsing fails
                    st.warning(f"Could not parse JSON for challenge {i}, using fallback parsing")
                    continue
                    
            except Exception as e:
                st.error(f"Error generating project ideas for challenge {i}: {str(e)}")
                continue
        
        return all_projects

def setup_api_key():
    """Handle API key setup with modern UI"""
    st.sidebar.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem; color: white; text-align: center;">
        <h3 style="margin: 0; color: white;">🔑 API Configuration</h3>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 0.9rem;">Secure access to Gemini AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Try multiple sources for API key
    api_key = ""
    
    # 1. Try environment variable first
    api_key = os.getenv('GEMINI_API_KEY', '')
    
    # 2. Try Streamlit secrets (safely)
    if not api_key:
        try:
            if hasattr(st, 'secrets') and st.secrets:
                api_key = st.secrets.get("GEMINI_API_KEY", "")
        except Exception:
            # Secrets file doesn't exist or can't be read, that's fine
            pass
    
    # 3. If still no API key, ask user to input it
    if not api_key:
        api_key = st.sidebar.text_input(
            "🔐 Enter your Gemini API Key:",
            type="password",
            value=st.session_state.api_key,
            help="Get your API key from Google AI Studio",
            placeholder="Your API key here..."
        )
        
        if api_key:
            st.session_state.api_key = api_key
        
        # Help section
        with st.sidebar.expander("❓ Need help getting an API key?"):
            st.markdown("""
            **Quick Steps:**
            1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
            2. Sign in with your Google account
            3. Click "Create API Key"
            4. Copy and paste it above
            
            **It's completely free!** 🎉
            """)
    else:
        # If we found the API key from env/secrets, show a success message
        st.sidebar.success("✅ API key loaded successfully")
        st.sidebar.info("🔒 Your API key is securely configured")
    
    return api_key

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
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: #fef2f2; border-radius: 12px; border: 1px solid #fecaca;">
            <h3 style="color: #dc2626; margin-bottom: 1rem;">🔑 API Key Required</h3>
            <p style="color: #7f1d1d;">Please enter your Gemini API key in the sidebar to get started.</p>
            <a href="https://makersuite.google.com/app/apikey" target="_blank" 
               style="display: inline-block; margin-top: 1rem; padding: 0.75rem 1.5rem; 
                      background: linear-gradient(135deg, #dc2626, #b91c1c); color: white; 
                      text-decoration: none; border-radius: 8px; font-weight: 600;">
                Get Your Free API Key →
            </a>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Initialize Gemini service
    gemini_service = GeminiService(api_key)
    
    # Sidebar controls with modern design
    st.sidebar.markdown("""
    <div style="background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); 
                padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem; border: 1px solid #cbd5e0;">
        <h3 style="margin: 0; color: #2d3748; text-align: center;">🎯 Project Settings</h3>
        <p style="margin: 0.5rem 0 0 0; color: #718096; text-align: center; font-size: 0.9rem;">Customize your project generation</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Number of ideas selector with better styling
    st.sidebar.markdown("### 📊 Generation Settings")
    ideas_count = st.sidebar.selectbox(
        "💡 Ideas per challenge:",
        options=[4, 6, 8, 10, 12],
        index=0,  # Default to 4
        help="Choose how many project ideas to generate for each engineering challenge"
    )
    
    # Show total expected projects
    st.sidebar.info(f"📈 Expected output: ~{ideas_count * 3} projects per company (3 challenges × {ideas_count} ideas)")
    
    # Company input with better design
    st.sidebar.markdown("### 🏢 Target Companies")
    company_input = st.sidebar.text_area(
        "Enter company names (one per line):",
        placeholder="Google\nMicrosoft\nOpenAI\nNetflix\nUber\nSpotify",
        height=140,
        help="Add companies you're interested in working for"
    )
    
    # Company count indicator
    if company_input.strip():
        company_count = len([c.strip() for c in company_input.strip().split('\n') if c.strip()])
        st.sidebar.success(f"🎯 {company_count} companies selected")
    
    # Optional skills input with improved design
    st.sidebar.markdown("### 🛠️ Your Skills")
    user_skills = st.sidebar.text_input(
        "Your technical skills (optional):",
        placeholder="Python, React, Machine Learning, AWS, Docker",
        help="This will help tailor project suggestions to your strengths"
    )
    
    # Skills preview
    if user_skills.strip():
        skills_list = [skill.strip() for skill in user_skills.split(',') if skill.strip()]
        st.sidebar.info(f"🔧 {len(skills_list)} skills detected: {', '.join(skills_list[:3])}{'...' if len(skills_list) > 3 else ''}")
    
    # Action buttons with modern styling
    st.sidebar.markdown("### 🚀 Actions")
    
    # Disable generate button if no companies or no API key
    can_generate = bool(api_key and company_input.strip())
    
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        generate_btn = st.button(
            "🔍 Generate Ideas", 
            type="primary", 
            use_container_width=True,
            disabled=not can_generate,
            help="Generate AI-powered project ideas" if can_generate else "Enter companies and API key first"
        )
    
    with col2:
        clear_btn = st.button(
            "🗑️ Clear All", 
            use_container_width=True,
            help="Clear all generated projects"
        )
    
    # Show generation info
    if can_generate and company_input.strip():
        company_count = len([c.strip() for c in company_input.strip().split('\n') if c.strip()])
        estimated_projects = company_count * 3 * ideas_count
        st.sidebar.markdown(f"""
        <div style="background: #e6fffa; padding: 1rem; border-radius: 8px; border-left: 4px solid #38b2ac; margin-top: 1rem;">
            <strong style="color: #2c7a7b;">Ready to Generate!</strong><br>
            <span style="color: #285e61; font-size: 0.9rem;">
                📊 {company_count} companies<br>
                🎯 ~{estimated_projects} total projects<br>
                ⏱️ ~{company_count * 30}s estimated time
            </span>
        </div>
        """, unsafe_allow_html=True)
    
    # Process companies
    if generate_btn and company_input.strip():
        companies = [company.strip() for company in company_input.strip().split('\n') if company.strip()]
        
        if companies:
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
            
            total_steps = len(companies) * 3  # 3 steps per company
            current_step = 0
            
            for company_idx, company in enumerate(companies, 1):
                try:
                    # Update status card
                    status_card.markdown(f"""
                    <div style="background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); 
                                padding: 1.5rem; border-radius: 12px; border: 1px solid #93c5fd; margin: 1rem 0;">
                        <div style="display: flex; align-items: center; justify-content: space-between;">
                            <div>
                                <h4 style="color: #1e40af; margin: 0;">Processing {company}</h4>
                                <p style="color: #3730a3; margin: 0.5rem 0 0 0;">Company {company_idx} of {len(companies)}</p>
                            </div>
                            <div style="font-size: 2rem;">🏢</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Step 1: Get company profile
                    status_text.markdown(f"**Step 1/3:** 📊 Analyzing {company} company profile...")
                    profile = gemini_service.get_company_profile(company)
                    current_step += 1
                    progress_bar.progress(current_step / total_steps)
                    
                    if not profile:
                        continue
                    
                    # Step 2: Get engineering challenges
                    status_text.markdown(f"**Step 2/3:** 🔍 Identifying engineering challenges for {company}...")
                    challenges = gemini_service.get_engineering_challenges(company, profile)
                    current_step += 1
                    progress_bar.progress(current_step / total_steps)
                    
                    if not challenges:
                        continue
                    
                    # Step 3: Generate project ideas
                    status_text.markdown(f"**Step 3/3:** 🚀 Generating {ideas_count} project ideas per challenge for {company}...")
                    projects = gemini_service.generate_project_ideas(company, challenges, ideas_count)
                    current_step += 1
                    progress_bar.progress(current_step / total_steps)
                    
                    # Add profile and challenges to projects
                    for project in projects:
                        project['company_profile'] = profile
                    
                    st.session_state.projects.extend(projects)
                    
                    # Success feedback for this company
                    status_text.markdown(f"✅ **Completed {company}** - Generated {len(projects)} projects!")
                    
                    # Small delay to avoid rate limiting
                    time.sleep(0.5)
                    
                except Exception as e:
                    st.error(f"❌ Error processing {company}: {str(e)}")
                    continue
            
            # Clear progress elements
            progress_bar.empty()
            status_text.empty()
            status_card.empty()
            st.session_state.processing = False
            
            if st.session_state.projects:
                st.balloons()  # Celebration animation!
                st.success(f"🎉 Successfully generated {len(st.session_state.projects)} project ideas across {len(companies)} companies!")
            else:
                st.warning("⚠️ No projects were generated. Please try again or check your company names.")
    
    # Clear all projects
    if clear_btn:
        st.session_state.projects = []
        st.success("✨ All projects cleared! Ready for new ideas.")
    
    # Display stats if we have projects
    if st.session_state.projects:
        # Calculate stats
        total_projects = len(st.session_state.projects)
        unique_companies = len(set(project['company'] for project in st.session_state.projects))
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
                <span class="stat-number">{unique_companies}</span>
                <span class="stat-label">Companies Analyzed</span>
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
                    # Find the company in the input and regenerate
                    company_list = [c.strip() for c in company_input.strip().split('\n') if c.strip()]
                    if company in company_list:
                        # Remove existing projects for this company
                        st.session_state.projects = [p for p in st.session_state.projects if p['company'] != company]
                        
                        # Regenerate for this company
                        with st.spinner(f"Regenerating ideas for {company}..."):
                            try:
                                profile = gemini_service.get_company_profile(company)
                                if profile:
                                    challenges = gemini_service.get_engineering_challenges(company, profile)
                                    if challenges:
                                        new_projects = gemini_service.generate_project_ideas(company, challenges, ideas_count)
                                        for project in new_projects:
                                            project['company_profile'] = profile
                                        st.session_state.projects.extend(new_projects)
                                        st.success(f"✨ Generated {len(new_projects)} new ideas for {company}!")
                                        st.rerun()
                            except Exception as e:
                                st.error(f"Error regenerating for {company}: {str(e)}")
            
            # Company profile expander
            if projects and 'company_profile' in projects[0]:
                with st.expander(f"📊 View {company} Company Profile", expanded=False):
                    st.markdown(f"""
                    <div style="background: #f8fafc; padding: 1rem; border-radius: 8px; line-height: 1.6;">
                        {projects[0]['company_profile']}
                    </div>
                    """, unsafe_allow_html=True)
            
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
            fieldnames = ['company', 'title', 'description', 'tech_stack', 'demo_hook', 'challenge']
            writer = csv.DictWriter(csv_buffer, fieldnames=fieldnames)
            writer.writeheader()
            
            for project in st.session_state.projects:
                writer.writerow({
                    'company': project.get('company', ''),
                    'title': project.get('title', ''),
                    'description': project.get('description', ''),
                    'tech_stack': project.get('tech_stack', ''),
                    'demo_hook': project.get('demo_hook', ''),
                    'challenge': project.get('challenge', '')
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

## Companies Analyzed
{', '.join(companies_projects.keys())}

## Project Summary
Total Projects: {len(st.session_state.projects)}

"""
            for company, projects in companies_projects.items():
                readme_content += f"\n## {company}\n\n"
                for project in projects:
                    readme_content += f"### {project.get('title', 'Untitled')}\n"
                    readme_content += f"**Challenge:** {project.get('challenge', 'N/A')}\n\n"
                    readme_content += f"**Description:** {project.get('description', 'N/A')}\n\n"
                    readme_content += f"**Tech Stack:** {project.get('tech_stack', 'N/A')}\n\n"
                    readme_content += f"**Demo Hook:** {project.get('demo_hook', 'N/A')}\n\n"
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
