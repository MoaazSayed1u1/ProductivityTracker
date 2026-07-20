import streamlit as st
import pandas as pd
from datetime import date
from datetime import datetime
from database.db import (
    create_database,
    seed_career_tasks,
    seed_tracks,
    save_today,
    get_connection,
    get_today_score,
    get_current_streak,
    get_week_average,
    get_month_average,
    get_all_scores,
    get_trend_data,
    get_analytics,
    get_total_hours,
    get_today_hours,
    get_completed_tasks,
    save_daily_reflection,
    get_daily_reflection,
    get_last_7_reflections,
    get_last_30_days,
    get_year_data
)
from components.heatmap import prepare_heatmap_data
from components.heatmap_chart import create_heatmap
from components.trend_chart import create_trend_chart
from components.goal_progress import create_goal_progress
from components.career_dialog import career_dialog
from database.db import get_track_progress
from services.todoist_service import get_projects
from components.career_card import create_career_card
# ==========================
# Page Configuration
# ==========================

st.set_page_config(
    page_title="Productivity Tracker",
    page_icon="🔥",
    layout="wide"
)

# ==========================
# Database
# ==========================

today = date.today().isoformat()
create_database()
seed_tracks()
seed_career_tasks()
current_score = get_today_score()
total_hours = get_total_hours("Data Analysis")
today_hours = get_today_hours("Data Analysis")
completed, total = get_completed_tasks("Data Analysis")
goal_fig = create_goal_progress(current_score)
current_streak = get_current_streak()
week_avg = get_week_average()
month_avg = get_month_average()

df = get_all_scores()
heatmap_df = prepare_heatmap_data(df)
heatmap_fig = create_heatmap(heatmap_df)

period = st.segmented_control(
    "",
    options=["Last 30 Days", "This Year"],
    default="Last 30 Days"
)

if period == "Last 30 Days":
    trend_df = get_last_30_days()
else:
    trend_df = get_year_data()

trend_fig = create_trend_chart(trend_df)

#st.write(trend_df)
trend_fig = create_trend_chart(trend_df)
analytics = get_analytics()
total_hours = get_total_hours("Data Analysis")
# ==========================
# Load CSS
# ==========================

