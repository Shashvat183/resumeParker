import json
import os
from typing import Dict, Any
from pypdf import PdfReader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage
from dotenv import load_dotenv

load_dotenv()

class ResumeParser:
    def __init__(self):
        """Initialize the resume parser with Gemini AI"""
        api_key = os.getenv("GEMINI_API_KEY")
        
        if api_key and api_key != "your_gemini_api_key_here":
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-pro",
                google_api_key=api_key,
                temperature=0.1
            )
            self.use_mock = False
        else:
            print("⚠️  Using mock AI analysis (no valid Gemini API key found)")
            self.llm = None
            self.use_mock = True
    
    def extract_text_from_pdf(self, pdf_file) -> str:
        """Extract text from PDF file"""
        try:
            reader = PdfReader(pdf_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    def create_analysis_prompt(self, resume_text: str) -> str:
        """Create a comprehensive prompt for resume analysis"""
        prompt = f"""
        Analyze the following resume and extract comprehensive information in JSON format. Be thorough and accurate.
        
        Resume Text:
        {resume_text}
        
        Please extract the following information and return it as a valid JSON object:
        
        {{
            "personal_info": {{
                "name": "Full name",
                "email": "Email address",
                "phone": "Phone number",
                "address": "Full address",
                "linkedin": "LinkedIn profile URL",
                "github": "GitHub profile URL",
                "website": "Personal website URL"
            }},
            "skills": {{
                "core_skills": ["Technical skills array"],
                "soft_skills": ["Soft skills array"],
                "certifications": ["Certifications array"],
                "languages": [
                    {{"language": "Language name", "proficiency": "Proficiency level"}}
                ]
            }},
            "work_experience": [
                {{
                    "company": "Company name",
                    "position": "Job title",
                    "duration": "Employment duration",
                    "location": "Work location",
                    "description": ["Bullet points of responsibilities"],
                    "technologies": ["Technologies used"]
                }}
            ],
            "education": [
                {{
                    "institution": "School/University name",
                    "degree": "Degree type",
                    "field_of_study": "Major/Field",
                    "graduation_date": "Graduation date",
                    "gpa": "GPA if mentioned",
                    "location": "Institution location"
                }}
            ],
            "projects": [
                {{
                    "name": "Project name",
                    "description": "Project description",
                    "technologies": ["Technologies used"],
                    "duration": "Project duration",
                    "url": "Project URL if available"
                }}
            ],
            "achievements": ["List of achievements, awards, publications"],
            "analysis": {{
                "resume_rating": 8.5,
                "strengths": "Key strengths of this resume",
                "improvement_areas": "Areas that need improvement with specific suggestions",
                "upskill_suggestions": "Detailed suggestions for skills to learn and career growth",
                "missing_sections": ["List of commonly expected resume sections that are missing"]
            }}
        }}
        
        Instructions:
        1. Extract all available information accurately
        2. For missing information, use null or empty arrays appropriately
        3. Rate the resume out of 10 based on completeness, clarity, and professional presentation
        4. Provide specific, actionable improvement suggestions
        5. Suggest relevant upskilling opportunities based on the person's background
        6. Identify missing resume sections like summary, certifications, etc.
        7. Return only valid JSON without any additional text or formatting
        """
        return prompt
    
    def get_mock_analysis(self, resume_text: str) -> Dict[str, Any]:
        """Generate mock analysis when API key is not available"""
        # Basic text analysis for mock data
        words = resume_text.lower().split()
        
        # Extract potential email
        email = None
        for word in words:
            if '@' in word and '.' in word:
                email = word.strip('.,()[]')
                break
        
        # Extract potential skills (basic keyword matching)
        tech_skills = []
        skill_keywords = ['python', 'javascript', 'java', 'react', 'node', 'sql', 'git', 'aws', 'docker', 'kubernetes']
        for skill in skill_keywords:
            if skill in resume_text.lower():
                tech_skills.append(skill.capitalize())
        
        return {
            'personal_info': {
                'name': 'Sample Name (Mock)',
                'email': email or 'sample@email.com',
                'phone': '+1-234-567-8900',
                'address': 'Sample Address',
                'linkedin': None,
                'github': None,
                'website': None
            },
            'skills': {
                'core_skills': tech_skills or ['Python', 'JavaScript', 'SQL'],
                'soft_skills': ['Communication', 'Problem Solving', 'Team Work'],
                'certifications': [],
                'languages': [{'language': 'English', 'proficiency': 'Native'}]
            },
            'work_experience': [
                {
                    'company': 'Sample Company',
                    'position': 'Software Developer',
                    'duration': '2022 - Present',
                    'location': 'Remote',
                    'description': ['Developed applications', 'Collaborated with team'],
                    'technologies': tech_skills[:3] or ['Python', 'React']
                }
            ],
            'education': [
                {
                    'institution': 'Sample University',
                    'degree': 'Bachelor of Science',
                    'field_of_study': 'Computer Science',
                    'graduation_date': '2022',
                    'gpa': None,
                    'location': 'Sample City'
                }
            ],
            'projects': [
                {
                    'name': 'Sample Project',
                    'description': 'A sample project for demonstration',
                    'technologies': tech_skills[:2] or ['Python'],
                    'duration': '3 months',
                    'url': None
                }
            ],
            'achievements': ['Mock Achievement 1', 'Mock Achievement 2'],
            'analysis': {
                'resume_rating': 7.5,
                'strengths': 'This is a mock analysis. The resume shows technical skills and experience.',
                'improvement_areas': 'Mock suggestion: Add more quantifiable achievements and specific project outcomes.',
                'upskill_suggestions': 'Mock suggestion: Consider learning cloud technologies like AWS or Azure.',
                'missing_sections': ['Professional Summary', 'Certifications']
            },
            'raw_text': resume_text
        }
    
    def analyze_resume(self, pdf_file) -> Dict[str, Any]:
        """Analyze resume and return structured data"""
        try:
            # Extract text from PDF
            resume_text = self.extract_text_from_pdf(pdf_file)
            
            if not resume_text.strip():
                raise ValueError("No text could be extracted from the PDF")
            
            # Use mock analysis if no API key
            if self.use_mock:
                return self.get_mock_analysis(resume_text)
            
            # Create analysis prompt
            prompt = self.create_analysis_prompt(resume_text)
            
            # Get AI analysis
            message = HumanMessage(content=prompt)
            response = self.llm([message])
            
            # Parse JSON response
            try:
                analysis_data = json.loads(response.content)
            except json.JSONDecodeError:
                # If JSON parsing fails, try to extract JSON from response
                content = response.content.strip()
                if content.startswith('```json'):
                    content = content[7:-3]  # Remove ```json and ```
                elif content.startswith('```'):
                    content = content[3:-3]  # Remove ```
                
                analysis_data = json.loads(content)
            
            # Add raw text to the analysis
            analysis_data['raw_text'] = resume_text
            
            return analysis_data
            
        except Exception as e:
            raise Exception(f"Error analyzing resume: {str(e)}")
    
    def format_for_database(self, analysis_data: Dict[str, Any], filename: str) -> Dict[str, Any]:
        """Format analysis data for database storage"""
        personal_info = analysis_data.get('personal_info', {})
        skills = analysis_data.get('skills', {})
        analysis = analysis_data.get('analysis', {})
        
        return {
            'filename': filename,
            'name': personal_info.get('name'),
            'email': personal_info.get('email'),
            'phone': personal_info.get('phone'),
            'address': personal_info.get('address'),
            'linkedin': personal_info.get('linkedin'),
            'github': personal_info.get('github'),
            'website': personal_info.get('website'),
            'core_skills': skills.get('core_skills', []),
            'soft_skills': skills.get('soft_skills', []),
            'certifications': skills.get('certifications', []),
            'languages': skills.get('languages', []),
            'work_experience': analysis_data.get('work_experience', []),
            'education': analysis_data.get('education', []),
            'projects': analysis_data.get('projects', []),
            'achievements': analysis_data.get('achievements', []),
            'resume_rating': analysis.get('resume_rating', 0),
            'improvement_areas': analysis.get('improvement_areas', ''),
            'upskill_suggestions': analysis.get('upskill_suggestions', ''),
            'strengths': analysis.get('strengths', ''),
            'missing_sections': analysis.get('missing_sections', []),
            'raw_text': analysis_data.get('raw_text', ''),
            'structured_data': analysis_data
        }
