# Prompts Module

This module centralizes all AI prompts used throughout the application for better maintainability and consistency.

## Structure

```
prompts/
├── __init__.py      # Module exports
├── prompts.py       # Centralized prompt templates
└── README.md        # This documentation
```

## Available Prompts

### 1. COMPANY_ANALYSIS_PROMPT
- **Purpose**: Analyzes a company and returns a structured profile
- **Parameters**: `company_name`
- **Returns**: JSON with company information including industry, size, tech stack, and engineering challenges

### 2. PROJECT_GENERATION_PROMPT
- **Purpose**: Generates project ideas based on company challenges
- **Parameters**: `total_ideas`, `company_name`, `challenges_text`, `skills_text`
- **Returns**: JSON array of project ideas

### 3. PROJECT_REFINEMENT_PROMPT
- **Purpose**: Refines existing project ideas with additional context
- **Parameters**: `company_name`, `project_title`, `project_description`, `challenge_title`, `challenge_description`
- **Returns**: JSON with refined project details

## Usage

```python
from app.services.prompts import (
    COMPANY_ANALYSIS_PROMPT,
    PROJECT_GENERATION_PROMPT,
    PROJECT_REFINEMENT_PROMPT
)

# Use in your service
prompt = COMPANY_ANALYSIS_PROMPT.format(company_name="Google")
```

## Adding New Prompts

1. Add the prompt template to `prompts.py`
2. Export it in `__init__.py`
3. Import and use it in your service

Example:
```python
# In prompts.py
NEW_PROMPT = """
Your prompt template here with {parameter} placeholders.
"""

# In __init__.py
from .prompts import NEW_PROMPT
__all__ = [..., 'NEW_PROMPT']

# In your service
from .prompts import NEW_PROMPT
prompt = NEW_PROMPT.format(parameter="value")
```

## Benefits

- **Centralized Management**: All prompts in one place
- **Easy Maintenance**: Update prompts without touching service logic
- **Consistency**: Standardized prompt formatting across the application
- **Reusability**: Prompts can be shared between different services
- **Version Control**: Track prompt changes separately from business logic 