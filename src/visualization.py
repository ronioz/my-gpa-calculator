import plotly.express as px
import plotly.graph_objects as go
from src.classes import Courses

THEME_COLOR = '#0dcaf0' 

def generate_gpa_plot(my_courses: Courses) -> str:
    """Generates a combo chart showing Term GPA (bars) and Cumulative GPA (line)."""
    terms = sorted(list(set(int(course.termID) for course in my_courses.courses.values())))
    if not terms:
        return "<h3>No course data available to visualize.</h3>"

    x_vals = []
    term_gpas = []
    cumulative_gpas = []

    # Calculate both micro and macro stats for each term
    for term in terms:
        x_vals.append(f"Term {term}")
        
        # 1. Term Specific GPA
        term_gpa = my_courses.calculateGPAByTerm(term)
        term_gpas.append(round(term_gpa, 2))
        
        # 2. Cumulative GPA up to this term
        c_score = sum(c.score * c.credit for c in my_courses.courses.values() if int(c.termID) <= term)
        c_credit = sum(c.credit for c in my_courses.courses.values() if int(c.termID) <= term)
        cum_gpa = c_score / c_credit if c_credit > 0 else 0.0
        cumulative_gpas.append(round(cum_gpa, 2))

    # Build the combo chart layer by layer
    fig = go.Figure()

    # Layer 1: The Bars (Term Performance)
    fig.add_trace(go.Bar(
        x=x_vals,
        y=term_gpas,
        name="Term GPA",
        marker_color='#3d8bfd', # Deep blue from our palette
        text=term_gpas,
        textposition='inside',
        insidetextanchor='middle'
    ))

    # Layer 2: The Line (Cumulative Trend)
    fig.add_trace(go.Scatter(
        x=x_vals,
        y=cumulative_gpas,
        name="Cumulative Trend",
        mode='lines+markers+text',
        marker=dict(color='#0dcaf0', size=12), # Glowing cyan
        line=dict(color='#0dcaf0', width=4),
        text=cumulative_gpas,
        textposition='top center',
        textfont=dict(size=14, color='white')
    ))

    # Polish the dark mode layout
    fig.update_layout(
        template='plotly_dark',
        title="Performance Analytics: Term vs. Cumulative",
        xaxis_title="Academic Term",
        yaxis_title="Weighted Grade (1-5)",
        yaxis=dict(range=[0, 5.8]), # Extra headroom for the top labels
        legend=dict(
            orientation="h", # Horizontal legend
            yanchor="bottom", 
            y=1.02, 
            xanchor="right", 
            x=1
        ),
        margin=dict(t=60, l=10, r=10, b=10)
    )

    return fig.to_html(full_html=False, include_plotlyjs='cdn')

def generate_credits_plot(my_courses: Courses) -> str:
    """Generates a hierarchical treemap of credits per course grouped by term."""
    if not my_courses.courses:
        return "<h3>No course data available to visualize.</h3>"
        
    data = []
    for c in my_courses.courses.values():
        data.append({
            "Term": f"Term {c.termID}",
            "Course": c.courseName,
            "Credits": c.credit
        })

    # A custom palette of cool, blueish tones that pop in dark mode
    blueish_palette = ['#0dcaf0', '#0d6efd', '#6ea8fe', '#9ec5fe', '#3d8bfd']

    fig = px.treemap(
        data, 
        path=["Term", "Course"],  
        values="Credits",         
        color="Term",             
        color_discrete_sequence=blueish_palette,  # Force Plotly to use our blues!
        title="Credit Distribution per Term"
    )
    
    fig.update_layout(
        template='plotly_dark',
        margin=dict(t=40, l=10, r=10, b=10) 
    )
    
    fig.update_traces(
        textinfo="label+value", 
        textfont=dict(size=14)
    )
    
    return fig.to_html(full_html=False, include_plotlyjs='cdn')

def generate_term_specific_plot(my_courses: Courses, term_id: int) -> str:
    """Generates a bar chart showing scores for courses in a specific term."""
    courses_in_term = [c for c in my_courses.courses.values() if c.termID == term_id]
    
    if not courses_in_term:
        return f"<h3>No course data available for Term {term_id}.</h3>"

    x_vals = [c.courseName for c in courses_in_term]
    y_vals = [c.score for c in courses_in_term]

    fig = px.bar(
        x=x_vals,
        y=y_vals,
        title=f"Course Grades for Term {term_id}",
        text=y_vals
    )
    
    fig.update_traces(
        textposition='outside',
        marker_color=THEME_COLOR
    )
    
    fig.update_layout(
        template='plotly_dark',
        xaxis_title="Course",
        yaxis_title="Grade (1-5)",
        yaxis_range=[0, 5.5], 
        xaxis_tickangle=-45
    )
    
    return fig.to_html(full_html=False, include_plotlyjs='cdn')