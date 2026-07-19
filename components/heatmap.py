import pandas as pd
from datetime import datetime, timedelta


def prepare_heatmap_data(df):
    """
    يحول البيانات إلى DataFrame يحتوي على آخر 365 يوم.
    """

    CAREER_START = pd.Timestamp("2026-07-14")
    CAREER_END = CAREER_START + pd.Timedelta(days=364)
    
    all_dates = pd.date_range(start=CAREER_START, end= CAREER_END)

    calendar = pd.DataFrame({
        "date": all_dates
    })

    if not df.empty:
        calendar = calendar.merge(
            df,
            on="date",
            how="left"
        )

    calendar["score"] = calendar["score"].fillna(0)

    calendar["weekday"] = calendar["date"].dt.weekday

    # نخلي أول عمود يبدأ من أول يوم Monday
    start_date = calendar["date"].min()

    start_date = start_date - pd.Timedelta(days=start_date.weekday())

    calendar["week"] = (
        (calendar["date"] - start_date).dt.days // 7
    )

    calendar["month"] = calendar["date"].dt.strftime("%b")

    calendar["day_name"] = calendar["date"].dt.strftime("%a")

    calendar["day"] = calendar["date"].dt.day

    calendar["color"] = calendar["score"].apply(get_color)

    return calendar
def get_color(score):
    """
    Convert productivity score to GitHub-style color.
    """

    if score == 0:
        return "#161B22"

    elif score <= 20:
        return "#0E4429"

    elif score <= 40:
        return "#006D32"

    elif score <= 60:
        return "#26A641"

    elif score <= 80:
        return "#39D353"

    return "#56F56F"