# Project Finder 🚀

A minimal, AI-powered Streamlit app that helps users discover custom side project ideas tailored to specific companies. Perfect for job seekers who want to showcase relevant skills and win interviews.

## ✨ Features

- **Company Analysis**: Get AI-powered company profiles including industry, tech stack, and recent highlights
- **Challenge Identification**: Discover 3 common engineering challenges each company faces
- **Project Generation**: Generate 3-5 concrete project ideas per challenge with:
  - Clear project titles and descriptions
  - Recommended tech stacks
  - Demo hooks that impress interviewers
- **Export Options**: Download results as JSON or CSV
- **Clean UI**: Intuitive Streamlit interface with expandable cards and organized layouts

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key (free from [Google AI Studio](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd Project-Finder
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key** (Choose one method):

   **Method A: Using Streamlit secrets (Recommended)**
   ```bash
   mkdir .streamlit
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   ```
   Edit `.streamlit/secrets.toml` and add your API key:
   ```toml
   GEMINI_API_KEY = "your_actual_api_key_here"
   ```

   **Method B: Environment variable**
   ```bash
   export GEMINI_API_KEY="your_actual_api_key_here"  # On Windows: set GEMINI_API_KEY=your_key
   ```

   **Method C: Enter in app**
   You can also enter your API key directly in the app's sidebar

4. **Run the app**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser** to `http://localhost:8501`

## 📖 How to Use

1. **Enter your Gemini API key** (if not configured in secrets)
2. **Add company names** in the sidebar (one per line)
3. **Optionally add your skills** to get more personalized suggestions
4. **Click "Generate Ideas"** and wait for AI processing
5. **Browse generated projects** organized by company
6. **Export results** as JSON or CSV for future reference

## 🎯 Example Output

For a company like "Acme Analytics", you might get projects like:

| Project | Tech Stack | Demo Hook |
|---------|------------|-----------|
| Real-time ETL Pipeline | Python, Kafka, S3 | Live dashboard with processed logs |
| Data Quality Monitor | Python, Great Expectations, SQLite | Automated data validation reports |
| Customer Churn Predictor | Python, scikit-learn, Streamlit | Interactive prediction dashboard |

## 🏗️ Project Structure

```
Project-Finder/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── .streamlit/
│   └── secrets.toml.example       # API key configuration template
└── README.md                      # This file
```

## 🔧 Configuration

### API Key Security

- **Never commit your actual API key** to version control
- Use `.streamlit/secrets.toml` for local development
- For deployment, use environment variables or your platform's secret management

### Customization

The app is designed to be easily customizable:

- **Modify prompts**: Edit the prompt templates in the `GeminiService` class
- **Adjust UI**: Update the Streamlit layout in the `main()` function
- **Add features**: Extend the `GeminiService` class or add new session state variables

## 🌐 Deployment

### Streamlit Community Cloud

1. Fork this repository
2. Connect your GitHub account to [Streamlit Community Cloud](https://share.streamlit.io/)
3. Deploy the app and add your `GEMINI_API_KEY` in the app secrets

### Other Platforms

The app can be deployed to any platform that supports Python and Streamlit:
- Heroku
- Railway
- Render
- Google Cloud Run
- AWS EC2

Just ensure your `GEMINI_API_KEY` environment variable is set.

## 🔍 Troubleshooting

### Common Issues

1. **"API key not found"**
   - Ensure your API key is properly set in `.streamlit/secrets.toml` or as an environment variable
   - Verify the API key is valid and has proper permissions

2. **"Rate limit exceeded"**
   - The app includes small delays between API calls
   - For heavy usage, consider implementing more sophisticated rate limiting

3. **"JSON parsing error"**
   - This can happen if Gemini returns unexpected format
   - The app includes fallback parsing, but some edge cases might need manual handling

4. **Empty results**
   - Try with well-known company names first
   - Ensure your API key has sufficient quota
   - Check if the company name is spelled correctly

### Performance Tips

- **Start with 1-2 companies** to test the app
- **Use specific, well-known company names** for better results
- **Clear results** before generating new ones to avoid confusion

## 🤝 Contributing

This is designed as a minimal, single-file application. If you want to contribute:

1. Keep changes focused and minimal
2. Maintain the single-file architecture
3. Test thoroughly with different company names
4. Update documentation as needed

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🎯 Future Enhancements

Potential improvements (while keeping it minimal):

- **Skill-based filtering**: Use the optional skills input to filter project suggestions
- **Project templates**: Generate basic README.md files for selected projects
- **Interview prep**: Add talking points for each project
- **Company data integration**: Light scraping for more accurate company information

---

**Happy coding and good luck with your interviews! 🚀**
