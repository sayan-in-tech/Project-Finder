/* JavaScript for Project Finder */

class ProjectFinder {
    constructor() {
        this.apiKey = '';
        this.projects = [];
        this.isLoading = false;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadApiKey();
    }

    setupEventListeners() {
        // API Key management
        document.getElementById('setApiKey').addEventListener('click', () => this.setApiKey());
        document.getElementById('apiKey').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.setApiKey();
        });

        // Project generation
        document.getElementById('generateIdeas').addEventListener('click', () => this.generateIdeas());
        document.getElementById('clearAll').addEventListener('click', () => this.clearAll());

        // Export functionality
        document.getElementById('exportProjects').addEventListener('click', () => this.exportProjects());
    }

    loadApiKey() {
        const savedApiKey = localStorage.getItem('gemini_api_key');
        if (savedApiKey) {
            this.apiKey = savedApiKey;
            document.getElementById('apiKey').value = savedApiKey;
            this.updateApiKeyStatus(true);
        }
    }

    setApiKey() {
        const apiKeyInput = document.getElementById('apiKey');
        const apiKey = apiKeyInput.value.trim();
        
        if (apiKey) {
            this.apiKey = apiKey;
            localStorage.setItem('gemini_api_key', apiKey);
            this.updateApiKeyStatus(true);
            this.showNotification('API Key saved successfully!', 'success');
        } else {
            this.showNotification('Please enter an API key', 'error');
        }
    }

    updateApiKeyStatus(isValid) {
        const statusElement = document.getElementById('apiKeyStatus');
        
        if (isValid) {
            statusElement.innerHTML = `
                <span class="badge bg-success">
                    <i class="fas fa-check me-1"></i>
                    API Key Ready
                </span>
            `;
        } else {
            statusElement.innerHTML = `
                <span class="badge bg-danger">
                    <i class="fas fa-times me-1"></i>
                    API Key Required
                </span>
            `;
        }
    }

    async generateIdeas() {
        if (!this.validateInputs()) {
            return;
        }

        this.isLoading = true;
        this.showLoading();

        try {
            const companyName = document.getElementById('companyName').value.trim();
            const userSkills = document.getElementById('userSkills').value.trim();
            const totalIdeas = parseInt(document.getElementById('totalIdeas').value);

            const requestData = {
                company_name: companyName,
                api_key: this.apiKey,
                user_skills: userSkills ? userSkills.split(',').map(s => s.trim()) : [],
                total_ideas: totalIdeas
            };

            this.updateLoadingProgress(30, 'Analyzing company...');

            const response = await fetch('/api/v1/companies/analyze-company', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestData)
            });

            this.updateLoadingProgress(60, 'Generating project ideas...');

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to generate projects');
            }

            const data = await response.json();
            this.updateLoadingProgress(90, 'Finalizing results...');

            this.projects = data.project_ideas || [];
            this.updateLoadingProgress(100, 'Complete!');

            setTimeout(() => {
                this.hideLoading();
                this.displayProjects();
                this.showNotification(`Successfully generated ${this.projects.length} project ideas!`, 'success');
            }, 1000);

        } catch (error) {
            console.error('Error generating ideas:', error);
            this.hideLoading();
            this.showNotification(`Error: ${error.message}`, 'error');
        }

        this.isLoading = false;
    }

    validateInputs() {
        if (!this.apiKey) {
            this.showNotification('Please set your API key first', 'error');
            return false;
        }

        const companyName = document.getElementById('companyName').value.trim();
        if (!companyName) {
            this.showNotification('Please enter a company name', 'error');
            return false;
        }

        return true;
    }

    showLoading() {
        document.getElementById('loading').classList.remove('d-none');
        document.getElementById('projects').style.display = 'none';
        this.scrollToElement('loading');
    }

    hideLoading() {
        document.getElementById('loading').classList.add('d-none');
        document.getElementById('projects').style.display = 'block';
    }

    updateLoadingProgress(percent, message) {
        const progressBar = document.querySelector('.progress-bar');
        const steps = document.querySelectorAll('.step');
        
        progressBar.style.width = `${percent}%`;
        
        // Update active step
        steps.forEach((step, index) => {
            step.classList.remove('active');
            if (percent >= (index + 1) * 33.33) {
                step.classList.add('active');
            }
        });

        // Update message
        document.querySelector('.loading-description').textContent = message;
    }

    displayProjects() {
        if (this.projects.length === 0) {
            document.getElementById('projects').innerHTML = '<p>No projects generated.</p>';
            return;
        }

        // Show projects header and stats
        document.querySelector('.projects-header').classList.remove('d-none');
        document.querySelector('.stats-section').classList.remove('d-none');

        // Update stats
        this.updateStats();

        // Generate projects HTML
        const projectsGrid = document.getElementById('projectsGrid');
        projectsGrid.innerHTML = '';

        this.projects.forEach((project, index) => {
            const projectCard = this.createProjectCard(project, index);
            projectsGrid.appendChild(projectCard);
        });

        // Scroll to projects section
        this.scrollToElement('projects');
    }

    createProjectCard(project, index) {
        const card = document.createElement('div');
        card.className = 'project-card fade-in';
        card.style.animationDelay = `${index * 0.1}s`;

        const techStackHtml = project.tech_stack.map(tech => 
            `<span class="tech-stack">${tech}</span>`
        ).join('');

        const difficultyClass = `difficulty-${project.difficulty}`;

        card.innerHTML = `
            <h3 class="project-title">${project.title}</h3>
            
            <div class="project-challenge">
                <strong>Challenge:</strong> ${project.challenge_title}
            </div>
            
            <div class="project-section">
                <div class="project-label">Description</div>
                <div class="project-content">${project.description}</div>
            </div>
            
            <div class="project-section">
                <div class="project-label">Tech Stack</div>
                <div class="project-content">${techStackHtml}</div>
            </div>
            
            <div class="project-section">
                <div class="project-label">Demo Hook</div>
                <div class="demo-hook">
                    <i class="fas fa-lightbulb me-2"></i>
                    ${project.demo_hook}
                </div>
            </div>
            
            <div class="project-meta">
                <span class="difficulty-badge ${difficultyClass}">
                    ${project.difficulty.charAt(0).toUpperCase() + project.difficulty.slice(1)}
                </span>
                <span>
                    <i class="fas fa-clock me-1"></i>
                    ${project.estimated_duration}
                </span>
            </div>
        `;

        return card;
    }

    updateStats() {
        const totalProjects = this.projects.length;
        const companiesAnalyzed = new Set(this.projects.map(p => p.company_name)).size;
        const uniqueTechs = new Set(this.projects.flatMap(p => p.tech_stack)).size;

        document.getElementById('totalProjects').textContent = totalProjects;
        document.getElementById('companiesAnalyzed').textContent = companiesAnalyzed;
        document.getElementById('technologiesSuggested').textContent = uniqueTechs;
    }

    clearAll() {
        this.projects = [];
        document.getElementById('projectsGrid').innerHTML = '';
        document.querySelector('.projects-header').classList.add('d-none');
        document.querySelector('.stats-section').classList.add('d-none');
        
        // Clear form
        document.getElementById('companyName').value = '';
        document.getElementById('userSkills').value = '';
        document.getElementById('totalIdeas').value = '4';
        
        this.showNotification('All projects cleared!', 'success');
    }

    exportProjects() {
        if (this.projects.length === 0) {
            this.showNotification('No projects to export', 'error');
            return;
        }

        const exportData = {
            generated_at: new Date().toISOString(),
            total_projects: this.projects.length,
            projects: this.projects
        };

        const dataStr = JSON.stringify(exportData, null, 2);
        const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
        
        const exportFileDefaultName = `project_ideas_${new Date().toISOString().split('T')[0]}.json`;
        
        const linkElement = document.createElement('a');
        linkElement.setAttribute('href', dataUri);
        linkElement.setAttribute('download', exportFileDefaultName);
        linkElement.click();
        
        this.showNotification('Projects exported successfully!', 'success');
    }

    showNotification(message, type) {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 100px; right: 20px; z-index: 1050; max-width: 300px;';
        
        notification.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(notification);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 5000);
    }

    scrollToElement(elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            element.scrollIntoView({ behavior: 'smooth' });
        }
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ProjectFinder();
});

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});

// Add some interactivity to the hero section
document.addEventListener('DOMContentLoaded', () => {
    const heroIcon = document.querySelector('.hero-icon');
    if (heroIcon) {
        heroIcon.addEventListener('mouseenter', () => {
            heroIcon.style.transform = 'scale(1.1) rotate(5deg)';
        });
        
        heroIcon.addEventListener('mouseleave', () => {
            heroIcon.style.transform = 'scale(1) rotate(0deg)';
        });
    }
});
