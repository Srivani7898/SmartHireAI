"""
SmartHire.AI Setup Script
Complete installation and configuration script for local development
"""

import os
import sys
import subprocess
import sqlite3
from pathlib import Path

def print_header(text):
    """Print formatted header."""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def print_step(step_num, text):
    """Print formatted step."""
    print(f"\n🔸 Step {step_num}: {text}")

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"   Running: {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"   ✅ Success: {description}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Error: {description}")
        print(f"   Error details: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    print_step(1, "Checking Python Version")
    
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} is not compatible")
        print("   Please install Python 3.8 or higher")
        return False

def create_virtual_environment():
    """Create and activate virtual environment."""
    print_step(2, "Creating Virtual Environment")
    
    if not os.path.exists("venv"):
        if run_command("python -m venv venv", "Creating virtual environment"):
            print("   📁 Virtual environment created successfully")
        else:
            return False
    else:
        print("   📁 Virtual environment already exists")
    
    # Provide activation instructions
    if os.name == 'nt':  # Windows
        activate_cmd = "venv\\Scripts\\activate"
    else:  # Unix/Linux/MacOS
        activate_cmd = "source venv/bin/activate"
    
    print(f"   💡 To activate virtual environment, run: {activate_cmd}")
    return True

def install_dependencies():
    """Install required Python packages."""
    print_step(3, "Installing Python Dependencies")
    
    # Determine pip command
    pip_cmd = "venv/Scripts/pip" if os.name == 'nt' else "venv/bin/pip"
    
    packages = [
        "streamlit>=1.28.0",
        "sentence-transformers>=2.2.2",
        "PyMuPDF>=1.23.0",
        "python-docx>=0.8.11",
        "scikit-learn>=1.3.0",
        "spacy>=3.6.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "plotly>=5.15.0",
        "nltk>=3.8.1",
        "sqlalchemy>=2.0.0",
        "python-dotenv>=1.0.0",
        "bcrypt>=4.0.0",
        "Pillow>=10.0.0"
    ]
    
    print("   📦 Installing packages...")
    for package in packages:
        if not run_command(f"{pip_cmd} install {package}", f"Installing {package.split('>=')[0]}"):
            return False
    
    return True

def download_models():
    """Download required models and data."""
    print_step(4, "Downloading Required Models")
    
    # Determine python command
    python_cmd = "venv/Scripts/python" if os.name == 'nt' else "venv/bin/python"
    
    # Download spaCy model
    if not run_command(f"{python_cmd} -m spacy download en_core_web_sm", "Downloading spaCy English model"):
        print("   ⚠️  spaCy model download failed, but you can continue")
    
    # Download NLTK data
    print("   📚 Downloading NLTK data...")
    nltk_script = """
import nltk
import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)
print('NLTK data downloaded successfully')
"""
    
    with open("temp_nltk_download.py", "w") as f:
        f.write(nltk_script)
    
    run_command(f"{python_cmd} temp_nltk_download.py", "Downloading NLTK data")
    
    # Clean up
    if os.path.exists("temp_nltk_download.py"):
        os.remove("temp_nltk_download.py")
    
    return True

def create_directories():
    """Create necessary directories."""
    print_step(5, "Creating Project Directories")
    
    directories = [
        "data",
        "data/resumes",
        "data/uploads", 
        "data/exports",
        "temp",
        "logs",
        "config"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"   📁 Created directory: {directory}")
    
    return True

