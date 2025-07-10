# 🚀 Project Finder

**Discover custom side-projects for target companies to showcase relevant skills and win interviews.**

A comprehensive web application that uses AI to analyze companies and generate personalized project ideas that demonstrate relevant technical skills for job interviews.

## ✨ Features

- **🤖 AI-Powered Analysis**: Uses Google Gemini AI to analyze companies and generate insights
- **🎯 Targeted Projects**: Creates project ideas specifically tailored to each company's tech stack and challenges
- **💾 Save & Share**: Save your workspace and share project ideas with others
- **📊 Analytics**: Track your project generation and company analysis history
- **⚡ Fast & Responsive**: Modern UI with real-time updates and caching
- **🔧 Comprehensive Error Handling**: Detailed logging and error reporting for easy debugging

## 🚀 Quick Start

### One Command Setup

The easiest way to run the project:

```bash
python run.py
```

This single command will:
- ✅ Check all dependencies
- ✅ Set up environment variables
- ✅ Start both backend and frontend servers
- ✅ Provide detailed error reporting
- ✅ Monitor processes and handle crashes

### Manual Setup

If you prefer manual setup:

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment:**
   ```bash
   cp env.example .env
   # Edit .env and add your Gemini API key
   ```

3. **Run the application:**
   ```bash
   python start.py
   ```

## 🔧 Configuration

### Required Environment Variables

Create a `.env` file in the project root:

```env
# Required: Your Gemini API key
GEMINI_API_KEY=your_api_key_here

# Optional: Database URL (defaults to SQLite)
DATABASE_URL=sqlite:///./database/project_finder.db

# Optional: Redis URL for caching (defaults to in-memory)
REDIS_URL=redis://localhost:6379

# Optional: Debug mode
DEBUG=True

# Optional: Log level
LOG_LEVEL=INFO
```

### Getting Your Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file

## 📁 Project Structure

```
Project-Finder/
├── backend/                 # FastAPI backend
│   ├── api/                # API endpoints
│   ├── core/               # Core configuration
│   ├── models/             # Database models
│   ├── services/           # Business logic
│   └── utils/              # Utilities
├── frontend/               # Streamlit frontend
│   └── app.py             # Main frontend application
├── database/               # SQLite database files
├── logs/                   # Application logs
├── tests/                  # Test suite
├── start.py               # Enhanced startup script
├── run.py                 # One-command runner
└── requirements.txt       # Python dependencies
```

## 🛠️ Development

### Running Individual Components

**Backend only:**
```bash
cd backend
python main.py
```

**Frontend only:**
```bash
cd frontend
streamlit run app.py
```

### Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_api.py

# Run with coverage
pytest --cov=backend
```

### Logging

The application uses structured logging with detailed error reporting:

- **Log files**: `logs/` directory
- **Error tracking**: Detailed error context with file and function names
- **Performance monitoring**: Request latency and cache statistics

## 🔍 Error Handling & Debugging

The application includes comprehensive error handling:

### Startup Checks
- ✅ Python version compatibility
- ✅ Dependency verification
- ✅ Project structure validation
- ✅ Environment configuration
- ✅ Port availability
- ✅ Database connection
- ✅ AI service initialization

### Runtime Monitoring
- 🔄 Process health monitoring
- 📊 Performance metrics
- 🚨 Automatic error recovery
- 📝 Detailed error logging

### Debugging Tips

1. **Check logs**: Look in `logs/` directory for detailed error information
2. **Verify API key**: Ensure your Gemini API key is correctly set
3. **Check ports**: Make sure ports 8000 and 8501 are available
4. **Database issues**: Check database permissions and connection strings

## 🚀 Deployment

### Local Development
```bash
python run.py
```

### Production Deployment
See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

## 📊 API Endpoints

- `GET /api/v1/profile?company={name}` - Get company profile
- `GET /api/v1/challenges?company={name}` - Get engineering challenges
- `GET /api/v1/ideas?company={name}` - Get project ideas
- `GET /api/v1/health` - Health check
- `GET /api/v1/metrics` - Performance metrics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues:

1. Check the logs in `logs/` directory
2. Verify your environment configuration
3. Ensure all dependencies are installed
4. Check the API documentation at `http://localhost:8000/docs`

---

**Made with ❤️ for developers looking to showcase their skills!** 