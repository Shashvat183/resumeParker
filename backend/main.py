from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session
from typing import List
import os
import uvicorn

# Import local modules
from database import get_db, Resume
from resume_parser import ResumeParser
from schemas import ResumeAnalysis, ResumeListItem, ResumeUploadResponse

# Initialize FastAPI app
app = FastAPI(
    title="AI Resume Parser",
    description="An intelligent resume parsing application with AI-powered analysis",
    version="1.0.0"
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="../frontend"), name="static")

# Initialize resume parser
resume_parser = ResumeParser()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main HTML page"""
    try:
        with open("../frontend/index.html", "r", encoding="utf-8") as file:
            return HTMLResponse(content=file.read(), status_code=200)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Frontend not found</h1>", status_code=404)

@app.post("/upload-resume", response_model=ResumeUploadResponse)
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload and analyze a resume PDF"""
    try:
        # Validate file type
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        # Analyze the resume
        analysis_data = resume_parser.analyze_resume(file.file)
        
        # Format data for database
        db_data = resume_parser.format_for_database(analysis_data, file.filename)
        
        # Save to database
        db_resume = Resume(**db_data)
        db.add(db_resume)
        db.commit()
        db.refresh(db_resume)
        
        # Prepare response
        personal_info = analysis_data.get('personal_info', {})
        skills = analysis_data.get('skills', {})
        analysis = analysis_data.get('analysis', {})
        
        response_data = ResumeAnalysis(
            # Personal Information
            name=personal_info.get('name'),
            email=personal_info.get('email'),
            phone=personal_info.get('phone'),
            address=personal_info.get('address'),
            linkedin=personal_info.get('linkedin'),
            github=personal_info.get('github'),
            website=personal_info.get('website'),
            
            # Skills
            core_skills=skills.get('core_skills', []),
            soft_skills=skills.get('soft_skills', []),
            certifications=skills.get('certifications', []),
            languages=skills.get('languages', []),
            
            # Experience and Education
            work_experience=analysis_data.get('work_experience', []),
            education=analysis_data.get('education', []),
            projects=analysis_data.get('projects', []),
            achievements=analysis_data.get('achievements', []),
            
            # AI Analysis
            resume_rating=analysis.get('resume_rating', 0),
            improvement_areas=analysis.get('improvement_areas', ''),
            upskill_suggestions=analysis.get('upskill_suggestions', ''),
            strengths=analysis.get('strengths', ''),
            missing_sections=analysis.get('missing_sections', [])
        )
        
        return ResumeUploadResponse(
            message="Resume uploaded and analyzed successfully",
            resume_id=db_resume.id,
            analysis=response_data
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error processing resume: {str(e)}")

@app.get("/resumes", response_model=List[ResumeListItem])
async def get_all_resumes(db: Session = Depends(get_db)):
    """Get all uploaded resumes for table view"""
    try:
        resumes = db.query(Resume).order_by(Resume.upload_date.desc()).all()
        
        return [
            ResumeListItem(
                id=resume.id,
                filename=resume.filename,
                name=resume.name,
                email=resume.email,
                phone=resume.phone,
                upload_date=resume.upload_date,
                resume_rating=resume.resume_rating
            )
            for resume in resumes
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching resumes: {str(e)}")

@app.get("/resume/{resume_id}", response_model=ResumeAnalysis)
async def get_resume_details(resume_id: int, db: Session = Depends(get_db)):
    """Get detailed analysis of a specific resume"""
    try:
        resume = db.query(Resume).filter(Resume.id == resume_id).first()
        
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found")
        
        return ResumeAnalysis(
            # Personal Information
            name=resume.name,
            email=resume.email,
            phone=resume.phone,
            address=resume.address,
            linkedin=resume.linkedin,
            github=resume.github,
            website=resume.website,
            
            # Skills
            core_skills=resume.core_skills or [],
            soft_skills=resume.soft_skills or [],
            certifications=resume.certifications or [],
            languages=resume.languages or [],
            
            # Experience and Education
            work_experience=resume.work_experience or [],
            education=resume.education or [],
            projects=resume.projects or [],
            achievements=resume.achievements or [],
            
            # AI Analysis
            resume_rating=resume.resume_rating or 0,
            improvement_areas=resume.improvement_areas or '',
            upskill_suggestions=resume.upskill_suggestions or '',
            strengths=resume.strengths or '',
            missing_sections=resume.missing_sections or []
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching resume details: {str(e)}")

@app.delete("/resume/{resume_id}")
async def delete_resume(resume_id: int, db: Session = Depends(get_db)):
    """Delete a specific resume"""
    try:
        resume = db.query(Resume).filter(Resume.id == resume_id).first()
        
        if not resume:
            raise HTTPException(status_code=404, detail="Resume not found")
        
        db.delete(resume)
        db.commit()
        
        return {"message": "Resume deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting resume: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "AI Resume Parser is running"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
