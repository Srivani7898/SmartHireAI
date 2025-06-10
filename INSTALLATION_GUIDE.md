# SmartHire.AI - Complete Installation Guide

## 📋 Prerequisites

Before installing SmartHire.AI, ensure you have:

- **Python 3.8 or higher** installed on your system
- **pip** package manager (comes with Python)
- **Git** (optional, for cloning repository)
- **10GB free disk space** (for models and dependencies)
- **Internet connection** (for downloading models and packages)

### Check Python Version
\`\`\`bash
python --version
# or
python3 --version
\`\`\`

## 🚀 Quick Installation (Recommended)

### Option 1: Automated Setup (Easiest)

1. **Download the project files** to your computer
2. **Open terminal/command prompt** in the project directory
3. **Run the automated setup script:**

\`\`\`bash
python setup.py
\`\`\`

This script will:
- ✅ Check Python version compatibility
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Download required models
- ✅ Set up database
- ✅ Create configuration files
- ✅ Generate sample data

### Option 2: Manual Installation

If you prefer manual control or the automated script fails:

#### Step 1: Create Virtual Environment
\`\`\`bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
\`\`\`

#### Step 2: Install Dependencies
\`\`\`bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
\`\`\`

#### Step 3: Download Models
\`\`\`bash
# Download spaCy English model
python -m spacy download en_core_web_sm

# Download NLTK data (run in Python)
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
\`\`\`

#### Step 4: Initialize Database
\`\`\`bash
python -c "from database import init_database; init_database()"
\`\`\`

## 🗂️ Project Structure After Installation

\`\`\`
SmartHireAI/
├── 📄 app.py                    # Main Streamlit application
├── 📄 resume_parser.py          # Resume parsing module
├── 📄 job_matcher.py            # S-BERT job matching
├── 📄 utils.py                  # Utility functions
├── 📄 database.py               # Database operations
├── 📄 setup.py                  # Automated setup script
├── 📄 install.py                # Quick install script
├── 📄 requirements.txt          # Python dependencies
├── 📄 .env                      # Environment configuration
├── 📁 config/                   # Configuration files
│   └── 📄 config.py
├── 📁 data/                     # Data storage
│   ├── 📄 smarthire.db         # SQLite database
│   ├── 📁 resumes/             # Uploaded resumes
│   ├── 📁 uploads/             # Temporary uploads
│   ├── 📁 exports/             # Generated reports
│   └── 📁 sample_resumes/      # Sample data
├── 📁 temp/                     # Temporary files
├── 📁 logs/                     # Application logs
├── 📁 venv/                     # Virtual environment
├── 📄 run_windows.bat           # Windows run script
└── 📄 run_unix.sh               # Unix/Linux run script
\`\`\`

## 🏃‍♂️ Running the Application

### Method 1: Using Run Scripts (Easiest)

**Windows:**
\`\`\`bash
run_windows.bat
\`\`\`

**macOS/Linux:**
\`\`\`bash
./run_unix.sh
\`\`\`

### Method 2: Manual Start

\`\`\`bash
# Activate virtual environment first
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Run the application
streamlit run app.py
\`\`\`

### Method 3: Direct Command
\`\`\`bash
# If virtual environment is already activated
streamlit run app.py
\`\`\`

The application will automatically open in your default web browser at:
**http://localhost:8501**

## 🔧 Configuration

### Environment Variables (.env file)

The `.env` file contains important configuration settings:

\`\`\`env
# Database
DATABASE_URL=sqlite:///data/smarthire.db

# Application Settings
APP_NAME=SmartHire.AI
DEBUG=True

# Security
SECRET_KEY=your-secret-key-change-this

# File Upload Settings
MAX_FILE_SIZE_MB=10
ALLOWED_EXTENSIONS=pdf,docx

# Model Settings
SBERT_MODEL=all-MiniLM-L6-v2
SIMILARITY_THRESHOLD=0.5
\`\`\`

### Database Configuration

SmartHire.AI uses SQLite by default for local development:
- **Database file:** `data/smarthire.db`
- **Default admin user:** username: `admin`, password: `admin123`

## 📊 Database Schema

The system creates the following tables:

1. **users** - User authentication and roles
2. **job_postings** - Job descriptions and requirements
3. **screening_sessions** - Resume screening sessions
4. **resume_analyses** - Analysis results and scores

## 🧪 Testing the Installation

### 1. Basic Functionality Test

1. **Start the application**
2. **Navigate to Resume Screening tab**
3. **Enter a sample job description:**
   \`\`\`
   Software Engineer position requiring Python, JavaScript, and React experience.
   Bachelor's degree in Computer Science preferred.
   \`\`\`
4. **Upload sample resumes** (convert sample text files to PDF/DOCX)
5. **Run screening process**

### 2. Sample Data Test

Use the generated sample data in `data/sample_resumes/`:
- `john_doe_resume.txt`
- `sample_job_description.txt`

Convert the text files to PDF or DOCX format for testing.

## 🔍 Troubleshooting

### Common Issues and Solutions

#### 1. Python Version Error
\`\`\`
Error: Python 3.8+ required
\`\`\`
**Solution:** Install Python 3.8 or higher from [python.org](https://python.org)

#### 2. Virtual Environment Issues
\`\`\`
Error: 'venv' is not recognized
\`\`\`
**Solution:** 
\`\`\`bash
python -m venv venv
\`\`\`

#### 3. Package Installation Failures
\`\`\`
Error: Failed to install sentence-transformers
\`\`\`
**Solutions:**
- Update pip: `pip install --upgrade pip`
- Install with no cache: `pip install --no-cache-dir sentence-transformers`
- Use conda: `conda install -c conda-forge sentence-transformers`

#### 4. spaCy Model Download Issues
\`\`\`
Error: Can't find model 'en_core_web_sm'
\`\`\`
**Solution:**
\`\`\`bash
python -m spacy download en_core_web_sm --user
\`\`\`

#### 5. Streamlit Port Issues
\`\`\`
Error: Port 8501 is already in use
\`\`\`
**Solution:**
\`\`\`bash
streamlit run app.py --server.port 8502
\`\`\`

#### 6. Database Connection Issues
\`\`\`
Error: Database locked
\`\`\`
**Solution:**
- Close all application instances
- Delete `data/smarthire.db`
- Run `python -c "from database import init_database; init_database()"`

#### 7. File Upload Issues
\`\`\`
Error: File too large
\`\`\`
**Solution:** 
- Check file size (max 10MB by default)
- Modify `MAX_FILE_SIZE_MB` in `.env` file

#### 8. Memory Issues with Large Files
\`\`\`
Error: Out of memory
\`\`\`
**Solutions:**
- Process fewer files at once
- Increase system RAM
- Use smaller resume files

### Performance Optimization

#### For Better Performance:
1. **Use SSD storage** for faster file operations
2. **Increase RAM** for processing large batches
3. **Close other applications** while running
4. **Use smaller batch sizes** for resume processing

#### System Requirements:
- **Minimum:** 4GB RAM, 2GB free disk space
- **Recommended:** 8GB RAM, 5GB free disk space
- **Optimal:** 16GB RAM, 10GB free disk space

## 🔒 Security Considerations

### For Production Use:

1. **Change default passwords:**
   \`\`\`bash
   # Change admin password in the application
   # Or update database directly
   \`\`\`

2. **Update secret key:**
   \`\`\`env
   SECRET_KEY=your-very-secure-secret-key-here
   \`\`\`

3. **Use environment variables:**
   \`\`\`bash
   export SECRET_KEY="your-secret-key"
   export DATABASE_URL="your-database-url"
   \`\`\`

4. **Enable HTTPS** for web deployment

## 🌐 Deployment Options

### Local Development
- Use the installation guide above
- Access via `http://localhost:8501`

