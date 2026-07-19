import sqlite3
from pathlib import Path
from datetime import date, timedelta
import pandas as pd
from services.todoist_service import get_projects, get_tasks_by_project


Path("data").mkdir(exist_ok=True)

DB_FILE = "data/productivity.db"


def get_connection():
    return sqlite3.connect(DB_FILE)


def create_database():
    conn = get_connection()
    cursor = conn.cursor()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS productivity(
            date TEXT PRIMARY KEY,
            score INTEGER
        )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS career_tasks(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        track TEXT NOT NULL,

        task_name TEXT NOT NULL,

        weight INTEGER NOT NULL,

        completed INTEGER DEFAULT 0

    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS career_tracks(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT UNIQUE,

        icon TEXT,

        color TEXT

    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS career_sessions(

        track TEXT NOT NULL,

        session_date TEXT NOT NULL,

        study_hours REAL NOT NULL,

        productivity INTEGER,

        notes TEXT,

        PRIMARY KEY(track, session_date)

    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS task_progress (
        task_id TEXT PRIMARY KEY,
        completed INTEGER DEFAULT 0
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS daily_reflections (
        date TEXT PRIMARY KEY,
        reflection TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_today(score):
    conn = get_connection()

    today = date.today().isoformat()

    conn.execute("""
        INSERT OR REPLACE INTO productivity(date, score)
        VALUES(?,?)
    """, (today, score))

    conn.commit()
    conn.close()


def get_today_score():
    conn = get_connection()

    today = date.today().isoformat()

    cursor = conn.execute("""
        SELECT score
        FROM productivity
        WHERE date=?
    """, (today,))

    row = cursor.fetchone()

    conn.close()

    if row:
        return row[0]

    return 75


def get_current_streak():
    conn = get_connection()

    rows = conn.execute("""
        SELECT date
        FROM productivity
        ORDER BY date DESC
    """).fetchall()

    conn.close()

    dates = {row[0] for row in rows}

    streak = 0
    current = date.today()

    while current.isoformat() in dates:
        streak += 1
        current -= timedelta(days=1)

    return streak


def get_week_average():
    conn = get_connection()

    week_ago = (date.today() - timedelta(days=6)).isoformat()

    row = conn.execute("""
        SELECT AVG(score)
        FROM productivity
        WHERE date >= ?
    """, (week_ago,)).fetchone()

    conn.close()

    return round(row[0], 1) if row[0] else 0


def get_month_average():
    conn = get_connection()

    month_start = date.today().replace(day=1).isoformat()

    row = conn.execute("""
        SELECT AVG(score)
        FROM productivity
        WHERE date >= ?
    """, (month_start,)).fetchone()

    conn.close()

    return round(row[0], 1) if row[0] else 0

def get_all_scores():
    conn = get_connection()

    df = pd.read_sql_query(
        """
        SELECT
            date,
            score
        FROM productivity
        ORDER BY date
        """,
        conn
    )

    conn.close()

    if df.empty:
        return df

    df["date"] = pd.to_datetime(df["date"])

    return df


def get_trend_data():
    conn = get_connection()

    df = pd.read_sql_query(
        """
        SELECT
            date,
            score
        FROM productivity
        ORDER BY date
        """,
        conn
    )

    conn.close()

    if df.empty:
        return df

    df["date"] = pd.to_datetime(df["date"])

    return df


def get_analytics():
    conn = get_connection()

    stats = {}

    # Highest Score
    row = conn.execute(
        "SELECT MAX(score) FROM productivity"
    ).fetchone()
    stats["highest"] = row[0] if row[0] is not None else 0

    # Lowest Score
    row = conn.execute(
        "SELECT MIN(score) FROM productivity"
    ).fetchone()
    stats["lowest"] = row[0] if row[0] is not None else 0

    # Average Score
    row = conn.execute(
        "SELECT AVG(score) FROM productivity"
    ).fetchone()
    stats["average"] = round(row[0], 1) if row[0] else 0

    # Total Entries
    row = conn.execute(
        "SELECT COUNT(*) FROM productivity"
    ).fetchone()
    stats["entries"] = row[0]

    # Days >= 80
    row = conn.execute(
        "SELECT COUNT(*) FROM productivity WHERE score >= 80"
    ).fetchone()
    stats["above80"] = row[0]

    conn.close()

    return stats



def seed_tracks():

    conn = get_connection()

    count = conn.execute(
        "SELECT COUNT(*) FROM career_tracks"
    ).fetchone()[0]

    if count == 0:

        tracks = [

            ("Data Analysis","📊","#39D353"),

            ("Machine Learning","🤖","#58A6FF"),

            ("Lean Six Sigma","🏭","#F2CC60"),

            ("Supply Chain","🚚","#FF7B72")

        ]

        conn.executemany(

            """
            INSERT INTO career_tracks(name,icon,color)
            VALUES(?,?,?)
            """,

            tracks

        )

    conn.commit()

    conn.close()




def seed_career_tasks():

    conn = get_connection()

    count = conn.execute(
        "SELECT COUNT(*) FROM career_tasks"
    ).fetchone()[0]

    if count == 0:

        tasks = [

            ("Data Analysis","Python",10),
            ("Data Analysis","NumPy",10),
            ("Data Analysis","Pandas",15),
            ("Data Analysis","Matplotlib",10),
            ("Data Analysis","SQL",20),
            ("Data Analysis","Statistics",15),
            ("Data Analysis","Power BI",20)

        ]

        conn.executemany(

            """
            INSERT INTO career_tasks(track,task_name,weight)
            VALUES(?,?,?)
            """,

            tasks

        )

    conn.commit()

    conn.close()

def get_tasks(track):

    conn = get_connection()

    rows = conn.execute(

        """
        SELECT
            id,
            task_name,
            weight,
            completed
        FROM career_tasks
        WHERE track=?
        """,

        (track,)

    ).fetchall()

    conn.close()

    return rows

def update_task(task_id, completed):

    conn = get_connection()

    conn.execute(

        """
        UPDATE career_tasks
        SET completed=?
        WHERE id=?
        """,

        (completed, task_id)

    )

    conn.commit()

    conn.close()


def get_track_progress(track):

    completed, total = get_completed_tasks(track)

    if total == 0:
        return 0

    return round(completed / total * 100)



def get_tracks():

    conn = get_connection()

    rows = conn.execute(
        """
        SELECT
            name,
            icon,
            color
        FROM career_tracks
        ORDER BY id
        """
    ).fetchall()

    conn.close()

    return rows


from datetime import date


def save_study_session(track, hours):

    print("SAVE:", track, hours)

    conn = get_connection()

    conn.execute(
    """
    INSERT OR REPLACE INTO career_sessions(
        track,
        session_date,
        study_hours
    )
    VALUES(?,?,?)
    """,
    (
        track,
        date.today().isoformat(),
        hours
    )
)

    conn.commit()
    cursor = conn.execute("SELECT * FROM career_sessions")
    print(cursor.fetchall())

    conn.close()



def get_today_hours(track):

    conn = get_connection()

    row = conn.execute(
        """
        SELECT study_hours
        FROM career_sessions
        WHERE track = ?
        AND session_date = ?
        """,
        (
            track,
            date.today().isoformat()
        )
    ).fetchone()

    conn.close()

    if row:
        return row[0]

    return 0.0


def get_total_hours(track):

    conn = get_connection()

    row = conn.execute(
        """
        SELECT SUM(study_hours)
        FROM career_sessions
        WHERE track = ?
        """,
        (track,)
    ).fetchone()

    conn.close()

    if row[0] is None:
        return 0.0

    return round(float(row[0]), 1)


def get_today_hours(track):

    conn = get_connection()

    row = conn.execute(
        """
        SELECT study_hours
        FROM career_sessions
        WHERE track = ?
        AND session_date = ?
        """,
        (
            track,
            date.today().isoformat()
        )
    ).fetchone()

    conn.close()

    if row:
        return float(row[0])

    return 0.0


def get_completed_tasks(track):

    projects = get_projects()

    project = next(
        (p for p in projects if p.name == track),
        None
    )

    if project is None:
        return 0, 0

    tasks = get_tasks_by_project(project.id)

    conn = get_connection()
    cursor = conn.cursor()

    completed = 0

    for task in tasks:

        cursor.execute(
            "SELECT completed FROM task_progress WHERE task_id = ?",
            (task.id,)
        )

        row = cursor.fetchone()

        if row and row[0]:
            completed += 1

    conn.close()

    return completed, len(tasks)


def is_task_completed(task_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT completed FROM task_progress WHERE task_id = ?",
        (task_id,)
    )

    row = cursor.fetchone()

    conn.close()

    if row:
        return bool(row[0])

    return False

def update_task_status(task_id, completed):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO task_progress(task_id, completed)
        VALUES (?, ?)
    """, (task_id, int(completed)))

    conn.commit()

    conn.close()


def is_task_completed(task_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT completed FROM task_progress WHERE task_id = ?",
        (task_id,)
    )

    row = cursor.fetchone()

    conn.close()

    if row:
        return bool(row[0])

    return False


def update_task_status(task_id, completed):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO task_progress(task_id, completed)
        VALUES (?, ?)
    """, (task_id, int(completed)))

    conn.commit()

    conn.close()




def save_daily_reflection(date, reflection):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO daily_reflections (date, reflection)
        VALUES (?, ?)
    """, (date, reflection))

    conn.commit()
    conn.close()


def get_daily_reflection(date):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT reflection
        FROM daily_reflections
        WHERE date = ?
    """, (date,))

    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]

    return ""






def get_last_7_reflections():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT date, reflection
        FROM daily_reflections
        ORDER BY date DESC
        LIMIT 7
    """)

    data = cursor.fetchall()

    conn.close()

    return data[::-1]   # علشان يبقى من الأقدم للأحدث


def get_last_30_days():

    conn = get_connection()

    query = """
        SELECT date, score
        FROM productivity
        ORDER BY date DESC
        LIMIT 30
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df.sort_values("date")




def get_year_data():

    conn = get_connection()

    query = """
        SELECT date, score
        FROM productivity
        ORDER BY date
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df