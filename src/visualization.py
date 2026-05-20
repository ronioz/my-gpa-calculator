import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from src.classes import Courses

MONO_COLORS = ['#404040', '#555555', '#707070', '#888888', '#A0A0A0', '#C0C0C0']
pio.templates.default = "plotly_dark"
pio.templates["mono_theme"] = pio.templates["plotly_dark"]
pio.templates["mono_theme"].layout.colorway = MONO_COLORS

def generate_gpa_plot(my_courses: Courses) -> str:
    """Generates a combo chart using shades of gray."""
    terms = sorted(list(set(int(course.termID) for course in my_courses.courses.values())))
    if not terms:
        return "<h3>No course data available to visualize.</h3>"

    x_vals, term_gpas, cumulative_gpas = [], [], []
    for term in terms:
        x_vals.append(f"Term {term}")
        term_gpas.append(round(my_courses.calculateGPAByTerm(term), 2))
        c_score = sum(c.score * c.credit for c in my_courses.courses.values() if int(c.termID) <= term)
        c_credit = sum(c.credit for c in my_courses.courses.values() if int(c.termID) <= term)
        cumulative_gpas.append(round(c_score / c_credit if c_credit > 0 else 0.0, 2))

    fig = go.Figure()
    fig.add_trace(go.Bar(x=x_vals, y=term_gpas, name="Term GPA", marker_color='#404040', text=term_gpas, textposition='auto'))
    fig.add_trace(go.Scatter(x=x_vals, y=cumulative_gpas, name="Cumulative Trend", mode='lines+markers', 
                             marker=dict(color='#A0A0A0', size=10), line=dict(color='#A0A0A0', width=3)))

    fig.update_layout(template='mono_theme', title="Performance Analytics: Term vs. Cumulative", 
                      yaxis=dict(range=[0, 5.5], gridcolor='#262626'), xaxis=dict(gridcolor='#262626'))
    html_content = fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    css_injection = """
    <style>
        body { background: transparent !important; margin: 0 !important; padding: 0 !important; }
        .plotly-graph-div { background: transparent !important; }
    </style>
    """
    return css_injection + html_content

def generate_credits_plot(my_courses: Courses) -> str:
    """Generates a treemap using grayscale tones."""
    if not my_courses.courses: return "<h3>No data available.</h3>"
    
    data = [{"Term": f"Term {c.termID}", "Course": c.courseName, "Credits": c.credit} for c in my_courses.courses.values()]
    fig = px.treemap(data, path=["Term", "Course"], values="Credits", color="Term", 
                     color_discrete_sequence=MONO_COLORS, title="Credit Distribution per Term")
    
    fig.update_layout(template='mono_theme', margin=dict(t=40, l=10, r=10, b=10))
    html_content = fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    css_injection = """
    <style>
        body { background: transparent !important; margin: 0 !important; padding: 0 !important; }
        .plotly-graph-div { background: transparent !important; }
    </style>
    """
    return css_injection + html_content

def generate_term_specific_plot(my_courses: Courses, term_id: int) -> str:
    """Generates a grayscale bar chart for a specific term."""
    courses_in_term = [c for c in my_courses.courses.values() if c.termID == term_id]
    if not courses_in_term: return f"<h3>No data for Term {term_id}.</h3>"

    fig = px.bar(x=[c.courseName for c in courses_in_term], y=[c.score for c in courses_in_term],
                 title=f"Course Grades for Term {term_id}", text=[c.score for c in courses_in_term])
    
    fig.update_traces(marker_color='#606060', textposition='outside')
    fig.update_layout(template='mono_theme', yaxis=dict(range=[0, 5.5], gridcolor='#262626'), xaxis=dict(gridcolor='#262626'))
    html_content = fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    css_injection = """
    <style>
        body { background: transparent !important; margin: 0 !important; padding: 0 !important; }
        .plotly-graph-div { background: transparent !important; }
    </style>
    """
    return css_injection + html_content