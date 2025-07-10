# Example usage of the Project Finder app
# This script demonstrates how to use the Gemini service directly

import os
import sys
sys.path.append('.')

from app import GeminiService
import json

def main():
    # Get API key from environment or user input
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        api_key = input("Enter your Gemini API key: ")
    
    if not api_key:
        print("API key is required!")
        return
    
    # Initialize service
    gemini = GeminiService(api_key)
    
    # Example company
    company = "OpenAI"
    
    print(f"Analyzing {company}...")
    
    # Step 1: Get company profile
    print("\n1. Getting company profile...")
    profile = gemini.get_company_profile(company)
    print(f"Profile: {profile[:200]}...")
    
    # Step 2: Get challenges
    print("\n2. Identifying challenges...")
    challenges = gemini.get_engineering_challenges(company, profile)
    print("Challenges:")
    for i, challenge in enumerate(challenges, 1):
        print(f"  {i}. {challenge}")
    
    # Step 3: Generate project ideas
    print("\n3. Generating project ideas...")
    projects = gemini.generate_project_ideas(company, challenges)
    
    print(f"\nGenerated {len(projects)} project ideas:")
    for i, project in enumerate(projects, 1):
        print(f"\n--- Project {i} ---")
        print(f"Title: {project.get('title', 'N/A')}")
        print(f"Description: {project.get('description', 'N/A')}")
        print(f"Tech Stack: {project.get('tech_stack', 'N/A')}")
        print(f"Demo Hook: {project.get('demo_hook', 'N/A')}")
    
    # Save to file
    with open(f"{company.lower()}_projects.json", 'w') as f:
        json.dump(projects, f, indent=2)
    
    print(f"\nResults saved to {company.lower()}_projects.json")

if __name__ == "__main__":
    main()
