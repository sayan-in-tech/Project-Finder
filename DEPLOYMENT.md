# Project Finder - Deployment Guide

This guide covers various deployment options for the Project Finder application.

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Google Cloud account with Gemini API access
- Git

### 1. Local Development Setup

```bash
# Clone the repository
git clone <repository-url>
cd Project-Finder

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your Gemini API key
```

### 2. Environment Configuration

Create a `.env` file in the root directory:

```env
# Required - Get from https://makersuite.google.com/app/apikey
GEMINI_API_KEY=your_gemini_api_key_here

# Optional - Uses SQLite by default
DATABASE_URL=sqlite:///./database/project_finder.db
```

### 3. Run the Application

#### Option A: Development Mode (Recommended for development)

```bash
# Terminal 1: Start the backend
cd backend
uvicorn main:app --reload --port 8000

# Terminal 2: Start the frontend
cd frontend
streamlit run app.py --server.port 8501
```

#### Option B: Production Deployment

```bash
# Deploy to cloud platform of your choice
# See sections below for detailed instructions
```

## 🚀 Local Production Setup

### Single Process Deployment

```bash
# Install production dependencies
pip install gunicorn

# Start backend with gunicorn
cd backend
gunicorn main:app --workers 4 --bind 0.0.0.0:8000

# Start frontend with streamlit
cd frontend
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

### Process Management with PM2

```bash
# Install PM2
npm install -g pm2

# Create ecosystem.config.js
# Start with PM2
pm2 start ecosystem.config.js
```

### Systemd Service (Linux)

```bash
# Create systemd service files
# Enable and start services
sudo systemctl enable project-finder-backend
sudo systemctl enable project-finder-frontend
```

## ☁️ Cloud Deployment

### Render Deployment

1. **Fork the repository** to your GitHub account

2. **Create a new Web Service** on Render:
   - Connect your GitHub repository
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`

3. **Configure environment variables**:
   - `GEMINI_API_KEY`: Your Google Gemini API key
   - `DATABASE_URL`: PostgreSQL connection string (provided by Render)
   - `LOG_LEVEL`: INFO
   - `DEBUG`: false

4. **Deploy** and wait for the build to complete

### Heroku Deployment

1. **Install Heroku CLI** and login

2. **Create Heroku app**:
```bash
heroku create your-project-finder-app
```

3. **Set environment variables**:
```bash
heroku config:set GEMINI_API_KEY=your_api_key
heroku config:set DATABASE_URL=your_postgresql_url
```

4. **Deploy**:
```bash
git push heroku main
```

### Railway Deployment

1. **Connect your GitHub repository** to Railway

2. **Configure environment variables** in Railway dashboard:
   - `GEMINI_API_KEY`
   - `DATABASE_URL`
   - `LOG_LEVEL`

3. **Deploy** automatically on push to main branch

## 🔧 Production Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `GEMINI_API_KEY` | Google Gemini API key | **Yes** | - |
| `DATABASE_URL` | Database connection string | No | SQLite |

**All other settings use sensible defaults for development.**

### Database Configuration

#### SQLite (Default - No setup required)
```env
DATABASE_URL=sqlite:///./database/project_finder.db
```

#### PostgreSQL (Production)
```env
DATABASE_URL=postgresql://user:password@host:port/database
```

#### MySQL (Production)
```env
DATABASE_URL=mysql://user:password@host:port/database
```

## 🔒 Security Considerations

### API Key Management

1. **Never commit API keys** to version control
2. **Use environment variables** for all sensitive data
3. **Rotate API keys** regularly
4. **Use different keys** for development and production

### Database Security

1. **Use strong passwords** for database connections
2. **Enable SSL** for database connections in production
3. **Restrict database access** to application servers only
4. **Regular backups** of production data

### Application Security

1. **Enable HTTPS** in production
2. **Set secure SECRET_KEY** in production
3. **Disable DEBUG mode** in production
4. **Implement rate limiting** for API endpoints
5. **Use CORS properly** for frontend-backend communication

## 📊 Monitoring and Logging

### Health Checks

The application provides health check endpoints:

- **Backend**: `GET /health`
- **Frontend**: Built-in Streamlit health check

### Logging

Logs are written to:
- **Console**: Structured JSON logs
- **File**: `logs/app.log` (if configured)

### Metrics

Prometheus metrics are available at:
- **Backend**: `GET /metrics`

## 🔧 Troubleshooting

### Common Issues

#### 1. API Connection Errors
```bash
# Check if backend is running
curl http://localhost:8000/health

# Check logs
tail -f logs/app.log
```

#### 2. Database Connection Issues
```bash
# Check database file permissions
ls -la database/

# Recreate database
rm database/project_finder.db
# Restart application
```

#### 3. Gemini API Errors
```bash
# Verify API key
echo $GEMINI_API_KEY

# Test API key
curl -H "Authorization: Bearer $GEMINI_API_KEY" \
  https://generativelanguage.googleapis.com/v1beta/models
```

#### 4. Port Conflicts
```bash
# Check what's using the ports
lsof -i :8000
lsof -i :8501

# Change ports in configuration if needed
```

### Performance Optimization

1. **Enable Redis caching** for better performance
2. **Use production database** (PostgreSQL/MySQL)
3. **Optimize application** with production settings
4. **Implement CDN** for static assets
5. **Use load balancer** for high traffic

## 🚀 Scaling

### Horizontal Scaling

1. **Multiple backend instances** behind load balancer
2. **Shared database** (PostgreSQL/MySQL)
3. **Redis cluster** for session management
4. **CDN** for static content

### Vertical Scaling

1. **Increase server resources** (CPU, RAM)
2. **Optimize database queries**
3. **Implement connection pooling**
4. **Use async processing** for heavy tasks

## 📝 Maintenance

### Regular Tasks

1. **Update dependencies** monthly
2. **Monitor API usage** and costs
3. **Backup database** daily
4. **Check logs** for errors
5. **Update SSL certificates** before expiry

### Backup Strategy

```bash
# Database backup
sqlite3 database/project_finder.db ".backup backup.db"

# PostgreSQL backup
pg_dump $DATABASE_URL > backup.sql

# File backup
tar -czf backup.tar.gz database/ logs/
```

## 🆘 Support

For deployment issues:

1. **Check logs**: `tail -f logs/app.log`
2. **Verify environment**: `echo $GEMINI_API_KEY`
3. **Test endpoints**: `curl http://localhost:8000/health`
4. **Check documentation**: README.md
5. **Create issue**: GitHub repository

## 📚 Additional Resources

- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Streamlit Deployment](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app)
- [Python Deployment Best Practices](https://docs.python.org/3/library/venv.html)
- [Google Gemini API](https://ai.google.dev/docs) 