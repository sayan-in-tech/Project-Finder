"""
Prompts for project idea generation
"""

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