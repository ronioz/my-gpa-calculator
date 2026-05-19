import sqlite3
from classes import Course, Courses

class CourseStorage:
    def __init__(self, filename: str = "courses.db") -> None:
        self.filename = filename
        self._init_db()

    def _init_db(self):
        """Creates the database table if it doesn't exist."""
        with sqlite3.connect(self.filename) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS courses (
                    course_name TEXT PRIMARY KEY,
                    credit INTEGER,
                    score INTEGER,
                    term_id INTEGER
                )
            """)

    def save(self, courses_dict: dict) -> None:
        """Saves current memory state to the database."""
        with sqlite3.connect(self.filename) as conn:
            # Clear old entries and insert current state
            conn.execute("DELETE FROM courses")
            for course in courses_dict.values():
                conn.execute(
                    "INSERT INTO courses VALUES (?, ?, ?, ?)",
                    (course.courseName, course.credit, course.score, course.termID)
                )

    def load(self) -> dict:
        """Loads data from the database into a dictionary."""
        courses = {}
        with sqlite3.connect(self.filename) as conn:
            cursor = conn.execute("SELECT * FROM courses")
            for row in cursor.fetchall():
                # row is (name, credit, score, term_id)
                course = Course(row[0], row[1], row[2], row[3])
                courses[course.courseName] = course
        return courses