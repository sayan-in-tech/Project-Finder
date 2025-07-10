# Project Finder - Modular Architecture

An AI-powered side project generator that helps users discover custom side projects for target companies using Google's Gemini API to showcase relevant skills and win interviews.

## 🏗️ Architecture Overview

This project has been refactored into a clean, modular architecture with clear separation of concerns:

### Frontend (Streamlit)
- **Location**: `frontend/streamlit_app.py`
- **Purpose**: Pure UI layer with no business logic
- **Features**: Modern, responsive interface that communicates with backend via REST API
- **Dependencies**: Only UI-related libraries (Streamlit, requests)

### Backend (Flask API)
- **Location**: `backend/`
- **Purpose**: All business logic and AI processing
- **Structure**:
  - `models/`: Pydantic models for data validation
  - `services/`: Business logic services
  - `prompts/`: AI prompts management
  - `routes/`: API endpoints
  - `server.py`: Flask server

### Key Benefits
1. **Separation of Concerns**: Frontend and backend are completely independent
2. **Scalability**: Easy to add new features or change AI providers
3. **Maintainability**: Clear structure makes code easy to understand and modify
4. **Reusability**: Backend API can be used by other frontends (web, mobile, etc.)

## 📁 Project Structure

```
Project-Finder/
├── frontend/
│   └── streamlit_app.py          # Pure UI layer
├── backend/
│   ├── models/
│   │   └── models.py             # Pydantic data models
│   ├── services/
│   │   ├── company_analysis_service.py    # Company analysis logic
│   │   └── project_generation_service.py  # Project generation logic
│   ├── prompts/
│   │   ├── company_analysis.py   # Company analysis prompts
│   │   └── project_generation.py # Project generation prompts
│   ├── routes/
│   │   └── api_routes.py         # Flask API endpoints
│   └── server.py                 # Flask server
├── run_app.py                    # Unified launcher script
├── requirements.txt              # Updated dependencies
└── README.md                    # Comprehensive documentation
```

## 🚀 Getting Started

### Prerequisites
1. Python 3.8+
2. Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Project-Finder
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**
   ```bash
   export GEMINI_API_KEY=your_api_key_here
   ```

### Running the Application

#### Single Command Launch (Recommended)

```bash
python run_app.py
```

This will:
1. Start the backend API server on `http://localhost:5000`
2. Wait for the backend to be ready
3. Start the frontend on `http://localhost:8501`
4. Open your browser automatically

#### Alternative: Manual Launch

If you prefer to run components separately:

1. **Start the backend server**
   ```bash
   python -m backend.server
   ```
   The API will be available at `http://localhost:5000`

2. **Start the frontend** (in a new terminal)
   ```bash
   streamlit run frontend/streamlit_app.py
   ```
   The UI will be available at `http://localhost:8501`

## 🔧 API Endpoints

The backend provides the following REST API endpoints:

- `POST /api/analyze-company` - Analyze a company and generate projects
- `GET /api/company-profile/<company_name>` - Get company profile only
- `GET /api/engineering-challenges/<company_name>` - Get engineering challenges
- `POST /api/generate-projects` - Generate projects for specific challenges
- `POST /api/refine-project` - Refine an existing project idea
- `GET /health` - Health check endpoint

## 🏢 Company Analysis Layer

The system now separates company data collection from idea generation:

### 1. Company Analysis Service
- **Purpose**: Analyzes companies and extracts comprehensive profiles
- **Features**:
  - Industry classification
  - Company size estimation
  - Technology stack analysis
  - Recent highlights and business focus
  - Engineering challenges identification

### 2. Project Generation Service
- **Purpose**: Generates project ideas based on analyzed company data
- **Features**:
  - Tailored project suggestions
  - Difficulty and duration estimation
  - Demo hook generation
  - Technology stack recommendations

## 📊 Data Models

The system uses comprehensive Pydantic models for data validation:

- `CompanyProfile`: Complete company information
- `EngineeringChallenge`: Technical challenges the company faces
- `ProjectIdea`: Generated project suggestions
- `TechStack`: Categorized technology information

## 🎯 Key Features

### Single Company Focus
- Analyze one company at a time for deeper insights
- More detailed company profiles
- Better project relevance

### Modular Prompt Management
- All AI prompts are stored in `backend/prompts/`
- Easy to modify and improve prompts
- Version control for prompt changes

### Comprehensive Company Classification
- Industry type classification
- Company size estimation
- Technology stack categorization
- Business focus analysis

## 🔄 Development Workflow

### Adding New Features

1. **Backend Changes**:
   - Add new models in `backend/models/`
   - Create new services in `backend/services/`
   - Add prompts in `backend/prompts/`
   - Create API routes in `backend/routes/`

2. **Frontend Changes**:
   - Modify `frontend/streamlit_app.py`
   - Update UI components
   - Add new API calls

### Modifying AI Prompts

1. Edit prompts in `backend/prompts/`
2. Test with the API endpoints
3. Deploy changes

### Adding New Services

1. Create new service class in `backend/services/`
2. Add corresponding API routes
3. Update frontend to use new endpoints

## 🧪 Testing

### Backend Testing
```bash
# Test API endpoints
curl http://localhost:5000/health
curl -X POST http://localhost:5000/api/analyze-company \
  -H "Content-Type: application/json" \
  -d '{"company_name": "Google"}'
```

### Frontend Testing
1. Start the backend server
2. Run the frontend
3. Test the UI functionality

## 🚀 Deployment

### Backend Deployment
- Deploy Flask app to your preferred platform (Heroku, AWS, etc.)
- Set environment variables for API keys
- Configure CORS if needed

### Frontend Deployment
- Deploy Streamlit app to Streamlit Cloud or similar
- Update API base URL in frontend code
- Configure environment variables

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

If you encounter any issues:
1. Check the API health endpoint
2. Verify your API key is correct
3. Check the logs for error messages
4. Open an issue on GitHub

---

**Happy coding! 🚀** 