### Streamlit Cloud
1. Push code to GitHub
2. Connect to Streamlit Cloud
3. Deploy with automatic updates

### Docker Deployment
\`\`\`dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
\`\`\`

### Heroku Deployment
1. Create `Procfile`: `web: streamlit run app.py --server.port=$PORT`
2. Deploy using Heroku CLI

## 📞 Support

### Getting Help

1. **Check this guide** for common solutions
2. **Review error messages** carefully
3. **Check system requirements**
4. **Try the troubleshooting steps**

### Academic Support
- **Student:** Srivani N (1AT23MC093)
- **Institution:** Atria Institute of Technology
- **Department:** MCA

### Technical Issues
- Check Python and package versions
- Verify internet connection for model downloads
- Ensure sufficient disk space and memory

## ✅ Installation Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Models downloaded
- [ ] Database initialized
- [ ] Configuration files created
- [ ] Application starts successfully
- [ ] Can access web interface
- [ ] Sample data works
- [ ] File upload works
- [ ] Resume screening works

## 🎉 Next Steps

After successful installation:

1. **Explore the interface** - Familiarize yourself with all features
2. **Test with sample data** - Use provided samples to understand workflow
3. **Create real job postings** - Add your own job descriptions
4. **Upload real resumes** - Test with actual resume files
5. **Analyze results** - Review the analytics dashboard
6. **Export reports** - Generate CSV reports for analysis
7. **Customize settings** - Adjust configuration as needed

**Congratulations! SmartHire.AI is now ready to use! 🎯**
