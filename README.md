Based on the files provided, here is a professional `README.md` for your Hungarian University GPA project.

---

# Hungarian University GPA Portal

A comprehensive GPA management tool designed for the Hungarian higher education grading system (1–5 scale). This project combines a FastAPI backend with an interactive dashboard to help students track their academic progress, visualize grade distributions, and calculate weighted cumulative GPAs.

## 🚀 Features

* **GPA Management:** Easily add, edit, or remove courses with their respective ECTS credits, grades, and term identifiers.
* **Weighted GPA Calculation:** Automatically computes weighted cumulative GPA and term-specific GPAs.
* **Interactive Visualizations:** Powered by **Plotly**, providing:
* **GPA Trends:** Compare term performance against cumulative progress.
* **Credit Distribution:** A treemap view to visualize the weight of your course load.
* **Term Details:** Breakdown of grades for specific semesters.


* **Responsive UI:** A dark-mode dashboard built with Bootstrap and custom CSS for a sleek, "terminal-inspired" aesthetic.

## 🛠 Tech Stack

* 
**Backend:** [FastAPI](https://fastapi.tiangolo.com/) 


* 
**Frontend Templating:** [Jinja2](https://jinja.palletsprojects.com/) 


* 
**Data Visualization:** [Plotly](https://plotly.com/) 


* 
**Data Handling:** Pandas and Pydantic 


* **Serialization:** JSON-based persistence

## 📦 Installation

1. **Clone the repository:**
```bash
git clone <your-repository-url>
cd <project-folder>

```


2. **Install dependencies:**
It is recommended to use a virtual environment.
```bash
pip install -r requirements.txt

```


3. **Run the application:**
```bash
uvicorn app:app --reload

```


4. **Access the Dashboard:**
Open your browser and navigate to `http://127.0.0.1:8000/dashboard`

## 📝 How to Use

### Via Web Dashboard

* Enter courses in the format: `CourseName Credit Grade Term` (e.g., `Calculus 5 4 1`).
* Use the "Course History" section to update credits, grades, or term assignments on the fly.
* Toggle between different visual reports using the buttons in the "Visual Performance" card.

### Via API

The project exposes a RESTful API:

* `GET /courses`: Retrieve all courses in JSON format.
* `POST /courses`: Add a new course via JSON request.
* `GET /gpa/total`: Get the current cumulative GPA.
* `GET /gpa/term/{term_id}`: Get GPA for a specific term.

## 🔮 Future Improvements

* **Authentication:** Add user login support to allow multiple students to manage their own gradebooks.
* **Export/Import:** Implement CSV/PDF export for official grade reports.
* **Database Integration:** Migrate from `courses.json` to a SQL database (e.g., SQLite/PostgreSQL) for improved concurrency and data integrity.
* **Predictive Analytics:** Add a tool to calculate "what-if" scenarios (e.g., "What grade do I need in my remaining courses to reach a 4.5 GPA?").

---

*This project was built to facilitate academic tracking within the Hungarian university system.*