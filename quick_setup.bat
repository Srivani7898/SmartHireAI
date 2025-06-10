@echo off
echo 🎯 SmartHire.AI - Quick Project Setup
echo ====================================

echo Creating project structure...
python create_files.py

echo.
echo ✅ Project structure created!
echo.
echo 📋 Next Steps:
echo 1. Copy all Python files from the code project into this folder
echo 2. Run: run_setup.bat (to install dependencies)
echo 3. Run: run_windows.bat (to start the application)
echo.
echo 📁 Files needed:
echo - app.py
echo - app_enhanced.py
echo - resume_parser.py
echo - job_matcher.py
echo - utils.py
echo - database.py
echo - requirements.txt
echo.
pause
