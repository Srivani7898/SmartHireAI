"""
Enhanced SmartHire.AI Application with Database Integration
Main Streamlit application with authentication and data persistence
"""

import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from resume_parser import ResumeParser
from job_matcher import JobMatcher
from utils import create_directories, save_uploaded_file, format_score
from database import db_manager, init_database, get_database_info
from config.config import Config

# Page configuration
st.set_page_config(
    page_title="SmartHire.AI - Resume Screening System",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
if 'db_initialized' not in st.session_state:
    init_database()
    st.session_state.db_initialized = True

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    .resume-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #28a745;
    }
    .low-score {
        border-left-color: #dc3545 !important;
    }
    .medium-score {
        border-left-color: #ffc107 !important;
    }
    .high-score {
        border-left-color: #28a745 !important;
    }
    .login-form {
        max-width: 400px;
        margin: 0 auto;
        padding: 2rem;
        background: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

def login_page():
    """Display login page."""
    st.markdown("""
    <div class="main-header">
        <h1>🎯 SmartHire.AI</h1>
        <h3>NLP-Based Resume Screening System</h3>
        <p>Please login to continue</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="login-form">', unsafe_allow_html=True)
        
        st.subheader("🔐 Login")
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            col_a, col_b = st.columns(2)
            with col_a:
                login_button = st.form_submit_button("Login", use_container_width=True)
            with col_b:
                register_button = st.form_submit_button("Register", use_container_width=True)
            
            if login_button:
                if username and password:
                    if db_manager.verify_password(username, password):
                        user = db_manager.get_user_by_username(username)
                        st.session_state.logged_in = True
                        st.session_state.user = {
                            'id': user.id,
                            'username': user.username,
                            'email': user.email,
                            'role': user.role
                        }
                        st.success("✅ Login successful!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password")
                else:
                    st.error("❌ Please enter both username and password")
            
            if register_button:
                if username and password:
                    if len(password) < 6:
                        st.error("❌ Password must be at least 6 characters")
                    else:
                        user = db_manager.create_user(username, f"{username}@smarthire.ai", password)
                        if user:
                            st.success("✅ Registration successful! Please login.")
                        else:
                            st.error("❌ Registration failed. Username might already exist.")
                else:
                    st.error("❌ Please enter both username and password")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Default credentials info
        st.info("""
        **Default Admin Credentials:**
        - Username: admin
        - Password: admin123
        
        **Or register a new account above**
        """)

def main_app():
    """Main application interface."""
    # Header
    st.markdown(f"""
    <div class="main-header">
        <h1>🎯 SmartHire.AI</h1>
        <h3>NLP-Based Resume Screening System for Recruitment Automation</h3>
        <p>Welcome, {st.session_state.user['username']} | Role: {st.session_state.user['role']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize components
    create_directories()
    resume_parser = ResumeParser()
    job_matcher = JobMatcher()
    
    # Sidebar
    with st.sidebar:
        st.header("👤 User Info")
        st.write(f"**Username:** {st.session_state.user['username']}")
        st.write(f"**Role:** {st.session_state.user['role']}")
        
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()
        
        st.header("📊 Project Info")
        st.info("""
        **Developed by:** Srivani N (1AT23MC093)
        
        **Under Guidance of:** Mr. Yashwanth Reddy V
        
        **Institution:** Atria Institute of Technology
        
        **Department:** MCA
        """)
        
        st.header("🔧 Features")
        st.markdown("""
        - ✅ Multi-format resume parsing (PDF, DOCX)
        - ✅ S-BERT semantic matching
        - ✅ Cosine similarity ranking
        - ✅ Database persistence
        - ✅ User authentication
        - ✅ Interactive dashboard
        - ✅ Detailed analytics
        """)
        
        # Database info
        db_info = get_database_info()
        st.header("🗄️ Database Status")
        if db_info['status'] == 'connected':
            st.success("✅ Connected")
            stats = db_info['statistics']
            st.metric("Total Analyses", stats['total_analyses'])
            st.metric("Total Sessions", stats['total_sessions'])
        else:
            st.error("❌ Connection Error")
    
    # Main content
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Resume Screening", "📈 Analytics", "📋 Job Management", "ℹ️ About"])
    
    with tab1:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.header("📝 Job Description")
            
            # Load saved job postings
            job_postings = db_manager.get_job_postings(limit=10)
            job_options = ["Enter new job description"] + [f"{job.title} (ID: {job.id})" for job in job_postings]
            
            selected_job = st.selectbox("Select existing job or create new:", job_options)
            
            if selected_job == "Enter new job description":
                job_title = st.text_input("Job Title:", placeholder="e.g., Senior Software Engineer")
                job_description = st.text_area(
                    "Enter the job description:",
                    height=300,
                    placeholder="Enter detailed job requirements, skills, qualifications, and responsibilities..."
                )
                
                if st.button("💾 Save Job Posting") and job_title and job_description:
                    saved_job = db_manager.create_job_posting(
                        title=job_title,
                        description=job_description,
                        created_by=st.session_state.user['id']
                    )
                    if saved_job:
                        st.success(f"✅ Job posting saved with ID: {saved_job.id}")
                        st.rerun()
            else:
                # Load selected job
                job_id = int(selected_job.split("ID: ")[1].split(")")[0])
                selected_job_posting = db_manager.get_job_posting_by_id(job_id)
                job_title = selected_job_posting.title
                job_description = selected_job_posting.description
                
                st.text_input("Job Title:", value=job_title, disabled=True)
                st.text_area("Job Description:", value=job_description, height=300, disabled=True)
            
            # Job analysis
            if job_description:
                with st.expander("🔍 Job Description Analysis"):
                    analysis = job_matcher.analyze_job_description(job_description)
                    
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.metric("Word Count", analysis['word_count'])
                        st.metric("Key Skills Found", len(analysis['skills']))
                    
                    with col_b:
                        st.metric("Education Keywords", len(analysis['education']))
                        st.metric("Experience Keywords", len(analysis['experience']))
                    
                    if analysis['skills']:
                        st.write("**Key Skills Detected:**")
                        skills_text = ", ".join(analysis['skills'][:10])
                        st.write(skills_text)
        
        with col2:
            st.header("📄 Resume Upload")
            
            session_name = st.text_input("Session Name:", placeholder="e.g., Software Engineer Screening - March 2024")
            
            uploaded_files = st.file_uploader(
                "Upload resumes (PDF or DOCX):",
                type=['pdf', 'docx'],
                accept_multiple_files=True,
                help="You can upload multiple resume files at once"
            )
            
            if uploaded_files:
                st.success(f"✅ {len(uploaded_files)} resume(s) uploaded successfully!")
                
                # Display uploaded files
                with st.expander("📁 Uploaded Files"):
                    for file in uploaded_files:
                        st.write(f"• {file.name} ({file.size} bytes)")
        
        # Process resumes
        if st.button("🚀 Start Screening Process", type="primary", use_container_width=True):
            if not job_description:
                st.error("❌ Please enter a job description first!")
                return
            
            if not uploaded_files:
                st.error("❌ Please upload at least one resume!")
                return
            
            if not session_name:
                session_name = f"Screening Session - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            
            # Create screening session
            if 'selected_job_posting' in locals():
                job_posting_id = selected_job_posting.id
            else:
                # Create temporary job posting
                temp_job = db_manager.create_job_posting(
                    title=job_title or "Temporary Job",
                    description=job_description,
                    created_by=st.session_state.user['id']
                )
                job_posting_id = temp_job.id
            
            screening_session = db_manager.create_screening_session(
                job_posting_id=job_posting_id,
                session_name=session_name,
                created_by=st.session_state.user['id']
            )
            
            if not screening_session:
                st.error("❌ Failed to create screening session!")
                return
            
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            results = []
            total_files = len(uploaded_files)
            
            for i, uploaded_file in enumerate(uploaded_files):
                status_text.text(f"Processing {uploaded_file.name}...")
                progress_bar.progress((i + 1) / total_files)
                
                try:
                    # Save uploaded file
                    file_path = save_uploaded_file(uploaded_file)
                    
                    # Parse resume
                    resume_text = resume_parser.parse_resume(file_path)
                    
                    if resume_text:
                        # Extract information
                        resume_info = resume_parser.extract_information(resume_text)
                        
                        # Calculate similarity
                        similarity_score = job_matcher.calculate_similarity(
                            job_description, resume_text
                        )
                        
                        # Save to database
                        analysis_data = {
                            'resume_text_preview': resume_text[:500] + "..." if len(resume_text) > 500 else resume_text,
                            'word_count': len(resume_text.split()),
                            'contact_info': resume_info.get('contact', {}),
                            'years_of_experience': resume_info.get('years_of_experience')
                        }
                        
                        db_manager.save_resume_analysis(
                            session_id=screening_session.id,
                            filename=uploaded_file.name,
                            similarity_score=similarity_score,
                            skills=resume_info['skills'],
                            education=resume_info['education'],
                            experience=resume_info['experience'],
                            analysis_data=analysis_data
                        )
                        
                        results.append({
                            'filename': uploaded_file.name,
                            'similarity_score': similarity_score,
                            'resume_info': resume_info,
                            'resume_text': resume_text[:500] + "..." if len(resume_text) > 500 else resume_text
                        })
                    else:
                        st.warning(f"⚠️ Could not extract text from {uploaded_file.name}")
                        
                except Exception as e:
                    st.error(f"❌ Error processing {uploaded_file.name}: {str(e)}")
            
            progress_bar.progress(1.0)
            status_text.text("✅ Processing complete!")
            
            if results:
                # Sort by similarity score
                results.sort(key=lambda x: x['similarity_score'], reverse=True)
                
                # Store results in session state
                st.session_state['screening_results'] = results
                st.session_state['job_description'] = job_description
                st.session_state['session_id'] = screening_session.id
                
                # Display results
                st.header("🏆 Screening Results")
                
                # Summary metrics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Resumes", len(results))
                
                with col2:
                    avg_score = sum(r['similarity_score'] for r in results) / len(results)
                    st.metric("Average Score", f"{avg_score:.1%}")
                
                with col3:
                    high_score_count = sum(1 for r in results if r['similarity_score'] >= 0.7)
                    st.metric("High Match (≥70%)", high_score_count)
                
                with col4:
                    best_score = max(r['similarity_score'] for r in results)
                    st.metric("Best Score", f"{best_score:.1%}")
                
                # Detailed results
                for i, result in enumerate(results):
                    score = result['similarity_score']
                    score_class = "high-score" if score >= 0.7 else "medium-score" if score >= 0.5 else "low-score"
                    
                    with st.container():
                        st.markdown(f"""
                        <div class="resume-card {score_class}">
                            <h4>#{i+1} {result['filename']}</h4>
                            <p><strong>Match Score: {score:.1%}</strong></p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        col_a, col_b = st.columns([2, 1])
                        
                        with col_a:
                            info = result['resume_info']
                            if info['skills']:
                                st.write("**Skills:**", ", ".join(info['skills'][:5]))
                            if info['education']:
                                st.write("**Education:**", ", ".join(info['education'][:3]))
                            if info['experience']:
                                st.write("**Experience:**", ", ".join(info['experience'][:3]))
                        
                        with col_b:
                            if st.button(f"View Details", key=f"details_{i}"):
                                with st.expander(f"📄 {result['filename']} - Full Details", expanded=True):
                                    st.write("**Resume Text Preview:**")
                                    st.text(result['resume_text'])
                                    
                                    st.write("**Extracted Information:**")
                                    st.json(result['resume_info'])
    
    with tab2:
        st.header("📈 Analytics Dashboard")
        
        # Load analytics data from database
        db_stats = db_manager.get_analysis_statistics()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Analyses", db_stats['total_analyses'])
        with col2:
            st.metric("Total Sessions", db_stats['total_sessions'])
        with col3:
            st.metric("Total Jobs", db_stats['total_jobs'])
        with col4:
            st.metric("Average Score", f"{db_stats['average_similarity']:.1%}")
        
        if 'screening_results' in st.session_state:
            results = st.session_state['screening_results']
            
            # Score distribution
            col1, col2 = st.columns(2)
            
            with col1:
                scores = [r['similarity_score'] for r in results]
                fig_hist = px.histogram(
                    x=scores,
                    nbins=10,
                    title="Score Distribution",
                    labels={'x': 'Similarity Score', 'y': 'Number of Resumes'}
                )
                fig_hist.update_layout(showlegend=False)
                st.plotly_chart(fig_hist, use_container_width=True)
            
            with col2:
                # Top candidates
                top_5 = results[:5]
                fig_bar = px.bar(
                    x=[r['similarity_score'] for r in top_5],
                    y=[r['filename'] for r in top_5],
                    orientation='h',
                    title="Top 5 Candidates",
                    labels={'x': 'Similarity Score', 'y': 'Resume'}
                )
                fig_bar.update_layout(yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig_bar, use_container_width=True)
            
            # Export results
            st.subheader("📊 Export Results")
            
            # Prepare data for export
            export_data = []
            for i, result in enumerate(results):
                export_data.append({
                    'Rank': i + 1,
                    'Filename': result['filename'],
                    'Similarity Score': f"{result['similarity_score']:.1%}",
                    'Skills': ", ".join(result['resume_info']['skills'][:5]),
                    'Education': ", ".join(result['resume_info']['education'][:3]),
                    'Experience': ", ".join(result['resume_info']['experience'][:3])
                })
            
            df = pd.DataFrame(export_data)
            
            col1, col2 = st.columns(2)
            with col1:
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV Report",
                    data=csv,
                    file_name=f"smarthire_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            
            with col2:
                st.dataframe(df, use_container_width=True)
        
        else:
            st.info("📊 Run the screening process first to see analytics!")
    
    with tab3:
        st.header("📋 Job Management")
        
        # Job postings management
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📝 Saved Job Postings")
            
            job_postings = db_manager.get_job_postings(limit=20)
            
            if job_postings:
                for job in job_postings:
                    with st.expander(f"📄 {job.title} (ID: {job.id})"):
                        st.write(f"**Created:** {job.created_at}")
                        st.write(f"**Description:**")
                        st.text(job.description[:300] + "..." if len(job.description) > 300 else job.description)
                        
                        # Show screening sessions for this job
                        sessions = [s for s in db_manager.get_screening_sessions() if s.job_posting_id == job.id]
                        if sessions:
                            st.write(f"**Screening Sessions ({len(sessions)}):**")
                            for session in sessions:
                                analyses = db_manager.get_resume_analyses_by_session(session.id)
                                st.write(f"• {session.session_name} - {len(analyses)} resumes analyzed")
            else:
                st.info("No job postings found. Create one in the Resume Screening tab.")
        
        with col2:
            st.subheader("📊 Quick Stats")
            
            # Recent sessions
            recent_sessions = db_manager.get_screening_sessions(limit=5)
            st.write("**Recent Sessions:**")
            for session in recent_sessions:
                analyses = db_manager.get_resume_analyses_by_session(session.id)
                avg_score = sum(json.loads(a.analysis_data).get('similarity_score', 0) for a in analyses) / len(analyses) if analyses else 0
                st.write(f"• {session.session_name}")
                st.write(f"  {len(analyses)} resumes, avg: {avg_score:.1%}")
    
    with tab4:
        st.header("ℹ️ About SmartHire.AI")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎯 Project Overview")
            st.write("""
            SmartHire.AI is an advanced NLP-based resume screening system designed to automate 
            and optimize the recruitment process. Using state-of-the-art machine learning 
            techniques, it provides fair, efficient, and accurate candidate evaluation.
            """)
            
            st.subheader("🔬 Technology Stack")
            st.write("""
            - **NLP Model:** S-BERT (Sentence-BERT)
            - **Similarity Metric:** Cosine Similarity
            - **Frontend:** Streamlit
            - **Database:** SQLite with SQLAlchemy
            - **Text Processing:** spaCy, NLTK
            - **File Parsing:** PyMuPDF, python-docx
            - **Visualization:** Plotly
            """)
        
        with col2:
            st.subheader("✨ Key Features")
            st.write("""
            - **Multi-format Support:** PDF and DOCX resume parsing
            - **Semantic Matching:** Advanced S-BERT embeddings
            - **Database Persistence:** SQLite database for data storage
            - **User Authentication:** Secure login and user management
            - **Bias Reduction:** Objective, algorithm-based scoring
            - **Real-time Processing:** Instant results and rankings
            - **Interactive Dashboard:** Comprehensive analytics
            - **Export Capabilities:** CSV reports for further analysis
            """)
            
            st.subheader("🎓 Academic Information")
            st.write("""
            **Student:** Srivani N (1AT23MC093)
            
            **Guide:** Mr. Yashwanth Reddy V, Assistant Professor
            
            **Institution:** Atria Institute of Technology
            
            **Department:** Master of Computer Applications (MCA)
            """)

def main():
    """Main application entry point."""
    # Check if user is logged in
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if not st.session_state.logged_in:
        login_page()
    else:
        main_app()

if __name__ == "__main__":
    main()
