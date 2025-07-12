# 🚀 Project Finder

> **AI-Powered Project Discovery & Generation Platform**  
> *Transform your portfolio with personalized project ideas based on real company challenges*

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Project%20Finder-blue?style=for-the-badge&logo=rocket)](https://project-finder-dznt.onrender.com/)
[![GitHub](https://img.shields.io/badge/GitHub-Project%20Finder-black?style=for-the-badge&logo=github)](https://github.com/sayan-in-tech/Project-Finder)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Gemini AI](https://img.shields.io/badge/Gemini%20AI-2.5%20Flash%20Lite-orange?style=for-the-badge&logo=google)](https://ai.google.dev/)

---

## ✨ What is Project Finder?

Project Finder is an intelligent platform that generates personalized project ideas based on real engineering challenges from top tech companies. Perfect for developers looking to build impressive portfolios and prepare for technical interviews.

### 🎯 **Key Features**

- 🤖 **AI-Powered Analysis** - Uses Google's Gemini 2.5 Flash Lite for intelligent company analysis
- 🌐 **Smart Web Scraping** - Automatically analyzes company websites for deeper insights
- 💡 **Personalized Projects** - Generates projects tailored to your skills and experience level
- 📊 **Token Usage Preview** - Shows exactly how many tokens will be used before generating ideas
- 🎨 **Modern UI/UX** - Beautiful, responsive interface built with Bootstrap 5
- ⚡ **Fast & Efficient** - Optimized for speed with smart content truncation
- 🔒 **Secure** - Your API keys are stored locally and never shared

---

## 🚀 Live Demo

**Experience Project Finder in action:**  
👉 **[https://project-finder-dznt.onrender.com/](https://project-finder-dznt.onrender.com/)**

---

## 🛠️ Tech Stack

### **Backend**
- **FastAPI** - Modern, fast web framework for building APIs
- **Python 3.8+** - Core programming language
- **Google Gemini AI** - Advanced AI for intelligent analysis
- **Selenium** - Web scraping for company website analysis
- **BeautifulSoup4** - HTML parsing and content extraction
- **spaCy** - Natural language processing for text summarization

### **Frontend**
- **Bootstrap 5** - Modern, responsive CSS framework
- **JavaScript (ES6+)** - Interactive client-side functionality
- **Font Awesome** - Beautiful icons and UI elements
- **Google Fonts** - Typography optimization

### **Infrastructure**
- **Render** - Cloud hosting and deployment
- **Uvicorn** - ASGI server for FastAPI
- **Pydantic** - Data validation and settings management

---

## 🎯 How It Works

### 1. **Company Analysis**
- Enter a target company name (e.g., "Google", "Netflix", "OpenAI")
- Optionally provide the company website URL for deeper analysis
- Add additional context or information about the company

### 2. **AI-Powered Processing**
- Our AI analyzes the company's business model, tech stack, and challenges
- Web scraping extracts relevant information from company websites
- Smart content truncation optimizes token usage and costs

### 3. **Personalized Project Generation**
- AI generates project ideas based on real engineering challenges
- Projects are tailored to your specified skills and experience level
- Each project includes detailed implementation guidance

### 4. **Token Usage Transparency**
- Preview exactly how many tokens will be used before generation
- Smart warnings for high token usage
- Cost-effective processing with intelligent content optimization

---

## 🚀 Quick Start

### **Prerequisites**
- Python 3.8 or higher
- Google Gemini API key ([Get one here](https://aistudio.google.com/app/apikey))

### **Installation**

1. **Clone the repository**
   ```bash
   git clone https://github.com/sayan-in-tech/Project-Finder.git
   cd Project-Finder
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:8000`

### **Environment Setup**

Create a `.env` file in the root directory:
```env
# API Configuration
API_V1_STR=/api/v1
PROJECT_NAME=Project Finder
PROJECT_DESCRIPTION=AI-Powered Project Discovery Platform
VERSION=1.0.0

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True

# CORS Settings
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000"]
```

---

## 📖 API Documentation

### **Interactive API Docs**
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### **Key Endpoints**

#### **Company Analysis**
```http
POST /api/v1/companies/analyze-company
```
Analyze a company and generate project ideas.

#### **Token Preview**
```http
POST /api/v1/companies/preview-tokens
```
Preview token usage before generating ideas.

#### **Project Generation**
```http
POST /api/v1/projects/generate-projects
```
Generate project ideas based on company challenges.

---

## 🏗️ Project Structure

```
Project-Finder/
├── app/
│   ├── api/                    # API routes
│   │   ├── companies.py        # Company analysis endpoints
│   │   └── projects.py         # Project generation endpoints
│   ├── core/                   # Core configuration
│   │   ├── config.py           # Settings management
│   │   └── deps.py             # Dependencies
│   ├── models/                 # Data models
│   │   └── schemas.py          # Pydantic schemas
│   ├── services/               # Business logic
│   │   ├── company_service.py  # Company analysis service
│   │   ├── gemini_service.py   # AI integration
│   │   ├── project_service.py  # Project generation service
│   │   ├── website_parser.py   # Web scraping service
│   │   └── prompts/            # AI prompt management
│   │       ├── prompts.py      # Centralized prompts
│   │       └── __init__.py     # Module exports
│   ├── static/                 # Static assets
│   │   ├── css/
│   │   └── js/
│   ├── templates/              # HTML templates
│   │   └── index.html          # Main application page
│   └── main.py                 # FastAPI application
├── main.py                     # Application entry point
├── requirements.txt             # Python dependencies
└── README.md                   # This file
```

---

## 🎨 Features in Detail

### **🤖 Intelligent AI Analysis**
- **Company Profiling**: Analyzes business model, industry, and tech stack
- **Challenge Identification**: Identifies real engineering challenges
- **Smart Summarization**: Efficient content processing with NLP

### **🌐 Advanced Web Scraping**
- **Multi-page Crawling**: Analyzes multiple pages for comprehensive insights
- **Content Extraction**: Focuses on main content areas
- **Smart Filtering**: Removes boilerplate and irrelevant content

### **💡 Personalized Project Generation**
- **Skill-based Matching**: Tailors projects to your technical skills
- **Difficulty Levels**: Beginner, intermediate, and advanced projects
- **Implementation Guidance**: Detailed technical specifications

### **📊 Token Usage Optimization**
- **Preview System**: See token count before generation
- **Smart Truncation**: Optimizes content for cost efficiency
- **Usage Warnings**: Alerts for high token consumption

---

## 🔧 Configuration

### **API Key Setup**
1. Get your Google Gemini API key from [AI Studio](https://aistudio.google.com/app/apikey)
2. Enter the API key in the web interface
3. Your key is stored locally and never shared

### **Customization Options**
- **Project Count**: Generate 2-12 project ideas
- **Skill Specification**: Add your technical skills for personalized results
- **Additional Context**: Provide extra company information for better analysis

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### **Development Setup**
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Test thoroughly
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

### **Guidelines**
- Follow PEP 8 Python style guidelines
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Google Gemini AI** for providing the powerful AI capabilities
- **FastAPI** team for the excellent web framework
- **Bootstrap** for the beautiful UI components
- **Open Source Community** for inspiration and support

---

## 📞 Support & Contact

- **Author**: [Sayan Ghosh](https://github.com/sayan-in-tech)
- **Live Demo**: [https://project-finder-dznt.onrender.com/](https://project-finder-dznt.onrender.com/)
- **GitHub**: [https://github.com/sayan-in-tech/Project-Finder](https://github.com/sayan-in-tech/Project-Finder)

---

**Made with ❤️ by [Sayan Ghosh](https://github.com/sayan-in-tech)**

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/sayan-in-tech)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/sayan-in-tech)
[![Twitter](https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/sayan_in_tech)

</div> 