with open("assets/style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# ==========================
# Header
# ==========================
hour = datetime.now().hour

if hour < 12:
    greeting = "Good Morning"
elif hour < 18:
    greeting = "Good Afternoon"
else:
    greeting = "Good Evening"

today_text = datetime.now().strftime("%A, %B %d, %Y")

left, right = st.columns([4, 1])

with left:
    st.markdown(
        f"""
<div style="padding-top:8px;">
<h1 style="margin:0;font-size:42px;font-weight:800;line-height:1.2;">
👋 {greeting}, Moaaz
</h1>

<p style="color:#94A3B8;font-size:18px;margin-top:8px;margin-bottom:0;">
Track your progress and build your best self.
</p>

</div>
""",
        unsafe_allow_html=True,
    )

with right:
    st.markdown(f"""
    <div style="
        display:flex;
        justify-content:flex-end;
        align-items:center;
        height:70px;
        color:#94A3B8;
        font-size:15px;
        font-weight:500;
    ">
        📅 {today_text}
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
# ==========================
# Main Layout
# ==========================
def metric_card(icon, title, value):
    st.markdown(
    f"""
<div class="metric-card">

<div class="metric-icon">{icon}</div>

<div class="metric-title">{title}</div>

<div class="metric-value">{value}</div>


</div>
""",
    unsafe_allow_html=True,
)


col1, col2, col3, col4 = st.columns(4, gap="large")

with col1:
    metric_card(
        "🔥",
        "Current Streak",
        f"{current_streak} Days"
    )

with col2:
    metric_card(
        "📈",
        "Weekly Average",
        f"{week_avg:.1f}%"
    )

with col3:
    metric_card(
        "📅",
        "Monthly Average",
        f"{month_avg:.1f}%"
    )

with col4:
    metric_card(
        "🎯",
        "Today's Score",
        f"{current_score}%"
    )

st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

left, right = st.columns([1, 2.3], gap="medium")

with left:

    with st.container(border=True):

        st.markdown("### 🎯 Today's Productivity")
        st.caption("How productive was your day?")

        score = st.slider(
            "",
            0,
            100,
            current_score,
            label_visibility="collapsed"
        )

        st.markdown(
            f"<h2 style='text-align:right;color:#7C5CFC'>{score}%</h2>",
            unsafe_allow_html=True
        )

        if st.button(
            "💾 Save Today's Score",
            use_container_width=True
        ):
            save_today(score)

with right:

    with st.container(border=True):

        st.markdown("### 🗓️ Productivity Heatmap")

        st.plotly_chart(
            heatmap_fig,
            use_container_width=True,
            config={"displayModeBar": False}
        )
# =========================
#FeedBack
# =========================

# ==========================
# Daily Reflection
# ==========================

with st.expander("📝 Daily Reflection", expanded=False):

    reflection = st.text_area(
        "",
        value=get_daily_reflection(today),
        height=180,
        placeholder="How was your day today?",
        label_visibility="collapsed"
    )

    if st.button("💾 Save Reflection", use_container_width=True):
        save_daily_reflection(today, reflection)
        st.success("Saved successfully ✅")


# ==========================
# Weekly Review
# ==========================

with st.expander("📅 Weekly Review", expanded=False):

    reflections = get_last_7_reflections()

    if not reflections:
        st.info("No reflections yet.")

    else:

        for day, reflection in reflections:

            st.markdown(
                f"""
                <div style="
                    font-size:17px;
                    font-weight:700;
                    margin-top:18px;
                    margin-bottom:8px;
                    color:#F8FAFC;
                ">
                    📅 {day}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <div style="
                    background:#0D1117;
                    border:1px solid #30363D;
                    border-radius:12px;
                    padding:14px;
                    color:#D1D5DB;
                    line-height:1.7;
                    margin-bottom:12px;
                ">
                    {reflection}
                </div>
                """,
                unsafe_allow_html=True
            )
# ==========================
# Heatmap
# ==========================

#st.divider()

#st.markdown("""
#<div class="card">
#    <h3>📅 Productivity Overview</h3>
#""", unsafe_allow_html=True)

#st.plotly_chart(
#    heatmap_fig,
#    use_container_width=True,
#    config={"displayModeBar": False}
#)

#st.markdown("</div>", unsafe_allow_html=True)

# ==========================
# Trend Chart
# ==========================

st.divider()
with st.container(border=True):
    st.markdown("""
    <div class="card">
        <h3>📈 Productivity Trend</h3>
    </div>
    """, unsafe_allow_html=True)

    period = st.segmented_control(
        "",
        options=["Last 30 Days", "This Year"],
        default="Last 30 Days",
        key="trend_period"
    )

    if period == "Last 30 Days":
        trend_df = get_last_30_days()
    else:
        trend_df = get_year_data()

    trend_fig = create_trend_chart(trend_df)

    st.plotly_chart(
        trend_fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )

st.markdown("</div>", unsafe_allow_html=True)
with st.container(border=True):
    st.subheader("📊 Analytics")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "⭐ Highest Score",
           f"{analytics['highest']}%"
        )

        st.metric(
            "📉 Lowest Score",
            f"{analytics['lowest']}%"
        )

    with c2:
        st.metric(
            "📈 Average",
            f"{analytics['average']}%"
        )

        st.metric(
            "🎯 Days ≥ 80%",
            analytics["above80"]
        )

    with c3:
        st.metric(
            "📅 Total Entries",
            analytics["entries"]
        )

        st.metric(
            "🔥 Current Streak",
            current_streak
        )


st.divider()
with st.container(border=True):
    st.subheader("🎯 Daily Goal")

    st.plotly_chart(
        goal_fig,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )
    
st.markdown("</div>", unsafe_allow_html=True)

st.header("🎯 Career Roadmap")

projects = [
    p for p in get_projects()
    if p.name.lower() != "inbox"
]

if not projects:
    st.info("No Todoist projects found.")
else:

    cols = st.columns(2)

    for i, project in enumerate(projects):

        with cols[i % 2]:
            create_career_card(project.name)


# ==========================
# Database Preview
# ==========================

st.divider()

with st.expander("🛠 Database Preview"):

    st.dataframe(
        heatmap_df,
        use_container_width=True
    )



st.subheader("Career Sessions")

conn = get_connection()

df = pd.read_sql_query(
    "SELECT * FROM career_sessions",
    conn
)

conn.close()

st.dataframe(df)
