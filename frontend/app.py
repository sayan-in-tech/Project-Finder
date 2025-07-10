"""
Project Finder - Streamlit Frontend
Main application for discovering custom side-projects for target companies.
"""

import streamlit as st
import requests
import json
import pandas as pd
from typing import Dict, List, Any
import time
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Project Finder",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #FF6B6B;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #4A90E2;
        margin-bottom: 1rem;
    }
    .project-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 4px solid #FF6B6B;
    }
    .tech-stack {
        display: inline-block;
        background-color: #E3F2FD;
        color: #1976D2;
        padding: 0.2rem 0.5rem;
        border-radius: 15px;
        font-size: 0.8rem;
        margin: 0.1rem;
    }
    .difficulty-badge {
        display: inline-block;
        padding: 0.2rem 0.5rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
    }
    .difficulty-easy { background-color: #C8E6C9; color: #2E7D32; }
    .difficulty-medium { background-color: #FFF3E0; color: #F57C00; }
    .difficulty-hard { background-color: #FFCDD2; color: #C62828; }
    .stButton > button {
        background-color: #FF6B6B;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #E55A5A;
    }
</style>
""", unsafe_allow_html=True)

# API configuration
API_BASE_URL = "http://localhost:8000/api/v1"

def make_api_request(endpoint: str, params: Dict = None) -> Dict:
    """Make API request to backend."""
    try:
        url = f"{API_BASE_URL}/{endpoint}"
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return None

def make_post_request(endpoint: str, data: Dict = None) -> Dict:
    """Make POST API request to backend."""
    try:
        url = f"{API_BASE_URL}/{endpoint}"
        response = requests.post(url, json=data, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return None

def get_difficulty_color(difficulty: str) -> str:
    """Get CSS class for difficulty badge."""
    difficulty = difficulty.lower()
    if difficulty == "easy":
        return "difficulty-easy"
    elif difficulty == "medium":
        return "difficulty-medium"
    elif difficulty == "hard":
        return "difficulty-hard"
    return "difficulty-medium"

def display_project_card(project: Dict, company_name: str):
    """Display a project card with all details."""
    with st.container():
        st.markdown(f"""
        <div class="project-card">
            <h3>{project['title']}</h3>
            <p><strong>Description:</strong> {project['description']}</p>
            <p><strong>Demo Hook:</strong> {project['demo_hook']}</p>
            <p><strong>Tech Stack:</strong></p>
            <div>
        """, unsafe_allow_html=True)
        
        # Display tech stack as badges
        for tech in project.get('tech_stack', []):
            st.markdown(f'<span class="tech-stack">{tech}</span>', unsafe_allow_html=True)
        
        st.markdown(f"""
            </div>
            <p><strong>Duration:</strong> {project.get('estimated_duration', '2-3 weeks')}</p>
            <p><strong>Difficulty:</strong> 
                <span class="difficulty-badge {get_difficulty_color(project.get('difficulty', 'medium'))}">
                    {project.get('difficulty', 'medium').title()}
                </span>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Action buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"💾 Save to Workspace", key=f"save_{project['id']}"):
                save_project_to_workspace(project['id'])
        
        with col2:
            if st.button(f"📝 Add Notes", key=f"notes_{project['id']}"):
                st.session_state[f"show_notes_{project['id']}"] = True
        
        # Notes input
        if st.session_state.get(f"show_notes_{project['id']}", False):
            notes = st.text_area("Add notes for this project:", key=f"notes_input_{project['id']}")
            if st.button("Save Notes", key=f"save_notes_{project['id']}"):
                save_project_with_notes(project['id'], notes)
                st.session_state[f"show_notes_{project['id']}"] = False
                st.rerun()

def save_project_to_workspace(project_id: int):
    """Save project to workspace."""
    response = make_post_request(f"projects/save/{project_id}")
    if response:
        st.success(f"Project saved to workspace!")
        time.sleep(1)
        st.rerun()

def save_project_with_notes(project_id: int, notes: str):
    """Save project with notes."""
    response = make_post_request(f"projects/save/{project_id}", {"notes": notes})
    if response:
        st.success(f"Project saved with notes!")
        time.sleep(1)
        st.rerun()

def main():
    """Main application function."""
    
    # Header
    st.markdown('<h1 class="main-header">🚀 Project Finder</h1>', unsafe_allow_html=True)
    st.markdown("""
    <p style="text-align: center; font-size: 1.2rem; color: #666;">
        Discover custom side-projects for target companies to showcase relevant skills and win interviews
    </p>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("🎯 Navigation")
        page = st.selectbox(
            "Choose a page:",
            ["🏠 Home", "💼 Company Analysis", "💾 Saved Workspace", "📊 Analytics"],
            index=["🏠 Home", "💼 Company Analysis", "💾 Saved Workspace", "📊 Analytics"].index(st.session_state.get("page", "🏠 Home")),
            key="page_selector"
        )
        # Update session state when sidebar changes
        if page != st.session_state.get("page", "🏠 Home"):
            st.session_state.page = page
        
        st.header("⚙️ Settings")
        st.info("Make sure the backend API is running on localhost:8000")
        st.info("For production, update API_BASE_URL in app.py")
        
        if st.button("🔄 Clear All Data"):
            if st.button("⚠️ Confirm Clear", key="confirm_clear"):
                response = requests.delete(f"{API_BASE_URL}/projects/clear")
                if response.status_code == 200:
                    st.success("All data cleared!")
                    time.sleep(1)
                    st.rerun()
    
    # Initialize session state
    if 'current_company' not in st.session_state:
        st.session_state.current_company = None
    if 'company_profile' not in st.session_state:
        st.session_state.company_profile = None
    if 'challenges' not in st.session_state:
        st.session_state.challenges = None
    if 'projects' not in st.session_state:
        st.session_state.projects = None
    
    # Page routing
    current_page = st.session_state.get("page", "🏠 Home")
    
    if current_page == "🏠 Home":
        show_home_page()
    elif current_page == "💼 Company Analysis":
        show_company_analysis()
    elif current_page == "💾 Saved Workspace":
        show_saved_workspace()
    elif current_page == "📊 Analytics":
        show_analytics()

def show_home_page():
    """Display the home page."""
    st.markdown('<h2 class="sub-header">Welcome to Project Finder</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    ### 🎯 What is Project Finder?
    
    Project Finder helps you discover custom side-projects for target companies to showcase relevant skills and win interviews.
    
    ### 🚀 How it works:
    
    1. **Company Analysis**: Enter a company name to get their profile, industry, and tech stack
    2. **Challenge Identification**: Discover common engineering challenges the company faces
    3. **Project Generation**: Get 3-5 concrete project ideas per challenge with tech stacks and demo hooks
    4. **Save & Organize**: Save interesting projects to your workspace for later reference
    
    ### 💡 Example Companies to Try:
    - **Netflix** - Streaming and recommendation systems
    - **Uber** - Real-time location and ride-sharing
    - **Spotify** - Music streaming and recommendation
    - **Airbnb** - Booking platform and search
    - **Stripe** - Payment processing and fintech
    
    ### 🛠️ Tech Stack:
    - **Frontend**: Streamlit with modern UI components
    - **Backend**: FastAPI with async support
    - **AI**: Google Gemini API for intelligent project generation
    - **Database**: SQLite with SQLAlchemy ORM
    - **Caching**: Redis or in-memory caching
    
    ### 🎨 Features:
    - ✨ Modern, responsive UI
    - 🔄 Real-time project generation
    - 💾 Save projects to workspace
    - 📝 Add personal notes
    - 🎯 Company-specific recommendations
    - 📊 Project difficulty and duration estimates
    """)
    
    # Quick start section
    st.markdown("### 🚀 Quick Start")
    company_input = st.text_input("Enter a company name to get started:", placeholder="e.g., Netflix, Uber, Spotify")
    
    if st.button("🔍 Analyze Company"):
        if company_input:
            st.session_state.current_company = company_input
            st.success(f"Analyzing {company_input}...")
            st.session_state.page = "💼 Company Analysis"
            st.rerun()
        else:
            st.error("Please enter a company name.")

def show_company_analysis():
    """Display the company analysis page."""
    st.markdown('<h2 class="sub-header">💼 Company Analysis</h2>', unsafe_allow_html=True)
    
    # Company input
    company_input = st.text_input(
        "Enter company name:",
        value=st.session_state.current_company or "",
        placeholder="e.g., Netflix, Uber, Spotify"
    )
    
    if st.button("🔍 Get Company Profile") and company_input:
        with st.spinner(f"Analyzing {company_input}..."):
            # Get company profile
            profile_response = make_api_request("profile", {"company": company_input})
            
            if profile_response:
                st.session_state.company_profile = profile_response
                st.session_state.current_company = company_input
                
                # Display company profile
                st.success(f"✅ Found profile for {company_input}")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("🏢 Company Profile")
                    st.write(f"**Industry:** {profile_response.get('industry', 'N/A')}")
                    st.write(f"**Summary:** {profile_response.get('summary', 'N/A')}")
                
                with col2:
                    st.subheader("🛠️ Tech Stack")
                    tech_stack = profile_response.get('tech_stack', [])
                    for tech in tech_stack:
                        st.markdown(f'- {tech}')
                
                st.subheader("📰 Recent Highlights")
                highlights = profile_response.get('recent_highlights', [])
                for highlight in highlights:
                    st.markdown(f'- {highlight}')
                
                # Get challenges
                if st.button("🎯 Get Engineering Challenges"):
                    with st.spinner("Identifying engineering challenges..."):
                        challenges_response = make_api_request("challenges", {"company": company_input})
                        
                        if challenges_response:
                            st.session_state.challenges = challenges_response
                            
                            st.subheader("🎯 Engineering Challenges")
                            for i, challenge in enumerate(challenges_response.get('challenges', [])):
                                with st.expander(f"Challenge {i+1}: {challenge['title']}"):
                                    st.write(f"**Description:** {challenge['description']}")
                                    st.write(f"**Category:** {challenge.get('category', 'N/A')}")
                                    st.write(f"**Difficulty:** {challenge.get('difficulty', 'N/A')}")
                            
                            # Get project ideas
                            if st.button("💡 Generate Project Ideas"):
                                with st.spinner("Generating project ideas..."):
                                    ideas_response = make_api_request("ideas", {"company": company_input})
                                    
                                    if ideas_response:
                                        st.session_state.projects = ideas_response
                                        
                                        st.subheader("💡 Project Ideas")
                                        st.write(f"Generated {len(ideas_response.get('projects', []))} project ideas for {company_input}")
                                        
                                        # Display projects
                                        for project in ideas_response.get('projects', []):
                                            display_project_card(project, company_input)
                                        
                                        # Regenerate button
                                        if st.button("🔄 Regenerate Ideas"):
                                            with st.spinner("Generating new ideas..."):
                                                regenerate_response = make_post_request("ideas/regenerate", {"company": company_input})
                                                if regenerate_response:
                                                    st.session_state.projects = regenerate_response
                                                    st.success("New ideas generated!")
                                                    st.rerun()

def show_saved_workspace():
    """Display the saved workspace page."""
    st.markdown('<h2 class="sub-header">💾 Saved Workspace</h2>', unsafe_allow_html=True)
    
    # Get saved projects
    saved_response = make_api_request("projects")
    
    if saved_response and saved_response.get('projects'):
        st.write(f"📁 You have {saved_response['total']} saved projects")
        
        for project in saved_response['projects']:
            with st.container():
                st.markdown(f"""
                <div class="project-card">
                    <h3>{project['title']}</h3>
                    <p><strong>Company:</strong> {project.get('company', 'N/A')}</p>
                    <p><strong>Description:</strong> {project['description']}</p>
                    <p><strong>Demo Hook:</strong> {project['demo_hook']}</p>
                    <p><strong>Tech Stack:</strong></p>
                    <div>
                """, unsafe_allow_html=True)
                
                # Display tech stack
                for tech in project.get('tech_stack', []):
                    st.markdown(f'<span class="tech-stack">{tech}</span>', unsafe_allow_html=True)
                
                st.markdown(f"""
                    </div>
                    <p><strong>Duration:</strong> {project.get('estimated_duration', 'N/A')}</p>
                    <p><strong>Difficulty:</strong> 
                        <span class="difficulty-badge {get_difficulty_color(project.get('difficulty', 'medium'))}">
                            {project.get('difficulty', 'medium').title()}
                        </span>
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # Notes display
                if project.get('user_notes'):
                    st.info(f"📝 Notes: {project['user_notes']}")
                
                # Remove button
                if st.button(f"🗑️ Remove from Workspace", key=f"remove_{project['id']}"):
                    response = requests.delete(f"{API_BASE_URL}/projects/{project['id']}")
                    if response.status_code == 200:
                        st.success("Project removed from workspace!")
                        time.sleep(1)
                        st.rerun()
    else:
        st.info("💡 No saved projects yet. Analyze a company and save some projects to get started!")

def show_analytics():
    """Display the analytics page."""
    st.markdown('<h2 class="sub-header">📊 Analytics</h2>', unsafe_allow_html=True)
    
    # Get saved projects for analytics
    saved_response = make_api_request("projects")
    
    if saved_response and saved_response.get('projects'):
        projects = saved_response['projects']
        
        # Create analytics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Saved Projects", len(projects))
        
        with col2:
            companies = set(project.get('company') for project in projects if project.get('company'))
            st.metric("Companies Analyzed", len(companies))
        
        with col3:
            difficulties = [project.get('difficulty', 'medium') for project in projects]
            easy_count = difficulties.count('easy')
            medium_count = difficulties.count('medium')
            hard_count = difficulties.count('hard')
            
            st.metric("Most Common Difficulty", "Medium" if medium_count >= max(easy_count, medium_count, hard_count) else "Easy" if easy_count >= hard_count else "Hard")
        
        # Difficulty distribution
        st.subheader("📈 Difficulty Distribution")
        difficulty_data = pd.DataFrame({
            'Difficulty': ['Easy', 'Medium', 'Hard'],
            'Count': [easy_count, medium_count, hard_count]
        })
        st.bar_chart(difficulty_data.set_index('Difficulty'))
        
        # Tech stack analysis
        st.subheader("🛠️ Tech Stack Analysis")
        all_tech = []
        for project in projects:
            all_tech.extend(project.get('tech_stack', []))
        
        if all_tech:
            tech_counts = pd.Series(all_tech).value_counts()
            st.write("Most popular technologies:")
            for tech, count in tech_counts.head(10).items():
                st.write(f"- {tech}: {count} projects")
        
        # Company analysis
        st.subheader("🏢 Company Analysis")
        company_counts = pd.Series([project.get('company') for project in projects if project.get('company')]).value_counts()
        if not company_counts.empty:
            st.write("Projects by company:")
            for company, count in company_counts.items():
                st.write(f"- {company}: {count} projects")
    else:
        st.info("📊 No analytics available yet. Save some projects to see insights!")

if __name__ == "__main__":
    main() 