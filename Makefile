# Project Finder Makefile
# Common development and deployment tasks

.PHONY: help install test run clean docker-build docker-run docker-stop lint format

# Default target
help:
	@echo "Project Finder - Available Commands:"
	@echo ""
	@echo "Development:"
	@echo "  install     Install dependencies"
	@echo "  test        Run tests with coverage"
	@echo "  run         Run the application locally"
	@echo "  run-backend Run only the backend"
	@echo "  run-frontend Run only the frontend"
	@echo ""
	@echo "Deployment:"
	@echo "  deploy-render Deploy to Render"
	@echo "  deploy-heroku Deploy to Heroku"
	@echo "  deploy-railway Deploy to Railway"
	@echo ""
	@echo "Code Quality:"
	@echo "  lint        Run linting checks"
	@echo "  format      Format code with black and isort"
	@echo ""
	@echo "Maintenance:"
	@echo "  clean       Clean up generated files"
	@echo "  db-migrate  Run database migrations"
	@echo "  db-reset    Reset database"

# Development
install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt

test:
	@echo "Running tests..."
	pytest

test-unit:
	@echo "Running unit tests..."
	pytest tests/ -m unit

test-integration:
	@echo "Running integration tests..."
	pytest tests/ -m integration

test-api:
	@echo "Running API tests..."
	pytest tests/test_api.py -v

run:
	@echo "Starting Project Finder..."
	@echo "Backend: http://localhost:8000"
	@echo "Frontend: http://localhost:8501"
	@echo "API Docs: http://localhost:8000/docs"
	@echo ""
	@echo "Starting both services..."
	@python start.py

run-backend:
	@echo "Starting backend only..."
	cd backend && uvicorn main:app --reload --port 8000

run-frontend:
	@echo "Starting frontend only..."
	cd frontend && streamlit run app.py --server.port 8501

# Cloud Deployment
deploy-render:
	@echo "Deploying to Render..."
	@echo "1. Fork repository to GitHub"
	@echo "2. Connect to Render"
	@echo "3. Set build command: pip install -r requirements.txt"
	@echo "4. Set start command: uvicorn backend.main:app --host 0.0.0.0 --port \$PORT"

deploy-heroku:
	@echo "Deploying to Heroku..."
	@echo "1. Install Heroku CLI"
	@echo "2. Run: heroku create your-app-name"
	@echo "3. Run: git push heroku main"

deploy-railway:
	@echo "Deploying to Railway..."
	@echo "1. Connect GitHub repository to Railway"
	@echo "2. Configure environment variables"
	@echo "3. Deploy automatically"

# Code Quality
lint:
	@echo "Running linting checks..."
	flake8 backend/ frontend/ tests/
	mypy backend/ frontend/

format:
	@echo "Formatting code..."
	black backend/ frontend/ tests/
	isort backend/ frontend/ tests/

# Maintenance
clean:
	@echo "Cleaning up..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf database/*.db
	rm -rf logs/*.log

db-migrate:
	@echo "Running database migrations..."
	cd backend && alembic upgrade head

db-reset:
	@echo "Resetting database..."
	rm -f database/project_finder.db
	@echo "Database reset complete"

# Environment
setup-env:
	@echo "Setting up environment..."
	cp env.example .env
	@echo "Please edit .env with your Gemini API key"

# Production
deploy:
	@echo "Deploying to production..."
	@echo "Choose deployment platform:"
	@echo "  make deploy-render"
	@echo "  make deploy-heroku"
	@echo "  make deploy-railway"

# Monitoring
logs:
	@echo "Showing application logs..."
	tail -f logs/app.log

health:
	@echo "Checking application health..."
	curl -f http://localhost:8000/health || echo "Backend not responding"
	curl -f http://localhost:8501 || echo "Frontend not responding"

# Development helpers
dev-setup: setup-env install
	@echo "Development setup complete!"
	@echo "Next steps:"
	@echo "1. Edit .env with your Gemini API key"
	@echo "2. Run 'make run' to start the application"
	@echo "3. Visit http://localhost:8501"

# Quick start
quick-start: dev-setup
	@echo "Starting Project Finder..."
	make run 