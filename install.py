"""
Quick installation script for SmartHire.AI
Run this script to install all dependencies and set up the project
"""

import subprocess
import sys
import os

def install_requirements():
    """Install all required packages."""
    print("🚀 Installing SmartHire.AI dependencies...")
    
    try:
        # Upgrade pip first
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        
        # Install requirements
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        
        print("✅ All packages installed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Installation failed: {e}")
        return False

def download_models():
    """Download required models."""
    print("📥 Downloading required models...")
    
    try:
        # Download spaCy model
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
        print("✅ spaCy model downloaded!")
        
        # Download NLTK data
        import nltk
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('wordnet', quiet=True)
        print("✅ NLTK data downloaded!")
        
        return True
        
    except Exception as e:
        print(f"⚠️ Model download warning: {e}")
        print("You can continue, but some features may be limited.")
        return True

def main():
    """Main installation function."""
    print("=" * 60)
    print("  SmartHire.AI - Quick Installation")
    print("  NLP-Based Resume Screening System")
    print("=" * 60)
    
    if install_requirements():
        download_models()
        
        print("\n" + "=" * 60)
        print("🎉 Installation completed!")
        print("\nNext steps:")
        print("1. Run: python setup.py (for complete setup)")
        print("2. Or run: streamlit run app.py (to start immediately)")
        print("=" * 60)
    else:
        print("\n❌ Installation failed. Please check the errors above.")

if __name__ == "__main__":
    main()
