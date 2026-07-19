import streamlit as st
from services.todoist_service import (
    get_projects,
    get_tasks_by_project
)
from database.db import (
    save_study_session,
    get_today_hours,
    is_task_completed,
    update_task_status
)

@st.dialog("📋 Tasks")


def career_dialog(project_name):

    st.title(f"📚 {project_name}")
    st.caption("Track your learning progress")
    st.subheader("Today's Study")

    hours = st.number_input(
        "Hours Studied",
        min_value=0.0,
        max_value=24.0,
        step=0.5,
        value=get_today_hours(project_name)
    )

    st.divider()
    st.subheader("Today's Tasks")

    projects = get_projects()

    project = next(
        (p for p in projects if p.name == project_name),
        None
    )

    if project is None:
        st.error(f"Project '{project_name}' not found in Todoist.")
        st.stop()

    tasks = get_tasks_by_project(project.id)




    completed_weight = 0
    total_weight = len(tasks)

    for task in tasks:

        completed = is_task_completed(task.id)

        checked = st.checkbox(
            task.content,
            value=completed,
            key=f"task_{task.id}"
        )

        if checked != completed:
            update_task_status(task.id, checked)
    
        if checked:
            completed_weight += 1

    progress = (
        round(completed_weight / total_weight * 100)
        if total_weight > 0
        else 0
    )
    
    st.divider()

    st.subheader("Progress")

    st.progress(progress / 100)

    st.metric(
        "Completion",
        f"{progress}%"
    )

    st.metric(
        "Study Hours",
        f"{hours:.1f} h"
    )

    if st.button(
        "💾 Save Progress",
        use_container_width=True
    ):
        save_study_session(
            project_name,
            hours
        )

        st.success("Progress Saved ✅")

