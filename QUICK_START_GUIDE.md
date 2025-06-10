# SmartHire.AI - Quick Start Guide

## 🚀 One-Command Setup

### For Windows:
\`\`\`bash
run_setup.bat
\`\`\`

### For macOS/Linux:
\`\`\`bash
chmod +x run_setup.sh
./run_setup.sh
\`\`\`

## 📋 Manual Setup (If automated setup fails)

### Step 1: Install Dependencies
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### Step 2: Download Models
\`\`\`bash
python -m spacy download en_core_web_sm
\`\`\`

### Step 3: Initialize Database
\`\`\`bash
python -c "from database import init_database; init_database()"
\`\`\`

### Step 4: Run Application
\`\`\`bash
streamlit run app_enhanced.py
\`\`\`

## 🔐 Default Login Credentials

- **Username:** admin
- **Password:** admin123

## 📁 Required Libraries

### Core Dependencies:
- `streamlit` - Web interface framework
- `sentence-transformers` - S-BERT model for semantic similarity
- `scikit-learn` - Machine learning utilities
- `pandas` - Data manipulation
- `numpy` - Numerical computing

### NLP Libraries:
- `spacy` - Advanced NLP processing
- `nltk` - Natural language toolkit
- `PyMuPDF` - PDF text extraction
- `python-docx` - Word document processing

### Database & Security:
- `sqlalchemy` - Database ORM
- `bcrypt` - Password hashing
- `python-dotenv` - Environment configuration

### Visualization:
- `plotly` - Interactive charts
- `matplotlib` - Static plots

## 🗂️ Project Structure

\`\`\`
SmartHireAI/
├── 📄 app_enhanced.py          # Main application with authentication
├── 📄 resume_parser.py         # Resume text extraction
├── 📄 job_matcher.py           # S-BERT matching engine
├── 📄 database.py              # Database operations
├── 📄 utils.py                 # Utility functions
├── 📄 setup.py                 # Complete setup script
├── 📄 requirements.txt         # Python dependencies
├── 📁 config/                  # Configuration files
├── 📁 data/                    # Database and uploads
├── 📁 logs/                    # Application logs
└── 📁 venv/                    # Virtual environment
\`\`\`

## 🎯 How to Use

### 1. Login
- Open http://localhost:8501
- Login with admin/admin123 or register new account

### 2. Create Job Posting
- Go to "Resume Screening" tab
- Enter job title and description
- Save for future use

### 3. Upload Resumes
- Upload PDF or DOCX files
- Give session a name
- Click "Start Screening Process"

### 4. View Results
- See ranked candidates with similarity scores
- Export results to CSV
- View detailed analytics

## 🔧 Configuration

### Environment Variables (.env):
\`\`\`env
DATABASE_URL=sqlite:///data/smarthire.db
MAX_FILE_SIZE_MB=10
SBERT_MODEL=all-MiniLM-L6-v2
\`\`\`

### Database Tables:
- `users` - User authentication
- `job_postings` - Saved job descriptions
- `screening_sessions` - Resume screening sessions
- `resume_analyses` - Analysis results

## 🐛 Troubleshooting

### Common Issues:

**1. Module not found errors:**
\`\`\`bash
pip install -r requirements.txt
\`\`\`

**2. spaCy model missing:**
\`\`\`bash
python -m spacy download en_core_web_sm
\`\`\`

**3. Database errors:**
\`\`\`bash
python -c "from database import init_database; init_database()"
\`\`\`

**4. Port already in use:**
\`\`\`bash
streamlit run app_enhanced.py --server.port 8502
\`\`\`

## 📞 Support

For issues or questions:
- Check the INSTALLATION_GUIDE.md for detailed setup
- Review error messages in terminal
- Ensure all dependencies are installed
- Verify Python 3.8+ is being used

## 🎓 Academic Information

**Project:** NLP-Based Resume Screening System  
**Student:** Srivani N (1AT23MC093)  
**Institution:** Atria Institute of Technology  
**Department:** MCA  
**Guide:** Mr. Yashwanth Reddy V
