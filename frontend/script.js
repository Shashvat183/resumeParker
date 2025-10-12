// Global variables
let currentResumeData = null;

// DOM elements
const fileInput = document.getElementById('file-input');
const uploadArea = document.getElementById('upload-area');
const loading = document.getElementById('loading');
const results = document.getElementById('results');
const toast = document.getElementById('toast');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    setupFileUpload();
    loadResumeHistory();
});

// Setup file upload functionality
function setupFileUpload() {
    // File input change
    fileInput.addEventListener('change', handleFileSelect);
    
    // Drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('drag-over');
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('drag-over');
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('drag-over');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            handleFileSelect({ target: { files } });
        }
    });
    
    // Click to upload (only when clicking the upload area itself, not child elements)
    uploadArea.addEventListener('click', (e) => {
        // Prevent double triggers when clicking the button
        if (e.target.tagName === 'BUTTON') {
            return;
        }
        fileInput.click();
    });
}

// Handle file selection
function handleFileSelect(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    if (!file.name.toLowerCase().endsWith('.pdf')) {
        showToast('Please select a PDF file.', 'error');
        return;
    }
    
    uploadResume(file);
}

// Upload and analyze resume
async function uploadResume(file) {
    try {
        showLoading();
        
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await fetch('/upload-resume', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        currentResumeData = result.analysis;
        
        displayResults(result.analysis);
        showToast('Resume analyzed successfully!', 'success');
        
        // Reset file input to allow uploading the same file again
        fileInput.value = '';
    } catch (error) {
        console.error('Error uploading resume:', error);
        showToast('Error analyzing resume. Please try again.', 'error');
    } finally {
        hideLoading();
    }
}

// Display analysis results
function displayResults(analysis) {
    // Show results section
    results.classList.remove('hidden');
    
    // Update rating
    const rating = analysis.resume_rating || 0;
    document.getElementById('resume-rating').textContent = rating.toFixed(1);
    const ratingFill = document.getElementById('rating-fill');
    ratingFill.style.width = `${(rating / 10) * 100}%`;
    
    // Personal Information
    displayPersonalInfo(analysis);
    
    // Skills
    displaySkills('core-skills', analysis.core_skills || []);
    displaySkills('soft-skills', analysis.soft_skills || []);
    
    // Work Experience
    displayWorkExperience(analysis.work_experience || []);
    
    // Education
    displayEducation(analysis.education || []);
    
    // Projects
    displayProjects(analysis.projects || []);
    
    // AI Analysis
    displayAnalysis(analysis);
    
    // Scroll to results
    results.scrollIntoView({ behavior: 'smooth' });
}

// Display personal information
function displayPersonalInfo(analysis) {
    const container = document.getElementById('personal-info');
    const personalInfo = [
        { label: 'Name', value: analysis.name, icon: '👤' },
        { label: 'Email', value: analysis.email, icon: '📧' },
        { label: 'Phone', value: analysis.phone, icon: '📱' },
        { label: 'Address', value: analysis.address, icon: '🏠' },
        { label: 'LinkedIn', value: analysis.linkedin, icon: '💼' },
        { label: 'GitHub', value: analysis.github, icon: '🐱' },
        { label: 'Website', value: analysis.website, icon: '🌐' }
    ];
    
    container.innerHTML = personalInfo
        .filter(item => item.value)
        .map(item => `
            <div class="info-item">
                <span class="info-icon">${item.icon}</span>
                <span class="info-label">${item.label}:</span>
                <span class="info-value">${item.value}</span>
            </div>
        `).join('');
}

// Display skills
function displaySkills(containerId, skills) {
    const container = document.getElementById(containerId);
    if (skills.length === 0) {
        container.innerHTML = '<p class="text-muted">No skills found</p>';
        return;
    }
    
    container.innerHTML = skills
        .map(skill => `<span class="skill-tag">${skill}</span>`)
        .join('');
}

// Display work experience
function displayWorkExperience(experiences) {
    const container = document.getElementById('work-experience');
    
    if (experiences.length === 0) {
        container.innerHTML = '<p class="text-muted">No work experience found</p>';
        return;
    }
    
    container.innerHTML = experiences
        .map(exp => `
            <div class="experience-item">
                <div class="experience-header">
                    <div>
                        <div class="job-title">${exp.position || 'Position not specified'}</div>
                        <div class="company">${exp.company || 'Company not specified'}</div>
                    </div>
                    <div class="duration">${exp.duration || ''}</div>
                </div>
                ${exp.location ? `<div class="location">📍 ${exp.location}</div>` : ''}
                <div class="job-description">
                    <ul>
                        ${(exp.description || []).map(desc => `<li>${desc}</li>`).join('')}
                    </ul>
                </div>
                ${exp.technologies && exp.technologies.length > 0 ? `
                    <div class="technologies">
                        ${exp.technologies.map(tech => `<span class="tech-tag">${tech}</span>`).join('')}
                    </div>
                ` : ''}
            </div>
        `).join('');
}

// Display education
function displayEducation(education) {
    const container = document.getElementById('education');
    
    if (education.length === 0) {
        container.innerHTML = '<p class="text-muted">No education found</p>';
        return;
    }
    
    container.innerHTML = education
        .map(edu => `
            <div class="education-item">
                <div class="education-degree">${edu.degree || ''}</div>
                <div class="education-field">${edu.field_of_study || ''}</div>
                <div class="education-institution">${edu.institution || ''}</div>
                <div class="education-date">${edu.graduation_date || ''}</div>
                ${edu.gpa ? `<div class="education-gpa">GPA: ${edu.gpa}</div>` : ''}
                ${edu.location ? `<div class="education-location">📍 ${edu.location}</div>` : ''}
            </div>
        `).join('');
}

// Display projects
function displayProjects(projects) {
    const container = document.getElementById('projects');
    
    if (projects.length === 0) {
        container.innerHTML = '<p class="text-muted">No projects found</p>';
        return;
    }
    
    container.innerHTML = projects
        .map(project => `
            <div class="project-item">
                <div class="project-name">${project.name || 'Untitled Project'}</div>
                <div class="project-description">${project.description || ''}</div>
                ${project.technologies && project.technologies.length > 0 ? `
                    <div class="project-technologies">
                        ${project.technologies.map(tech => `<span class="tech-tag">${tech}</span>`).join('')}
                    </div>
                ` : ''}
                ${project.url ? `<div class="project-url"><a href="${project.url}" target="_blank">🔗 View Project</a></div>` : ''}
                ${project.duration ? `<div class="project-duration">⏱️ ${project.duration}</div>` : ''}
            </div>
        `).join('');
}

// Display AI analysis
function displayAnalysis(analysis) {
    document.getElementById('strengths').innerHTML = formatText(analysis.strengths || 'No strengths identified');
    document.getElementById('improvement-areas').innerHTML = formatText(analysis.improvement_areas || 'No improvement areas identified');
    document.getElementById('upskill-suggestions').innerHTML = formatText(analysis.upskill_suggestions || 'No upskilling suggestions available');
}

// Format text with line breaks
function formatText(text) {
    return text.replace(/\n/g, '<br>');
}

// Tab functionality
function openTab(event, tabName) {
    // Hide all tab contents
    const tabContents = document.querySelectorAll('.tab-content');
    tabContents.forEach(tab => tab.classList.remove('active'));
    
    // Remove active class from all tab buttons
    const tabButtons = document.querySelectorAll('.tab-button');
    tabButtons.forEach(btn => btn.classList.remove('active'));
    
    // Show selected tab and mark button as active
    document.getElementById(tabName).classList.add('active');
    event.currentTarget.classList.add('active');
    
    // Load resume history when switching to history tab
    if (tabName === 'history-tab') {
        loadResumeHistory();
    }
}

// Load resume history
async function loadResumeHistory() {
    try {
        const response = await fetch('/resumes');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const resumes = await response.json();
        displayResumeHistory(resumes);
        
    } catch (error) {
        console.error('Error loading resume history:', error);
        showToast('Error loading resume history', 'error');
    }
}

// Display resume history in table
function displayResumeHistory(resumes) {
    const tbody = document.getElementById('resumes-table-body');
    
    if (resumes.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="6" class="text-center">
                    No resumes uploaded yet
                </td>
            </tr>
        `;
        return;
    }
    
    tbody.innerHTML = resumes
        .map(resume => `
            <tr>
                <td>${resume.filename || 'Unknown'}</td>
                <td>${resume.name || 'N/A'}</td>
                <td>${resume.email || 'N/A'}</td>
                <td>${formatDate(resume.upload_date)}</td>
                <td>${resume.resume_rating ? resume.resume_rating.toFixed(1) + '/10' : 'N/A'}</td>
                <td>
                    <button class="action-btn btn-view" onclick="viewResumeDetails(${resume.id})">
                        👁️ Details
                    </button>
                    <button class="action-btn btn-delete" onclick="deleteResume(${resume.id})">
                        🗑️ Delete
                    </button>
                </td>
            </tr>
        `).join('');
}

// View resume details in modal
async function viewResumeDetails(resumeId) {
    try {
        const response = await fetch(`/resume/${resumeId}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const resume = await response.json();
        showModal(resume);
        
    } catch (error) {
        console.error('Error loading resume details:', error);
        showToast('Error loading resume details', 'error');
    }
}

// Show modal with resume details
function showModal(resumeData) {
    const modal = document.getElementById('details-modal');
    const modalBody = document.getElementById('modal-body');
    
    // Create the same results display but for modal
    modalBody.innerHTML = `
        <div class="modal-results">
            <div class="rating mb-20">
                <span>Overall Rating: </span>
                <span class="rating-score">${(resumeData.resume_rating || 0).toFixed(1)}</span>/10
                <div class="rating-bar">
                    <div class="rating-fill" style="width: ${((resumeData.resume_rating || 0) / 10) * 100}%"></div>
                </div>
            </div>
            
            <div class="results-grid">
                <div class="info-card">
                    <h3>👤 Personal Information</h3>
                    <div id="modal-personal-info" class="info-content"></div>
                </div>
                
                <div class="info-card">
                    <h3>🔧 Technical Skills</h3>
                    <div id="modal-core-skills" class="skills-list"></div>
                </div>
                
                <div class="info-card">
                    <h3>🤝 Soft Skills</h3>
                    <div id="modal-soft-skills" class="skills-list"></div>
                </div>
                
                <div class="info-card full-width">
                    <h3>💼 Work Experience</h3>
                    <div id="modal-work-experience" class="experience-list"></div>
                </div>
                
                <div class="info-card">
                    <h3>🎓 Education</h3>
                    <div id="modal-education" class="education-list"></div>
                </div>
                
                <div class="info-card">
                    <h3>🚀 Projects</h3>
                    <div id="modal-projects" class="projects-list"></div>
                </div>
                
                <div class="info-card full-width">
                    <h3>🔍 AI Analysis & Recommendations</h3>
                    
                    <div class="analysis-section">
                        <h4>💪 Strengths</h4>
                        <div id="modal-strengths" class="analysis-content"></div>
                    </div>
                    
                    <div class="analysis-section">
                        <h4>📈 Areas for Improvement</h4>
                        <div id="modal-improvement-areas" class="analysis-content"></div>
                    </div>
                    
                    <div class="analysis-section">
                        <h4>🎯 Upskilling Suggestions</h4>
                        <div id="modal-upskill-suggestions" class="analysis-content"></div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Populate modal with data using modified functions
    displayModalPersonalInfo(resumeData);
    displayModalSkills('modal-core-skills', resumeData.core_skills || []);
    displayModalSkills('modal-soft-skills', resumeData.soft_skills || []);
    displayModalWorkExperience(resumeData.work_experience || []);
    displayModalEducation(resumeData.education || []);
    displayModalProjects(resumeData.projects || []);
    displayModalAnalysis(resumeData);
    
    modal.style.display = 'block';
}

// Modal-specific display functions (similar to main ones but with modal- prefix)
function displayModalPersonalInfo(analysis) {
    const container = document.getElementById('modal-personal-info');
    const personalInfo = [
        { label: 'Name', value: analysis.name, icon: '👤' },
        { label: 'Email', value: analysis.email, icon: '📧' },
        { label: 'Phone', value: analysis.phone, icon: '📱' },
        { label: 'Address', value: analysis.address, icon: '🏠' },
        { label: 'LinkedIn', value: analysis.linkedin, icon: '💼' },
        { label: 'GitHub', value: analysis.github, icon: '🐱' },
        { label: 'Website', value: analysis.website, icon: '🌐' }
    ];
    
    container.innerHTML = personalInfo
        .filter(item => item.value)
        .map(item => `
            <div class="info-item">
                <span class="info-icon">${item.icon}</span>
                <span class="info-label">${item.label}:</span>
                <span class="info-value">${item.value}</span>
            </div>
        `).join('');
}

function displayModalSkills(containerId, skills) {
    const container = document.getElementById(containerId);
    if (skills.length === 0) {
        container.innerHTML = '<p class="text-muted">No skills found</p>';
        return;
    }
    
    container.innerHTML = skills
        .map(skill => `<span class="skill-tag">${skill}</span>`)
        .join('');
}

function displayModalWorkExperience(experiences) {
    const container = document.getElementById('modal-work-experience');
    
    if (experiences.length === 0) {
        container.innerHTML = '<p class="text-muted">No work experience found</p>';
        return;
    }
    
    container.innerHTML = experiences
        .map(exp => `
            <div class="experience-item">
                <div class="experience-header">
                    <div>
                        <div class="job-title">${exp.position || 'Position not specified'}</div>
                        <div class="company">${exp.company || 'Company not specified'}</div>
                    </div>
                    <div class="duration">${exp.duration || ''}</div>
                </div>
                ${exp.location ? `<div class="location">📍 ${exp.location}</div>` : ''}
                <div class="job-description">
                    <ul>
                        ${(exp.description || []).map(desc => `<li>${desc}</li>`).join('')}
                    </ul>
                </div>
                ${exp.technologies && exp.technologies.length > 0 ? `
                    <div class="technologies">
                        ${exp.technologies.map(tech => `<span class="tech-tag">${tech}</span>`).join('')}
                    </div>
                ` : ''}
            </div>
        `).join('');
}

function displayModalEducation(education) {
    const container = document.getElementById('modal-education');
    
    if (education.length === 0) {
        container.innerHTML = '<p class="text-muted">No education found</p>';
        return;
    }
    
    container.innerHTML = education
        .map(edu => `
            <div class="education-item">
                <div class="education-degree">${edu.degree || ''}</div>
                <div class="education-field">${edu.field_of_study || ''}</div>
                <div class="education-institution">${edu.institution || ''}</div>
                <div class="education-date">${edu.graduation_date || ''}</div>
                ${edu.gpa ? `<div class="education-gpa">GPA: ${edu.gpa}</div>` : ''}
                ${edu.location ? `<div class="education-location">📍 ${edu.location}</div>` : ''}
            </div>
        `).join('');
}

function displayModalProjects(projects) {
    const container = document.getElementById('modal-projects');
    
    if (projects.length === 0) {
        container.innerHTML = '<p class="text-muted">No projects found</p>';
        return;
    }
    
    container.innerHTML = projects
        .map(project => `
            <div class="project-item">
                <div class="project-name">${project.name || 'Untitled Project'}</div>
                <div class="project-description">${project.description || ''}</div>
                ${project.technologies && project.technologies.length > 0 ? `
                    <div class="project-technologies">
                        ${project.technologies.map(tech => `<span class="tech-tag">${tech}</span>`).join('')}
                    </div>
                ` : ''}
                ${project.url ? `<div class="project-url"><a href="${project.url}" target="_blank">🔗 View Project</a></div>` : ''}
                ${project.duration ? `<div class="project-duration">⏱️ ${project.duration}</div>` : ''}
            </div>
        `).join('');
}

function displayModalAnalysis(analysis) {
    document.getElementById('modal-strengths').innerHTML = formatText(analysis.strengths || 'No strengths identified');
    document.getElementById('modal-improvement-areas').innerHTML = formatText(analysis.improvement_areas || 'No improvement areas identified');
    document.getElementById('modal-upskill-suggestions').innerHTML = formatText(analysis.upskill_suggestions || 'No upskilling suggestions available');
}

// Close modal
function closeModal() {
    document.getElementById('details-modal').style.display = 'none';
}

// Delete resume
async function deleteResume(resumeId) {
    if (!confirm('Are you sure you want to delete this resume?')) {
        return;
    }
    
    try {
        const response = await fetch(`/resume/${resumeId}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        showToast('Resume deleted successfully', 'success');
        loadResumeHistory(); // Refresh the table
        
    } catch (error) {
        console.error('Error deleting resume:', error);
        showToast('Error deleting resume', 'error');
    }
}

// Utility functions
function showLoading() {
    uploadArea.style.display = 'none';
    loading.classList.remove('hidden');
    results.classList.add('hidden');
}

function hideLoading() {
    loading.classList.add('hidden');
    uploadArea.style.display = 'block';
}

function showToast(message, type = 'info') {
    toast.textContent = message;
    toast.className = `toast show ${type}`;
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 4000);
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('details-modal');
    if (event.target === modal) {
        closeModal();
    }
}
