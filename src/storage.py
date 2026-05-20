import json
import os
from src.classes import Course

class CourseStorage:
    def __init__(self, filename: str = "courses.json") -> None:
        self.filename = filename

    def save(self, courses_dict: dict) -> None:
        # Convert Course objects to dictionaries for JSON serialization
        serializable = {
            name: course.to_dict() 
            for name, course in courses_dict.items()
        }
        
        with open(self.filename, "w") as f:
            json.dump(serializable, f, indent=4)

    def load(self) -> dict:
        if not os.path.exists(self.filename):
            return {}
        
        with open(self.filename, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                return {}
        
        # Convert dictionaries back into Course objects
        courses = {}
        for name, course_data in data.items():
            courses[name] = Course.from_dict(course_data)
        return courses