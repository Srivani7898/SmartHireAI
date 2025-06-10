import streamlit as st
import pandas as pd
import os
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from resume_parser import ResumeParser
from job_matcher import JobMatcher
from utils import create_directories, save_uploaded_file, format_score

# Page configuration
st.set_page_config(
    page_title="SmartHire.AI - Resume Screening System",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎯 SmartHire.AI</h1>
        <h3>NLP-Based Resume Screening System for Recruitment Automation</h3>
        <p>AI-powered, bias-free, smart resume screening using S-BERT</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize components
    create_directories()
    resume_parser = ResumeParser()
    job_matcher = JobMatcher()
    
    # Sidebar
    with st.sidebar:
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
        - ✅ Bias-free screening
        - ✅ Interactive dashboard
        - ✅ Detailed analytics
        """)
    
    # Main content
    tab1, tab2, tab3 = st.tabs(["🎯 Resume Screening", "📈 Analytics", "ℹ️ About"])
    
    with tab1:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.header("📝 Job Description")
            job_description = st.text_area(
                "Enter the job description:",
                height=300,
                placeholder="Enter detailed job requirements, skills, qualifications, and responsibilities..."
            )
            
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
            
            # Skills analysis
            st.subheader("🔧 Skills Analysis")
            all_skills = []
            for result in results:
                all_skills.extend(result['resume_info']['skills'])
            
            if all_skills:
                from collections import Counter
                skill_counts = Counter(all_skills)
                top_skills = skill_counts.most_common(10)
                
                if top_skills:
                    fig_skills = px.bar(
                        x=[count for skill, count in top_skills],
                        y=[skill for skill, count in top_skills],
                        orientation='h',
                        title="Most Common Skills Across Resumes"
                    )
                    fig_skills.update_layout(yaxis={'categoryorder': 'total ascending'})
                    st.plotly_chart(fig_skills, use_container_width=True)
            
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
            - **Text Processing:** spaCy, NLTK
            - **File Parsing:** PyMuPDF, python-docx
            - **Visualization:** Plotly
            """)
        
        with col2:
            st.subheader("✨ Key Features")
            st.write("""
            - **Multi-format Support:** PDF and DOCX resume parsing
            - **Semantic Matching:** Advanced S-BERT embeddings
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

if __name__ == "__main__":
    main()
