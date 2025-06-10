"""
Script to create all necessary files for SmartHire.AI
Run this script to automatically create the project structure
"""

import os

def create_project_structure():
    """Create the complete project structure with all files."""
    
    # Create directories
    directories = [
        "config",
        "data",
        "data/resumes", 
        "data/uploads",
        "data/exports",
        "data/sample_resumes",
        "temp",
        "logs",
        "scripts"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}")
    
    # Create .env file
    env_content = """# SmartHire.AI Configuration
DATABASE_URL=sqlite:///data/smarthire.db
APP_NAME=SmartHire.AI
APP_VERSION=1.0.0
DEBUG=True
SECRET_KEY=your-secret-key-change-this-in-production
MAX_FILE_SIZE_MB=10
ALLOWED_EXTENSIONS=pdf,docx
SBERT_MODEL=all-MiniLM-L6-v2
SIMILARITY_THRESHOLD=0.5
LOG_LEVEL=INFO
LOG_FILE=logs/smarthire.log
"""
    
    with open(".env", "w") as f:
        f.write(env_content)
    print("✅ Created .env file")
    
    # Create config.py
    config_content = """import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///data/smarthire.db')
    APP_NAME = os.getenv('APP_NAME', 'SmartHire.AI')
    APP_VERSION = os.getenv('APP_VERSION', '1.0.0')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    MAX_FILE_SIZE_MB = int(os.getenv('MAX_FILE_SIZE_MB', '10'))
    ALLOWED_EXTENSIONS = os.getenv('ALLOWED_EXTENSIONS', 'pdf,docx').split(',')
    SBERT_MODEL = os.getenv('SBERT_MODEL', 'all-MiniLM-L6-v2')
    SIMILARITY_THRESHOLD = float(os.getenv('SIMILARITY_THRESHOLD', '0.5'))
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/smarthire.log')
"""
    
    with open("config/config.py", "w") as f:
        f.write(config_content)
    print("✅ Created config/config.py")
    
    # Create Windows batch files
    windows_setup = """@echo off
echo 🎯 SmartHire.AI - Windows Setup
echo ===============================

echo Checking Python installation...
python --version
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.8+ first.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python found!
echo.

echo Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ❌ Failed to create virtual environment
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\\Scripts\\activate

echo Upgrading pip...
python -m pip install --upgrade pip

echo Installing requirements...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install requirements
    pause
    exit /b 1
)

echo Downloading spaCy model...
python -m spacy download en_core_web_sm

echo Downloading NLTK data...
python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True); nltk.download('wordnet', quiet=True)"

echo Initializing database...
python -c "from database import init_database; init_database()"

echo.
echo 🎉 Setup completed successfully!
echo.
echo To run the application:
echo 1. run_windows.bat
echo 2. Or manually: venv\\Scripts\\activate then streamlit run app_enhanced.py
echo.
pause
"""
    
    with open("run_setup.bat", "w") as f:
        f.write(windows_setup)
    print("✅ Created run_setup.bat")
    
    # Create run script
    run_script = """@echo off
echo Starting SmartHire.AI...
echo.

if not exist "venv\\Scripts\\activate.bat" (
    echo ❌ Virtual environment not found!
    echo Please run run_setup.bat first.
    pause
    exit /b 1
)

call venv\\Scripts\\activate
streamlit run app_enhanced.py
pause
"""
    
    with open("run_windows.bat", "w") as f:
        f.write(run_script)
    print("✅ Created run_windows.bat")
    
    # Create sample data
    sample_resume = """John Doe
Software Engineer
Email: john.doe@email.com
Phone: (555) 123-4567

SUMMARY
Experienced Software Engineer with 4 years of experience in full-stack development.
Proficient in Python, JavaScript, React, and cloud technologies.

EDUCATION
Bachelor of Science in Computer Science
University of Technology, 2019

EXPERIENCE
Senior Software Engineer | TechCorp Inc. | 2021 - Present
- Developed web applications using React and Node.js
- Implemented RESTful APIs using Python Django
- Worked with PostgreSQL and MongoDB databases
- Deployed applications on AWS using Docker

TECHNICAL SKILLS
Programming Languages: Python, JavaScript, Java, SQL
Frontend: React, HTML5, CSS3, Bootstrap
Backend: Django, Flask, Node.js
Databases: PostgreSQL, MySQL, MongoDB
Cloud: AWS, Docker, Kubernetes
"""
    
    with open("data/sample_resumes/john_doe_resume.txt", "w") as f:
        f.write(sample_resume)
    
    sample_job = """Software Engineer - Full Stack Development

We are seeking a talented Software Engineer to join our team.

Requirements:
- Bachelor's degree in Computer Science
- 3+ years of experience in software development
- Proficiency in Python, JavaScript, and React
- Experience with databases (MySQL, PostgreSQL)
- Knowledge of cloud platforms (AWS, Azure)
- Familiarity with Docker and Kubernetes

Responsibilities:
- Develop and maintain web applications
- Collaborate with cross-functional teams
- Write clean, maintainable code
- Participate in code reviews
"""
    
    with open("data/sample_resumes/sample_job_description.txt", "w") as f:
        f.write(sample_job)
    
    print("✅ Created sample data files")
    
    print("\n🎯 Project structure created successfully!")
    print("\nNext steps:")
    print("1. Copy the main Python files (app.py, resume_parser.py, etc.) into this directory")
    print("2. Run: run_setup.bat")
    print("3. Run: run_windows.bat")

if __name__ == "__main__":
    create_project_structure()
