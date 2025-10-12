# 🤖 AI Resume Parser

An intelligent resume parsing application powered by AI that analyzes PDF resumes and provides detailed insights, ratings, and recommendations.
## images & videos


https://github.com/user-attachments/assets/3a1c8590-80ff-4a63-98e3-b12f81006677



<img width="1919" height="927" alt="Screenshot 2025-10-12 230115" src="https://github.com/user-attachments/assets/30de9260-8b2f-4a5b-9ea5-91ca60d90b47" />
<img width="1901" height="838" alt="Screenshot 2025-10-12 230153" src="https://github.com/user-attachments/assets/81abe790-13e7-4d7f-b7d1-e5e43ef296a3" />



## ✨ Features

- **📄 PDF Resume Upload**: Support for PDF resume uploads via drag & drop or file selection
- **🧠 AI-Powered Analysis**: Uses Google's Gemini AI to extract and analyze resume content
- **📊 Comprehensive Scoring**: Provides overall resume rating out of 10
- **🔍 Detailed Extraction**: Extracts personal information, skills, experience, education, and projects
- **💡 Smart Recommendations**: AI-generated suggestions for improvement and upskilling
- **📈 Resume History**: Track and manage multiple resume analyses
- **🎨 Modern UI**: Clean, responsive web interface
- **🚀 Fast Processing**: Quick analysis and results display

## 🛠️ Technology Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Database**: SQLite (default) / PostgreSQL (optional)
- **AI**: Google Gemini API
- **PDF Processing**: PyPDF2
- **Styling**: Custom CSS with modern design

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Google Gemini API key (optional, falls back to mock analysis)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/sujal-github/ai-resume-parser.git
cd ai-resume-parser
```

### 2. Set Up Environment

#### Option A: Using the Start Script (Recommended)

```bash
python start.py
```

The start script will automatically:
- Check Python version compatibility
- Install required dependencies
- Guide you through environment setup
- Start the application

#### Option B: Manual Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables**
   ```bash
   # Windows
   copy .env.example .env
   
   # Linux/Mac
   cp .env.example .env
   
   # Edit .env file with your configuration
   ```

3. **Start the Application**
   ```bash
   cd backend
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

### 3. Access the Application

Open your web browser and navigate to:
```
http://localhost:8000
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Google Gemini API Configuration (Optional)
GEMINI_API_KEY=your_gemini_api_key_here

# Database Configuration (Optional - defaults to SQLite)
DATABASE_URL=sqlite:///./resume_parser.db
# For PostgreSQL: DATABASE_URL=postgresql://user:password@localhost/dbname

# Application Settings
DEBUG=True
HOST=0.0.0.0
PORT=8000
```

### Getting Google Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the key and add it to your `.env` file

**Note**: If no API key is provided, the application will use mock analysis for demonstration purposes.

## 📁 Project Structure

```
ai-resume-parser/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── database.py          # Database models and configuration
│   ├── resume_parser.py     # AI resume analysis logic
│   └── schemas.py           # Pydantic schemas
├── frontend/
│   ├── index.html           # Main HTML file
│   ├── style.css            # Styling
│   └── script.js            # Frontend JavaScript
├── sample_data/             # Sample resumes for testing
├── .env.example            # Environment variables template
├── requirements.txt        # Python dependencies
├── start.py               # Application startup script
└── README.md              # This file
```

## 🎯 Usage

### Uploading a Resume

1. **Navigate to the Upload Tab**: Click on "📤 Upload Resume"
2. **Select PDF File**: Either drag & drop a PDF file or click "Choose File"
3. **Wait for Analysis**: The AI will analyze the resume (may take a few moments)
4. **View Results**: Scroll down to see detailed analysis results

### Features of Analysis

- **Personal Information**: Name, email, phone, address, LinkedIn, GitHub
- **Skills**: Technical and soft skills extraction
- **Work Experience**: Job history with descriptions and technologies
- **Education**: Academic background and qualifications
- **Projects**: Personal and professional projects
- **AI Recommendations**: Strengths, improvement areas, and upskilling suggestions
- **Overall Rating**: Numerical score out of 10

### Managing Resume History

1. **Switch to History Tab**: Click on "📊 Resume History"
2. **View All Resumes**: See all previously analyzed resumes
3. **View Details**: Click "👁️ Details" to see full analysis
4. **Delete Resumes**: Click "🗑️ Delete" to remove unwanted entries

## 🐛 Troubleshooting

### Common Issues

1. **Dependencies Installation Failed**
   ```bash
   # Try upgrading pip first
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

2. **Port Already in Use**
   ```bash
   # Change port in start.py or use:
   uvicorn main:app --port 8001
   ```

3. **PDF Upload Issues**
   - Ensure the file is a valid PDF
   - Check file size (should be reasonable)
   - Try a different PDF file

4. **Database Connection Issues**
   - For SQLite: Ensure write permissions in the directory
   - For PostgreSQL: Verify database URL and server status

### Getting Help

If you encounter issues:

1. Check the console output for error messages
2. Ensure all prerequisites are installed
3. Verify your environment configuration
4. Try with a sample resume from `sample_data/`

## 🔧 Development

### Setting Up Development Environment

1. **Clone and Setup**
   ```bash
   git clone https://github.com/sujal-github/ai-resume-parser.git
   cd ai-resume-parser
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   
   pip install -r requirements.txt
   ```

2. **Run in Development Mode**
   ```bash
   cd backend
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Make Changes**
   - Frontend files are served directly
   - Backend changes trigger auto-reload

### API Endpoints

- `GET /`: Serve main application
- `POST /upload-resume`: Upload and analyze resume
- `GET /resumes`: Get all resume history
- `GET /resume/{id}`: Get specific resume details
- `DELETE /resume/{id}`: Delete a resume
- `GET /health`: Health check endpoint

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Gemini AI for intelligent resume analysis
- FastAPI for the robust backend framework
- The open-source community for various tools and libraries

## 📞 Support

If you have questions or need support:

- Create an issue in the GitHub repository
- Check the troubleshooting section above
- Review the documentation

## 🌟 Sample Output Structure

```json
{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "phone": "+1-234-567-8900",
  "core_skills": ["Python", "Machine Learning", "FastAPI"],
  "soft_skills": ["Leadership", "Communication"],
  "work_experience": [
    {
      "position": "Senior Software Engineer",
      "company": "Tech Corp",
      "duration": "2021-2024",
      "description": ["Led development of ML systems", "Managed team of 5 engineers"]
    }
  ],
  "education": [
    {
      "degree": "Master of Science",
      "field_of_study": "Computer Science",
      "institution": "University of Technology",
      "graduation_date": "2020"
    }
  ],
  "projects": [
    {
      "name": "AI Resume Parser",
      "description": "Built an intelligent resume parsing system",
      "technologies": ["Python", "FastAPI", "Machine Learning"]
    }
  ],
  "resume_rating": 8.5,
  "improvement_areas": "Add more quantifiable achievements and metrics to demonstrate impact.",
  "upskill_suggestions": "Consider learning Docker, Kubernetes, and cloud technologies like AWS or Azure.",
  "strengths": "Strong technical background with good balance of technical and leadership skills."
}
```

---

**Made with ❤️ by Shashvat**

*Happy Resume Analyzing! 🚀*
