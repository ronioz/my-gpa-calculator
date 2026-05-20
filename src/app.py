from pathlib import Path
import json

from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from src.classes import Course, Courses
from src.storage import CourseStorage
from src.visualization import (
    generate_gpa_plot, 
    generate_credits_plot, 
    generate_term_specific_plot, 
)

# ==========================================
# 1. SETUP & INITIALIZATION
# ==========================================
app = FastAPI(title="Hungarian University GPA API", description="API and Dashboard for managing courses and calculating GPA.")

BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = BASE_DIR.parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))

# Initialize the storage manager and load existing data
my_courses = Courses()
storage = CourseStorage()

# Load the dictionary of courses from storage, and attach it to the Courses object
my_courses.courses = storage.load()

# Pydantic Model for API Input Validation
class CourseInput(BaseModel):
    course_name: str
    credit: int
    score: int
    term_id: int

# ==========================================
# 2. DASHBOARD ROUTES (HTML & Forms)
# ==========================================

@app.get("/dashboard", response_class=HTMLResponse, tags=["Dashboard"])
def view_dashboard(request: Request):
    """Renders the main HTML dashboard."""
    my_courses.courses = storage.load()
    total_score, total_credits = my_courses.calculateTotal()
    cumulative_gpa = my_courses.calculateGPA()

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "cumulative_gpa": f"{cumulative_gpa:.2f}",
            "total_credits": total_credits,
            "total_score": total_score,
            "courses": my_courses.courses.values(),
        }
    )

@app.post("/add-course")
async def add_course(raw_input: str = Form(...)):
    """Parses input, adds the course, saves to JSON, and reloads memory."""
    try:
        parts = raw_input.split()
        term = int(parts[-1])
        score = int(parts[-2])
        credit = int(parts[-3])
        name = " ".join(parts[:-3])
        
        new_course = Course(name, credit, score, term)
        my_courses.addCourse(new_course)
        
        # 1. Save to disk
        storage.save(my_courses.courses)
        # 2. Reload into memory immediately to ensure synchronization
        my_courses.courses = storage.load()
            
    except Exception as e:
        print(f"Error adding course: {e}")
        
    return RedirectResponse(url="/dashboard", status_code=303)

@app.post("/delete-course/{course_name}")
async def delete_course(course_name: str):
    """Deletes a course, saves, and reloads memory."""
    if course_name in my_courses.courses:
        my_courses.removeCourse(course_name)
        
        # 1. Save to disk
        storage.save(my_courses.courses)
        # 2. Reload into memory immediately
        my_courses.courses = storage.load()
            
    return RedirectResponse(url="/dashboard", status_code=303)

@app.post("/edit-course")
async def edit_course(
    course_name: str = Form(...), 
    new_credit: int = Form(...), 
    new_score: int = Form(...)
):
    storage = CourseStorage()
    courses = storage.load()
    if course_name in courses:
        courses[course_name].changeCredit(new_credit)
        courses[course_name].changeScore(new_score)
        storage.save(courses)

    return RedirectResponse(url="/dashboard", status_code=303)

@app.post("/edit/{course_name}")
async def edit_course(course_name: str, new_credit: int, new_score: int, new_term: int):
    courses_dict = storage.load() # Load existing state
    
    if course_name in courses_dict:
        course = courses_dict[course_name]
        
        # Use the validation methods you wrote in classes.py
        course.changeTerm(new_term)
        course.changeCredit(new_credit)
        course.changeScore(new_score)
        
        # Persist the change
        storage.save(courses_dict)
        return {"status": "success"}
    
    return {"status": "error", "message": "Course not found"}

# ==========================================
# 3. RAW API ENDPOINTS (JSON)
# ==========================================

@app.get("/", tags=["General"])
def read_root():
    return {"message": "Welcome to the Hungarian University GPA API. Visit /dashboard for the UI, or /docs for the API Swagger."}

@app.get("/courses", tags=["Courses"])
def get_all_courses():
    """Retrieve all saved courses."""
    return [course.to_dict() for course in my_courses.courses.values()]

@app.post("/courses", tags=["Courses"])
def add_new_course_api(course_in: CourseInput):
    """Add a new course to the database via JSON."""
    if course_in.score < 1 or course_in.score > 5:
        raise HTTPException(status_code=400, detail="Score must be between 1 and 5.")
    if course_in.credit <= 0:
        raise HTTPException(status_code=400, detail="Credits must be greater than 0.")
    if course_in.term_id <= 0:
        raise HTTPException(status_code=400, detail="Term ID must be a positive integer.")
    
    if course_in.course_name in my_courses.courses:
        raise HTTPException(status_code=400, detail=f"Course '{course_in.course_name}' already exists!")

    new_course = Course(
        course_in.course_name, 
        course_in.credit, 
        course_in.score, 
        course_in.term_id
    )
    my_courses.addCourse(new_course)
    storage.save(my_courses.courses)
    
    return {"message": f"Successfully added {course_in.course_name}."}

@app.get("/gpa/total", tags=["GPA Calculation"])
def get_total_gpa():
    """Calculate the final cumulative weighted GPA."""
    return {"total_gpa": round(my_courses.calculateGPA(), 2)}

@app.get("/gpa/term/{term_id}", tags=["GPA Calculation"])
def get_term_gpa(term_id: int):
    """Calculate the weighted GPA for a specific term."""
    return {
        "term_id": term_id, 
        "term_gpa": round(my_courses.calculateGPAByTerm(term_id), 2)
    }

# ==========================================
# 4. VISUALIZATION ENDPOINTS (IFRAMES)
# ==========================================

@app.get("/visualize/gpa", response_class=HTMLResponse, tags=["Visualizations"])
def visualize_gpa_by_term():
    """Returns an interactive Plotly bar chart of GPA by term."""
    return generate_gpa_plot(my_courses)

@app.get("/visualize/credits", response_class=HTMLResponse, tags=["Visualizations"])
def visualize_credits_distribution():
    """Returns an interactive Plotly treemap of credits per course."""
    return generate_credits_plot(my_courses)

@app.get("/visualize/term/{term_id}", response_class=HTMLResponse, tags=["Visualizations"])
def visualize_specific_term(term_id: int):
    """Returns an interactive Plotly bar chart for a specific term's courses."""
    return generate_term_specific_plot(my_courses, term_id)