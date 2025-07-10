"""
Prompts for company analysis and profiling
"""

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
        "id": "challenge_1",
        "title": "Challenge Title",
        "description": "Detailed description of the challenge (2-3 sentences)",
        "difficulty": "beginner|intermediate|advanced",
        "relevance_score": 0.85,
        "tech_areas": ["frontend", "backend", "ai_ml"]
    }},
    {{
        "id": "challenge_2", 
        "title": "Challenge Title",
        "description": "Detailed description of the challenge (2-3 sentences)",
        "difficulty": "beginner|intermediate|advanced",
        "relevance_score": 0.80,
        "tech_areas": ["database", "cloud", "devops"]
    }},
    {{
        "id": "challenge_3",
        "title": "Challenge Title", 
        "description": "Detailed description of the challenge (2-3 sentences)",
        "difficulty": "beginner|intermediate|advanced",
        "relevance_score": 0.75,
        "tech_areas": ["mobile", "ai_ml", "frontend"]
    }}
]

Focus on challenges that would be impressive to demonstrate in a job interview.
""" 