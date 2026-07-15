import sqlite3
from pathlib import Path
from datetime import date, timedelta

Path("data").mkdir(exist_ok=True)

DB_FILE = "data/productivity.db"


def get_connection():
    return sqlite3.connect(DB_FILE)


def create_database():
    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS productivity(
            date TEXT PRIMARY KEY,
            score INTEGER
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