import streamlit as st

from database.db import (
    get_total_hours,
    get_today_hours,
    get_completed_tasks,
    get_track_progress
)

from components.career_dialog import career_dialog


def create_career_card(project_name):
    
    total_hours = get_total_hours(project_name)
    today_hours = get_today_hours(project_name)
    completed, total = get_completed_tasks(project_name)
    progress = get_track_progress(project_name)

    with st.container(border=True):

        st.subheader(project_name)

        st.progress(progress / 100)

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "⏱ Hours",
                f"{total_hours} h"
            )

        with c2:
            st.metric(
                "📅 Today",
                f"{today_hours} h"
            )

        with c3:
            st.metric(
                "✔ Tasks",
                f"{completed}/{total}"
            )

        if st.button(
            f"Open {project_name}",
            key=f"open_{project_name.replace(' ', '_')}",
            width="stretch"
        ):
            st.write(project_name)
            career_dialog(project_name)
            