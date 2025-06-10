"""
Database operations for SmartHire.AI
Handles all database connections and operations using SQLAlchemy
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional, Any
from sqlalchemy import create_engine, Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from config.config import Config
import bcrypt

# Database setup
engine = create_engine(Config.DATABASE_URL, echo=Config.DEBUG)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    """User model for authentication and authorization."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default="user")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    job_postings = relationship("JobPosting", back_populates="creator")
    screening_sessions = relationship("ScreeningSession", back_populates="creator")

class JobPosting(Base):
    """Job posting model."""
    __tablename__ = "job_postings"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    requirements = Column(Text)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    creator = relationship("User", back_populates="job_postings")
    screening_sessions = relationship("ScreeningSession", back_populates="job_posting")

class ScreeningSession(Base):
    """Screening session model."""
    __tablename__ = "screening_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    job_posting_id = Column(Integer, ForeignKey("job_postings.id"))
    session_name = Column(String(200))
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    job_posting = relationship("JobPosting", back_populates="screening_sessions")
    creator = relationship("User", back_populates="screening_sessions")
    resume_analyses = relationship("ResumeAnalysis", back_populates="session")

class ResumeAnalysis(Base):
    """Resume analysis results model."""
    __tablename__ = "resume_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("screening_sessions.id"))
    filename = Column(String(255), nullable=False)
    similarity_score = Column(Float)
    skills_extracted = Column(Text)  # JSON string
    education_extracted = Column(Text)  # JSON string
    experience_extracted = Column(Text)  # JSON string
    analysis_data = Column(Text)  # JSON string for additional data
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    session = relationship("ScreeningSession", back_populates="resume_analyses")

