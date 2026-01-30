import streamlit as st
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Automation Tracker",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state for tasks
if "tasks" not in st.session_state:
    st.session_state.tasks = [
        {
            "id": 1,
            "name": "Daily Report Generation",
            "status": "completed",
            "submitter": "Ilda Karaj",
            "priority": "Medium",
            "last_run": "2026-01-30 09:00",
            "notes": "Runs every morning at 9 AM"
        },
        {
            "id": 2,
            "name": "Data Sync Pipeline",
            "status": "running",
            "submitter": "Torben Schmidt",
            "priority": "High",
            "last_run": "2026-01-30 14:30",
            "notes": "Syncing customer data from CRM"
        },
        {
            "id": 3,
            "name": "Backup Automation",
            "status": "pending",
            "submitter": "Kilian Zedelius",
            "priority": "Critical",
            "last_run": "2026-01-29 23:00",
            "notes": "Scheduled for midnight"
        },
    ]

if "next_id" not in st.session_state:
    st.session_state.next_id = 4

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

# Status styling
STATUS_COLORS = {
    "pending": "🟡",
    "running": "🔵",
    "completed": "🟢",
    "failed": "🔴"
}

# Priority options
PRIORITIES = ["Low", "Medium", "High", "Critical"]
PRIORITY_COLORS = {
    "Low": "🟢",
    "Medium": "🟡",
    "High": "🟠",
    "Critical": "🔴"
}

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
</style>

<div class="header-container">
    <p class="header-title">Automation Tracker</p>
    <p class="header-subtitle">Welcome! Submit your automation ideas and track their progress here.</p>
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
        ["pending", "running", "completed", "failed"],
        default=["pending", "running", "completed", "failed"]
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

filtered_tasks = [t for t in st.session_state.tasks if t["status"] in filter_status]
if filter_priority:
    filtered_tasks = [t for t in filtered_tasks if t.get("priority") in filter_priority]
if filter_submitter:
    filtered_tasks = [t for t in filtered_tasks if t.get("submitter") in filter_submitter]

if not filtered_tasks:
    st.info("No tasks found. Add a new task above!")
else:
    for task in filtered_tasks:
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])

            with col1:
                priority = task.get('priority', 'Medium')
                priority_icon = PRIORITY_COLORS.get(priority, '⚪')
                st.markdown(f"**{STATUS_COLORS[task['status']]} {task['name']}** &nbsp; {priority_icon} {priority}")
                submitter = task.get('submitter', 'Unknown')
                st.caption(f"Submitted by: {submitter} | Last run: {task['last_run']} | {task['notes']}")

            with col2:
                new_status = st.selectbox(
                    "Status",
                    ["pending", "running", "completed", "failed"],
                    index=["pending", "running", "completed", "failed"].index(task["status"]),
                    key=f"status_{task['id']}",
                    label_visibility="collapsed"
                )
                if new_status != task["status"]:
                    task["status"] = new_status
                    task["last_run"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                    st.rerun()

            with col3:
                if st.button("🗑️", key=f"delete_{task['id']}"):
                    st.session_state.tasks = [t for t in st.session_state.tasks if t["id"] != task["id"]]
                    st.rerun()

            st.divider()

# Footer
st.markdown("---")
st.caption("Built with Streamlit | Data resets on app restart")
