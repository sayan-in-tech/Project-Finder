module.exports = {
  apps: [
    {
      name: 'project-finder-backend',
      script: 'uvicorn',
      args: 'main:app --host 0.0.0.0 --port 8000',
      cwd: './backend',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '1G',
      env: {
        NODE_ENV: 'production',
        PORT: 8000
      }
    },
    {
      name: 'project-finder-frontend',
      script: 'streamlit',
      args: 'run app.py --server.port 8501 --server.address 0.0.0.0',
      cwd: './frontend',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '1G',
      env: {
        NODE_ENV: 'production',
        PORT: 8501
      }
    }
  ]
}; 