class DatabaseManager:
    """Database manager class for handling all database operations."""
    
    def __init__(self):
        """Initialize database manager."""
        self.engine = engine
        self.SessionLocal = SessionLocal
        
    def create_tables(self):
        """Create all database tables."""
        Base.metadata.create_all(bind=self.engine)
        
    def get_session(self):
        """Get database session."""
        return self.SessionLocal()
    
    def close_session(self, session):
        """Close database session."""
        session.close()
    
    # User operations
    def create_user(self, username: str, email: str, password: str, role: str = "user") -> Optional[User]:
        """Create a new user."""
        session = self.get_session()
        try:
            # Hash password
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            user = User(
                username=username,
                email=email,
                password_hash=password_hash,
                role=role
            )
            
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
            
        except Exception as e:
            session.rollback()
            print(f"Error creating user: {str(e)}")
            return None
        finally:
            self.close_session(session)
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        session = self.get_session()
        try:
            user = session.query(User).filter(User.username == username).first()
            return user
        finally:
            self.close_session(session)
    
    def verify_password(self, username: str, password: str) -> bool:
        """Verify user password."""
        user = self.get_user_by_username(username)
        if user:
            return bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8'))
        return False
    
    # Job posting operations
    def create_job_posting(self, title: str, description: str, requirements: str = None, created_by: int = None) -> Optional[JobPosting]:
        """Create a new job posting."""
        session = self.get_session()
        try:
            job_posting = JobPosting(
                title=title,
                description=description,
                requirements=requirements,
                created_by=created_by
            )
            
            session.add(job_posting)
            session.commit()
            session.refresh(job_posting)
            return job_posting
            
        except Exception as e:
            session.rollback()
            print(f"Error creating job posting: {str(e)}")
            return None
        finally:
            self.close_session(session)
    
    def get_job_postings(self, limit: int = 50) -> List[JobPosting]:
        """Get all job postings."""
        session = self.get_session()
        try:
            job_postings = session.query(JobPosting).order_by(JobPosting.created_at.desc()).limit(limit).all()
            return job_postings
        finally:
            self.close_session(session)
    
    def get_job_posting_by_id(self, job_id: int) -> Optional[JobPosting]:
        """Get job posting by ID."""
        session = self.get_session()
        try:
            job_posting = session.query(JobPosting).filter(JobPosting.id == job_id).first()
            return job_posting
        finally:
            self.close_session(session)
    
    # Screening session operations
    def create_screening_session(self, job_posting_id: int, session_name: str, created_by: int = None) -> Optional[ScreeningSession]:
        """Create a new screening session."""
        session = self.get_session()
        try:
            screening_session = ScreeningSession(
                job_posting_id=job_posting_id,
                session_name=session_name,
                created_by=created_by
            )
            
            session.add(screening_session)
            session.commit()
            session.refresh(screening_session)
            return screening_session
            
        except Exception as e:
            session.rollback()
            print(f"Error creating screening session: {str(e)}")
            return None
        finally:
            self.close_session(session)
    
    def get_screening_sessions(self, limit: int = 50) -> List[ScreeningSession]:
        """Get all screening sessions."""
        session = self.get_session()
        try:
            sessions = session.query(ScreeningSession).order_by(ScreeningSession.created_at.desc()).limit(limit).all()
            return sessions
        finally:
            self.close_session(session)
    
    # Resume analysis operations
    def save_resume_analysis(self, session_id: int, filename: str, similarity_score: float, 
                           skills: List[str], education: List[str], experience: List[str], 
                           analysis_data: Dict[str, Any]) -> Optional[ResumeAnalysis]:
        """Save resume analysis results."""
        session = self.get_session()
        try:
            resume_analysis = ResumeAnalysis(
                session_id=session_id,
                filename=filename,
                similarity_score=similarity_score,
                skills_extracted=json.dumps(skills),
                education_extracted=json.dumps(education),
                experience_extracted=json.dumps(experience),
                analysis_data=json.dumps(analysis_data)
            )
            
            session.add(resume_analysis)
            session.commit()
            session.refresh(resume_analysis)
            return resume_analysis
            
        except Exception as e:
            session.rollback()
            print(f"Error saving resume analysis: {str(e)}")
            return None
        finally:
            self.close_session(session)
    
    def get_resume_analyses_by_session(self, session_id: int) -> List[ResumeAnalysis]:
        """Get all resume analyses for a session."""
        session = self.get_session()
        try:
            analyses = session.query(ResumeAnalysis).filter(
                ResumeAnalysis.session_id == session_id
            ).order_by(ResumeAnalysis.similarity_score.desc()).all()
            return analyses
        finally:
            self.close_session(session)
    
    def get_analysis_statistics(self) -> Dict[str, Any]:
        """Get overall analysis statistics."""
        session = self.get_session()
        try:
            total_analyses = session.query(ResumeAnalysis).count()
            total_sessions = session.query(ScreeningSession).count()
            total_jobs = session.query(JobPosting).count()
            total_users = session.query(User).count()
            
            # Average similarity score
            avg_score = session.query(ResumeAnalysis.similarity_score).all()
            avg_similarity = sum([score[0] for score in avg_score if score[0]]) / len(avg_score) if avg_score else 0
            
            return {
                'total_analyses': total_analyses,
                'total_sessions': total_sessions,
                'total_jobs': total_jobs,
                'total_users': total_users,
                'average_similarity': avg_similarity
            }
        finally:
            self.close_session(session)

# Global database manager instance
db_manager = DatabaseManager()

def init_database():
    """Initialize database with tables."""
    try:
        db_manager.create_tables()
        print("✅ Database initialized successfully")
        
        # Create default admin user if no users exist
        session = db_manager.get_session()
        user_count = session.query(User).count()
        db_manager.close_session(session)
        
        if user_count == 0:
            admin_user = db_manager.create_user(
                username="admin",
                email="admin@smarthire.ai",
                password="admin123",
                role="admin"
            )
            if admin_user:
                print("✅ Default admin user created (username: admin, password: admin123)")
        
        return True
    except Exception as e:
        print(f"❌ Database initialization failed: {str(e)}")
        return False

def get_database_info():
    """Get database information."""
    try:
        stats = db_manager.get_analysis_statistics()
        return {
            'status': 'connected',
            'database_url': Config.DATABASE_URL,
            'statistics': stats
        }
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e)
        }
