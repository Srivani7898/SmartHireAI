#!/bin/bash

echo "🎯 SmartHire.AI - Complete Setup Script"
echo "======================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python $python_version is installed, but Python $required_version+ is required."
    exit 1
fi

echo "✅ Python $python_version detected"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing requirements..."
pip install -r requirements.txt

# Download models
echo "🤖 Downloading models..."
python -m spacy download en_core_web_sm

# Download NLTK data
echo "📚 Downloading NLTK data..."
python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True); nltk.download('wordnet', quiet=True)"

# Initialize database
echo "🗄️ Initializing database..."
python -c "from database import init_database; init_database()"

# Create directories
echo "📁 Creating directories..."
mkdir -p data/resumes data/uploads data/exports temp logs config

# Create sample data
echo "📄 Creating sample data..."
python -c "
import os
os.makedirs('data/sample_resumes', exist_ok=True)

sample_resume = '''John Doe
Software Engineer
Email: john.doe@email.com

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

TECHNICAL SKILLS
Programming Languages: Python, JavaScript, Java, SQL
Frontend: React, HTML5, CSS3, Bootstrap
Backend: Django, Flask, Node.js
Databases: PostgreSQL, MySQL, MongoDB
Cloud: AWS, Docker, Kubernetes
'''

with open('data/sample_resumes/john_doe_resume.txt', 'w') as f:
    f.write(sample_resume)

sample_job = '''Software Engineer - Full Stack Development

Requirements:
- Bachelor's degree in Computer Science
- 3+ years of experience in software development
- Proficiency in Python, JavaScript, and React
- Experience with databases (MySQL, PostgreSQL)
- Knowledge of cloud platforms (AWS, Azure)

Responsibilities:
- Develop and maintain web applications
- Collaborate with cross-functional teams
- Write clean, maintainable code
'''

with open('data/sample_resumes/sample_job_description.txt', 'w') as f:
    f.write(sample_job)

print('✅ Sample data created')
"

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Run the application: streamlit run app_enhanced.py"
echo "3. Open browser at: http://localhost:8501"
echo "4. Login with: admin / admin123"
echo ""
echo "📁 Sample data available in: data/sample_resumes/"
echo ""