def setup_database():
    """Initialize SQLite database."""
    print_step(6, "Setting Up Database")
    
    try:
        # Create database connection
        conn = sqlite3.connect('data/smarthire.db')
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'user',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS job_postings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                requirements TEXT,
                created_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (created_by) REFERENCES users (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS screening_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_posting_id INTEGER,
                session_name TEXT,
                created_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (job_posting_id) REFERENCES job_postings (id),
                FOREIGN KEY (created_by) REFERENCES users (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS resume_analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER,
                filename TEXT NOT NULL,
                similarity_score REAL,
                skills_extracted TEXT,
                education_extracted TEXT,
                experience_extracted TEXT,
                analysis_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES screening_sessions (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        
        print("   ✅ Database initialized successfully")
        print("   📊 Created tables: users, job_postings, screening_sessions, resume_analyses")
        return True
        
    except Exception as e:
        print(f"   ❌ Database setup failed: {str(e)}")
        return False

def create_config_files():
    """Create configuration files."""
    print_step(7, "Creating Configuration Files")
    
    # Create .env file
    env_content = """# SmartHire.AI Configuration
# Database
DATABASE_URL=sqlite:///data/smarthire.db

# Application Settings
APP_NAME=SmartHire.AI
APP_VERSION=1.0.0
DEBUG=True

# Security
SECRET_KEY=your-secret-key-change-this-in-production

# File Upload Settings
MAX_FILE_SIZE_MB=10
ALLOWED_EXTENSIONS=pdf,docx

# Model Settings
SBERT_MODEL=all-MiniLM-L6-v2
SIMILARITY_THRESHOLD=0.5

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/smarthire.log
"""
    
    with open(".env", "w") as f:
        f.write(env_content)
    print("   📄 Created .env configuration file")
    
    # Create config.py
    config_content = """import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///data/smarthire.db')
    
    # Application
    APP_NAME = os.getenv('APP_NAME', 'SmartHire.AI')
    APP_VERSION = os.getenv('APP_VERSION', '1.0.0')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # File Upload
    MAX_FILE_SIZE_MB = int(os.getenv('MAX_FILE_SIZE_MB', '10'))
    ALLOWED_EXTENSIONS = os.getenv('ALLOWED_EXTENSIONS', 'pdf,docx').split(',')
    
    # Model Settings
    SBERT_MODEL = os.getenv('SBERT_MODEL', 'all-MiniLM-L6-v2')
    SIMILARITY_THRESHOLD = float(os.getenv('SIMILARITY_THRESHOLD', '0.5'))
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/smarthire.log')
"""
    
    with open("config/config.py", "w") as f:
        f.write(config_content)
    print("   📄 Created config/config.py")
    
    return True

def create_sample_data():
    """Create sample data for testing."""
    print_step(8, "Creating Sample Data")
    
    # Sample resume content
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
    
    # Create sample resume file
    sample_dir = "data/sample_resumes"
    Path(sample_dir).mkdir(parents=True, exist_ok=True)
    
    with open(f"{sample_dir}/john_doe_resume.txt", "w") as f:
        f.write(sample_resume)
    
    # Sample job description
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
    
    with open(f"{sample_dir}/sample_job_description.txt", "w") as f:
        f.write(sample_job)
    
    print("   📄 Created sample resume and job description")
    return True

def create_run_scripts():
    """Create scripts to run the application."""
    print_step(9, "Creating Run Scripts")
    
    # Windows batch file
    windows_script = """@echo off
echo Starting SmartHire.AI...
call venv\\Scripts\\activate
streamlit run app.py
pause
"""
    
    with open("run_windows.bat", "w") as f:
        f.write(windows_script)
    print("   📄 Created run_windows.bat")
    
    # Unix/Linux shell script
    unix_script = """#!/bin/bash
echo "Starting SmartHire.AI..."
source venv/bin/activate
streamlit run app.py
"""
    
    with open("run_unix.sh", "w") as f:
        f.write(unix_script)
    
    # Make shell script executable
    if os.name != 'nt':
        os.chmod("run_unix.sh", 0o755)
    
    print("   📄 Created run_unix.sh")
    return True

def print_completion_message():
    """Print completion message with next steps."""
    print_header("🎉 INSTALLATION COMPLETED SUCCESSFULLY!")
    
    print("""
📋 NEXT STEPS:

1. Activate Virtual Environment:
   Windows: venv\\Scripts\\activate
   Unix/Linux/Mac: source venv/bin/activate

2. Run the Application:
   Windows: run_windows.bat
   Unix/Linux/Mac: ./run_unix.sh
   Or manually: streamlit run app.py

3. Open in Browser:
   The app will automatically open at: http://localhost:8501

4. Test the System:
   - Use sample data in data/sample_resumes/
   - Upload the sample job description
   - Upload resume files (convert .txt to .pdf/.docx)

📁 PROJECT STRUCTURE:
   ├── app.py                 # Main application
   ├── resume_parser.py       # Resume parsing module
   ├── job_matcher.py         # Job matching with S-BERT
   ├── utils.py              # Utility functions
   ├── database.py           # Database operations
   ├── config/               # Configuration files
   ├── data/                 # Data storage
   ├── logs/                 # Application logs
   └── venv/                 # Virtual environment

🔧 CONFIGURATION:
   - Edit .env file for custom settings
   - Database: SQLite (data/smarthire.db)
   - Logs: logs/smarthire.log

📞 SUPPORT:
   If you encounter issues, check the troubleshooting section in README.md
""")

def main():
    """Main setup function."""
    print_header("🎯 SmartHire.AI - Complete Setup Script")
    print("Setting up NLP-Based Resume Screening System")
    print("Developed by: Srivani N (1AT23MC093)")
    print("Institution: Atria Institute of Technology")
    
    # Check if already in virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("\n⚠️  You are already in a virtual environment.")
        print("Please deactivate it first and run this script again.")
        return
    
    steps = [
        check_python_version,
        create_virtual_environment,
        install_dependencies,
        download_models,
        create_directories,
        setup_database,
        create_config_files,
        create_sample_data,
        create_run_scripts
    ]
    
    for step in steps:
        if not step():
            print(f"\n❌ Setup failed at: {step.__name__}")
            print("Please check the error messages above and try again.")
            return
    
    print_completion_message()

if __name__ == "__main__":
    main()
