import os
import tempfile
import shutil
from typing import Optional
import streamlit as st

def create_directories():
    """Create necessary directories for the application."""
    directories = ['resumes', 'temp', 'exports']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")

def save_uploaded_file(uploaded_file) -> str:
    """
    Save uploaded file to temporary directory.
    
    Args:
        uploaded_file: Streamlit uploaded file object
        
    Returns:
        str: Path to saved file
    """
    try:
        # Create temp directory if it doesn't exist
        temp_dir = "temp"
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        
        # Generate unique filename
        file_path = os.path.join(temp_dir, uploaded_file.name)
        
        # Save file
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        return file_path
        
    except Exception as e:
        st.error(f"Error saving file: {str(e)}")
        raise

def format_score(score: float) -> str:
    """
    Format similarity score for display.
    
    Args:
        score (float): Similarity score between 0 and 1
        
    Returns:
        str: Formatted score string
    """
    percentage = score * 100
    return f"{percentage:.1f}%"

def get_score_color(score: float) -> str:
    """
    Get color based on score value.
    
    Args:
        score (float): Similarity score between 0 and 1
        
    Returns:
        str: Color name or hex code
    """
    if score >= 0.8:
        return "#28a745"  # Green
    elif score >= 0.6:
        return "#ffc107"  # Yellow
    elif score >= 0.4:
        return "#fd7e14"  # Orange
    else:
        return "#dc3545"  # Red

def get_score_category(score: float) -> str:
    """
    Get category based on score value.
    
    Args:
        score (float): Similarity score between 0 and 1
        
    Returns:
        str: Score category
    """
    if score >= 0.8:
        return "Excellent Match"
    elif score >= 0.6:
        return "Good Match"
    elif score >= 0.4:
        return "Fair Match"
    else:
        return "Poor Match"

def clean_temp_files():
    """Clean up temporary files."""
    temp_dir = "temp"
    if os.path.exists(temp_dir):
        try:
            shutil.rmtree(temp_dir)
            os.makedirs(temp_dir)
            print("✅ Cleaned temporary files")
        except Exception as e:
            print(f"❌ Error cleaning temp files: {str(e)}")

def validate_file_type(filename: str) -> bool:
    """
    Validate if file type is supported.
    
    Args:
        filename (str): Name of the file
        
    Returns:
        bool: True if file type is supported
    """
    supported_extensions = ['.pdf', '.docx']
    file_extension = os.path.splitext(filename)[1].lower()
    return file_extension in supported_extensions

def get_file_size_mb(file_path: str) -> float:
    """
    Get file size in MB.
    
    Args:
        file_path (str): Path to file
        
    Returns:
        float: File size in MB
    """
    try:
        size_bytes = os.path.getsize(file_path)
        size_mb = size_bytes / (1024 * 1024)
        return round(size_mb, 2)
    except Exception:
        return 0.0

def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Truncate text to specified length.
    
    Args:
        text (str): Input text
        max_length (int): Maximum length
        
    Returns:
        str: Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."

def extract_filename_without_extension(file_path: str) -> str:
    """
    Extract filename without extension.
    
    Args:
        file_path (str): Path to file
        
    Returns:
        str: Filename without extension
    """
    return os.path.splitext(os.path.basename(file_path))[0]

def create_download_link(data: str, filename: str, link_text: str) -> str:
    """
    Create download link for data.
    
    Args:
        data (str): Data to download
        filename (str): Name of download file
        link_text (str): Text for download link
        
    Returns:
        str: HTML download link
    """
    import base64
    
    b64 = base64.b64encode(data.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">{link_text}</a>'
    return href

def format_list_for_display(items: list, max_items: int = 5) -> str:
    """
    Format list for display with limited items.
    
    Args:
        items (list): List of items
        max_items (int): Maximum items to display
        
    Returns:
        str: Formatted string
    """
    if not items:
        return "None"
    
    if len(items) <= max_items:
        return ", ".join(items)
    else:
        displayed_items = items[:max_items]
        remaining = len(items) - max_items
        return f"{', '.join(displayed_items)} (+{remaining} more)"

def calculate_match_statistics(scores: list) -> dict:
    """
    Calculate statistics for match scores.
    
    Args:
        scores (list): List of similarity scores
        
    Returns:
        dict: Statistics dictionary
    """
    if not scores:
        return {
            'mean': 0.0,
            'median': 0.0,
            'min': 0.0,
            'max': 0.0,
            'std': 0.0
        }
    
    import statistics
    
    return {
        'mean': statistics.mean(scores),
        'median': statistics.median(scores),
        'min': min(scores),
        'max': max(scores),
        'std': statistics.stdev(scores) if len(scores) > 1 else 0.0
    }

def generate_report_summary(results: list, job_description: str) -> dict:
    """
    Generate summary report for screening results.
    
    Args:
        results (list): List of screening results
        job_description (str): Job description text
        
    Returns:
        dict: Summary report
    """
    if not results:
        return {}
    
    scores = [r['similarity_score'] for r in results]
    stats = calculate_match_statistics(scores)
    
    # Categorize results
    excellent = sum(1 for score in scores if score >= 0.8)
    good = sum(1 for score in scores if 0.6 <= score < 0.8)
    fair = sum(1 for score in scores if 0.4 <= score < 0.6)
    poor = sum(1 for score in scores if score < 0.4)
    
    return {
        'total_resumes': len(results),
        'statistics': stats,
        'categories': {
            'excellent': excellent,
            'good': good,
            'fair': fair,
            'poor': poor
        },
        'top_candidate': results[0]['filename'] if results else None,
        'top_score': max(scores) if scores else 0.0,
        'job_description_length': len(job_description.split())
    }
