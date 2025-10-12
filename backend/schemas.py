from pydantic import BaseModel
from typing import List, Optional, Any
from datetime import datetime

class WorkExperience(BaseModel):
    """Work experience entry"""
    company: str
    position: str
    duration: str
    location: Optional[str] = None
    description: List[str]
    technologies: List[str] = []

class Education(BaseModel):
    """Education entry"""
    institution: str
    degree: str
    field_of_study: str
    graduation_date: Optional[str] = None
    gpa: Optional[str] = None
    location: Optional[str] = None

class Project(BaseModel):
    """Project entry"""
    name: str
    description: str
    technologies: List[str]
    duration: Optional[str] = None
    url: Optional[str] = None

class ResumeAnalysis(BaseModel):
    """Complete resume analysis response"""
    # Personal Information
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    website: Optional[str] = None
    
    # Skills
    core_skills: List[str] = []
    soft_skills: List[str] = []
    certifications: List[str] = []
    languages: List[dict] = []  # [{"language": "English", "proficiency": "Native"}]
    
    # Experience and Education
    work_experience: List[WorkExperience] = []
    education: List[Education] = []
    projects: List[Project] = []
    achievements: List[str] = []
    
    # AI Analysis
    resume_rating: float
    improvement_areas: str
    upskill_suggestions: str
    strengths: str
    missing_sections: List[str] = []

class ResumeListItem(BaseModel):
    """Resume list item for table view"""
    id: int
    filename: str
    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    upload_date: datetime
    resume_rating: Optional[float]

class ResumeUploadResponse(BaseModel):
    """Response after uploading a resume"""
    message: str
    resume_id: int
    analysis: ResumeAnalysis

class Config:
    from_attributes = True
