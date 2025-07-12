"""
Centralized prompt templates for AI services
"""

# Company Analysis Prompt
COMPANY_ANALYSIS_PROMPT = """
Analyze the company "{company_name}" and provide the following information in JSON format:
{{
    "name": "Company name",
    "industry": "technology/finance/healthcare/ecommerce/education/entertainment/transportation/real_estate/manufacturing/consulting/other",
    "size": "startup/scaleup/enterprise/unknown",
    "description": "Brief company description",
    "business_focus": "Main business focus and primary revenue stream",
    "tech_stack": {{
        "backend": ["tech1", "tech2"],
        "frontend": ["tech1", "tech2"],
        "database": ["db1", "db2"],
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

Important: 
- Use lowercase for industry (e.g., "technology" not "Technology") and use the exact size values listed above.
- Return ONLY the JSON object, no markdown formatting, no code blocks, no additional text.
- Focus on real engineering challenges that this company might face.
"""

# Project Generation Prompt
PROJECT_GENERATION_PROMPT = """
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
        "demo_hook": "What to demonstrate in interview",
        "challenge_id": "challenge_1",
        "challenge_title": "Original challenge title"
    }}
]

Important: Return ONLY the JSON array, no markdown formatting, no code blocks, no additional text.
Make projects practical and achievable.
"""

# Project Refinement Prompt
PROJECT_REFINEMENT_PROMPT = """
Refine this project idea for {company_name}:

Current project: {project_title}
Description: {project_description}

Challenge context: {challenge_title} - {challenge_description}

Provide an improved version with:
- More detailed technical implementation
- Specific technologies to use
- Step-by-step development plan
- Success metrics

Return as JSON with the same structure as the original project.
Important: Return ONLY the JSON object, no markdown formatting, no code blocks, no additional text.
""" 