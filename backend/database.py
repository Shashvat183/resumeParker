from sqlalchemy import create_engine, Column, Integer, String, Text, JSON, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://username:password@localhost:5432/resume_parser_db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Resume(Base):
    __tablename__ = "resumes"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    upload_date = Column(DateTime, default=datetime.utcnow)
    
    # Personal Information
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    address = Column(Text)
    linkedin = Column(String)
    github = Column(String)
    website = Column(String)
    
    # Skills
    core_skills = Column(JSON)  # Array of technical skills
    soft_skills = Column(JSON)  # Array of soft skills
    certifications = Column(JSON)  # Array of certifications
    languages = Column(JSON)  # Array of languages with proficiency
    
    # Experience and Education
    work_experience = Column(JSON)  # Array of work experience objects
    education = Column(JSON)  # Array of education objects
    projects = Column(JSON)  # Array of project objects
    achievements = Column(JSON)  # Array of achievements/awards
    
    # AI Analysis Results
    resume_rating = Column(Float)  # Rating out of 10
    improvement_areas = Column(Text)  # Areas needing improvement
    upskill_suggestions = Column(Text)  # Skills to learn
    strengths = Column(Text)  # Resume strengths
    missing_sections = Column(JSON)  # Missing resume sections
    
    # Raw Data
    raw_text = Column(Text)  # Raw extracted text from PDF
    structured_data = Column(JSON)  # Complete structured data from AI

def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create tables when module is imported
create_tables()
