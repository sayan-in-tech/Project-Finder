COMPANY_PROFILE_PROMPT = """
Analyze the company "{company_name}" and provide a comprehensive profile in JSON format.

Include the following information:
1. Industry classification
2. Company size estimation
3. Business focus and main products/services
4. Technology stack they likely use
5. Recent highlights or news
6. Engineering challenges they face

Return the response as a valid JSON object with this structure:
{{
    "name": "{company_name}",
    "industry": "technology|finance|healthcare|ecommerce|education|entertainment|transportation|real_estate|manufacturing|consulting|other",
    "size": "startup|scaleup|enterprise|unknown",
    "description": "Comprehensive company description (200-300 words)",
    "business_focus": "Main business focus and products/services",
    "tech_stack": {{
        "frontend": ["React", "Vue.js", "Angular"],
        "backend": ["Python", "Java", "Node.js"],
        "database": ["PostgreSQL", "MongoDB", "Redis"],
        "cloud": ["AWS", "GCP", "Azure"],
        "devops": ["Docker", "Kubernetes", "Jenkins"],
        "ai_ml": ["TensorFlow", "PyTorch", "scikit-learn"],
        "mobile": ["React Native", "Flutter", "iOS"],
        "other": ["Other technologies"]
    }},
    "recent_highlights": [
        "Recent company news or achievements",
        "Product launches or updates",
        "Strategic initiatives"
    ]
}}

Focus on accuracy and relevance for job seekers. If information is not available, use reasonable estimates based on the company's industry and known characteristics.
"""

# ---------------------------------------------------------------------------------------

ENGINEERING_CHALLENGES_PROMPT = """
Based on the company profile for {company_name}, identify exactly 3 common engineering challenges they likely face.

Company Profile:
{company_profile}

Generate challenges that are:
1. Technically relevant for software engineers
2. Specific to the company's industry and business model
3. Realistic and achievable for side projects
4. Different from each other (cover different aspects)

Return as a JSON array:
[
    {{
        "id": "scalability_performance",
        "title": "Scalability & Performance Optimization",
        "description": "Detailed description of the challenge (2-3 sentences)",
        "difficulty": "beginner|intermediate|advanced",
        "relevance_score": 0.85,
        "tech_areas": ["frontend", "backend", "ai_ml"]
    }},
    {{
        "id": "data_analytics_ml", 
        "title": "Data Analytics & Machine Learning",
        "description": "Detailed description of the challenge (2-3 sentences)",
        "difficulty": "beginner|intermediate|advanced",
        "relevance_score": 0.80,
        "tech_areas": ["database", "cloud", "devops"]
    }},
    {{
        "id": "user_experience_mobile",
        "title": "User Experience & Mobile Development", 
        "description": "Detailed description of the challenge (2-3 sentences)",
        "difficulty": "beginner|intermediate|advanced",
        "relevance_score": 0.75,
        "tech_areas": ["mobile", "ai_ml", "frontend"]
    }}
]

Focus on challenges that would be impressive to demonstrate in a job interview. Use specific, descriptive titles that reflect the actual challenge area.
""" 

# ---------------------------------------------------------------------------------------

PROJECT_GENERATION_PROMPT = """
Generate exactly {ideas_per_challenge} concrete side project ideas for the company "{company_name}" based on this engineering challenge:

Challenge: {challenge}

Company Profile:
{company_profile}

User Skills: {user_skills}

Requirements for each project:
1. Must be realistic and achievable as a side project
2. Should demonstrate relevant technical skills
3. Should be impressive in a job interview
4. Should address the specific challenge
5. Should use modern, relevant technologies

For each project, provide:
- Title: Catchy, descriptive project name
- Description: Clear explanation of what the project does (2-3 sentences)
- Tech Stack: Specific technologies to use (comma-separated)
- Demo Hook: What to demonstrate in an interview that would impress
- Difficulty: beginner|intermediate|advanced
- Estimated Duration: 2-4 weeks|1-2 months|3-6 months

Return as a JSON array:
[
    {{
        "title": "Project Title",
        "description": "Clear description of what the project does and how it solves the challenge",
        "tech_stack": "Technology1, Technology2, Technology3",
        "demo_hook": "Specific demonstration that would impress in an interview",
        "difficulty": "beginner|intermediate|advanced",
        "estimated_duration": "2-4 weeks|1-2 months|3-6 months"
    }}
]

Focus on projects that:
- Show technical depth and problem-solving skills
- Are relevant to the company's industry and challenges
- Can be built incrementally with clear milestones
- Demonstrate both technical and business understanding
"""

# ---------------------------------------------------------------------------------------

PROJECT_REFINEMENT_PROMPT = """
Refine this project idea to make it more impressive and relevant for {company_name}:

Original Project: {project_title}
Description: {project_description}
Tech Stack: {tech_stack}

Company Context: {company_profile}
Challenge: {challenge}

Improve the project by:
1. Making it more specific to the company's industry
2. Adding advanced technical features
3. Improving the demo hook to be more impressive
4. Ensuring it addresses the engineering challenge directly
5. Making it more scalable and production-ready

Return the improved project as JSON:
{{
    "title": "Improved Project Title",
    "description": "Enhanced description with more technical depth",
    "tech_stack": "Enhanced tech stack with specific versions/frameworks",
    "demo_hook": "More impressive demonstration strategy",
    "difficulty": "beginner|intermediate|advanced",
    "estimated_duration": "2-4 weeks|1-2 months|3-6 months"
}}
""" 