import streamlit as st

from database.db import (
    create_database,
    save_today,
    get_today_score,
    get_current_streak,
    get_week_average,
    get_month_average
)

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
create_database()
current_score = get_today_score()
current_streak = get_current_streak()
week_avg = get_week_average()
month_avg = get_month_average()
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
st.title("🔥 Productivity Tracker")
st.caption("Become 1% better every day.")

st.divider()

# ==========================
# Main Layout
# ==========================
left, right = st.columns([2, 1])

with left:

    st.subheader("Today's Productivity")

    score = st.slider(
        "",
        min_value=0,
        max_value=100,
        value=current_score
    )

    st.progress(score / 100)

    st.metric(
        label="Today's Score",
        value=f"{score}%"
    )

    if st.button("💾 Save Today", use_container_width=True):
        save_today(score)
        st.success("Saved Successfully ✅")

with right:

    st.subheader("Quick Stats")

    st.metric(
    "🔥 Current Streak",
    f"{current_streak} Day" if current_streak == 1 else f"{current_streak} Days"
    )

    st.metric(
    "📈 Weekly Average",
    f"{week_avg}%"
    )


    st.metric(
    "📅 Monthly Average",
    f"{month_avg}%"
    )

st.divider()

st.subheader("GitHub Style Heatmap")

st.info("Coming Soon 🚀")