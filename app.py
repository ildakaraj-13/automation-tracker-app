import streamlit as st
import json
import os
from datetime import datetime

# Data file path
DATA_FILE = "tasks.json"

def load_tasks():
    """Load tasks from JSON file."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            return data.get("tasks", []), data.get("next_id", 1)
    return [], 1

def save_tasks():
    """Save tasks to JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump({
            "tasks": st.session_state.tasks,
            "next_id": st.session_state.next_id
        }, f, indent=2)

# Page config
st.set_page_config(
    page_title="Automation Tracker",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state for tasks (load from file)
if "tasks" not in st.session_state:
    tasks, next_id = load_tasks()
    st.session_state.tasks = tasks
    st.session_state.next_id = next_id

# Team members
TEAM_MEMBERS = [
    "Kilian Zedelius",
    "Jan Krueger",
    "Dr. Patrick Gassmann",
    "Anna Hosp",
    "Johannes Müller",
    "Johannes Brenninkmeyer",
    "Ludwig Jakob",
    "Hendrik Wendefeuer",
    "Ilda Karaj",
    "Julian Döttinger",
    "Artem Vorobyev",
    "Florian Kroiss",
    "Tobias Junker",
    "Torben Schmidt",
    "Michael Schreiber",
    "Dominique Vainikka",
]

# Options
PRIORITIES = ["Low", "Medium", "High", "Critical"]
STATUSES = ["pending", "running", "completed", "failed"]

# Custom CSS for modern styling
st.markdown("""
<style>
    .header-container {
        background: linear-gradient(135deg, #1e3a5f 0%, #2d5a87 100%);
        padding: 2rem 2.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .header-title {
        color: white;
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .header-subtitle {
        color: rgba(255, 255, 255, 0.85);
        font-size: 1.1rem;
        margin-top: 0.5rem;
        font-weight: 400;
    }
    .header-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.15);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        margin-top: 1rem;
    }
    .task-card {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 1rem 1.25rem;
        margin-bottom: 0.75rem;
        border-left: 4px solid #1e3a5f;
    }
    .task-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1e3a5f;
        margin: 0 0 0.25rem 0;
    }
    .task-meta {
        font-size: 0.85rem;
        color: #6c757d;
        margin: 0;
    }
    .task-description {
        font-size: 0.9rem;
        color: #495057;
        margin-top: 0.5rem;
        padding-top: 0.5rem;
        border-top: 1px solid #dee2e6;
    }
    .priority-badge {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 500;
        margin-left: 0.5rem;
    }
    .priority-low { background: #d4edda; color: #155724; }
    .priority-medium { background: #fff3cd; color: #856404; }
    .priority-high { background: #ffe5d0; color: #c25400; }
    .priority-critical { background: #f8d7da; color: #721c24; }
</style>

<div class="header-container">
    <p class="header-title">Automation Tracker</p>
    <p class="header-subtitle">Submit your automation ideas and track their progress.</p>
    <span class="header-badge">Internal Tool</span>
</div>
""", unsafe_allow_html=True)

# Metrics row
col1, col2, col3, col4 = st.columns(4)
total = len(st.session_state.tasks)
completed = len([t for t in st.session_state.tasks if t["status"] == "completed"])
running = len([t for t in st.session_state.tasks if t["status"] == "running"])
failed = len([t for t in st.session_state.tasks if t["status"] == "failed"])

col1.metric("Total Tasks", total)
col2.metric("Completed", completed)
col3.metric("Running", running)
col4.metric("Failed", failed)

st.divider()

# Add new task section
with st.expander("➕ Add New Task", expanded=False):
    with st.form("add_task_form", clear_on_submit=True):
        new_name = st.text_input("Task Name")
        new_submitter = st.selectbox("Submitted by", TEAM_MEMBERS)
        new_priority = st.selectbox("Priority", PRIORITIES, index=1)  # Default to Medium
        new_notes = st.text_area(
            "Description",
            placeholder="Describe what this automation should do (e.g., steps, inputs, expected outputs...)"
        )

        if st.form_submit_button("Add Task"):
            if new_name:
                st.session_state.tasks.append({
                    "id": st.session_state.next_id,
                    "name": new_name,
                    "submitter": new_submitter,
                    "priority": new_priority,
                    "status": "pending",
                    "last_run": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "notes": new_notes
                })
                st.session_state.next_id += 1
                save_tasks()
                st.rerun()
            else:
                st.error("Please enter a task name")

# Task list
st.subheader("📋 Tasks")

# Filters
col_filter1, col_filter2, col_filter3 = st.columns(3)
with col_filter1:
    filter_status = st.multiselect(
        "Filter by status",
        STATUSES,
        default=[]
    )
with col_filter2:
    filter_priority = st.multiselect(
        "Filter by priority",
        PRIORITIES,
        default=[]
    )
with col_filter3:
    filter_submitter = st.multiselect(
        "Filter by submitter",
        TEAM_MEMBERS,
        default=[]
    )

filtered_tasks = st.session_state.tasks.copy()
if filter_status:
    filtered_tasks = [t for t in filtered_tasks if t["status"] in filter_status]
if filter_priority:
    filtered_tasks = [t for t in filtered_tasks if t.get("priority") in filter_priority]
if filter_submitter:
    filtered_tasks = [t for t in filtered_tasks if t.get("submitter") in filter_submitter]

if not filtered_tasks:
    st.info("No tasks found. Add a new task above!")
else:
    for task in filtered_tasks:
        priority = task.get('priority', 'Medium')
        priority_class = f"priority-{priority.lower()}"
        submitter = task.get('submitter', 'Unknown')
        description = task.get('notes', '')

        # Build task card HTML
        description_html = f'<p class="task-description">{description}</p>' if description else ''

        st.markdown(f"""
        <div class="task-card">
            <p class="task-title">{task['name']}<span class="priority-badge {priority_class}">{priority}</span></p>
            <p class="task-meta">Submitted by {submitter} · Updated {task['last_run']}</p>
            {description_html}
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([4, 1])
        with col1:
            new_status = st.selectbox(
                "Status",
                STATUSES,
                index=STATUSES.index(task["status"]),
                key=f"status_{task['id']}",
                label_visibility="collapsed"
            )
            if new_status != task["status"]:
                task["status"] = new_status
                task["last_run"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                save_tasks()
                st.rerun()

        with col2:
            if st.button("Delete", key=f"delete_{task['id']}", type="secondary"):
                st.session_state.tasks = [t for t in st.session_state.tasks if t["id"] != task["id"]]
                save_tasks()
                st.rerun()

# Footer
st.markdown("---")
st.caption("Automation Tracker · Data persisted locally")
