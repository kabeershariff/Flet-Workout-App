import sqlite3
from datetime import datetime

def connect_db():
    return sqlite3.connect('beast.db')

def schedule():
    with connect_db() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS workouts (
        id INTEGER PRIMARY KEY,
        day TEXT,
        workout_name TEXT,
        sets INTEGER,
        reps INTEGER      
        )
        """)

def log():
    with connect_db() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS progress_log(
        id INTEGER PRIMARY KEY,
        date TEXT,
        workout_id INTEGER,
        status TEXT,
        FOREIGN KEY (workout_id) REFERENCES workouts(id)
        )
        """)
def add_workout(day, workout_name, sets, reps):
    with connect_db() as conn:
        conn.execute("""
        INSERT INTO workouts(day, workout_name, sets, reps)
        VALUES (?, ?, ?, ?)
        """, (day, workout_name, sets, reps))
        conn.commit()

def remove_workout(workout_id):
    with connect_db() as conn:
        conn.execute("""
        DELETE FROM workouts where id = ?
        """, (workout_id,))

def add_log(date, workout_id, status):
    with connect_db() as conn:
        conn.execute("""
        INSERT INTO progress_log(date, workout_id, status)
        VALUES (?, ?, ?)
        """, (date, workout_id, status))
        conn.commit()

def fetch_schedule_values():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT id, day, workout_name, sets, reps FROM workouts
        """)
        return cursor.fetchall()

def get_today_workout():
    with connect_db() as conn:
        cursor = conn.cursor()
        today = datetime.today().strftime('%A')
        query = "SELECT * FROM workouts WHERE day = ?"
        cursor.execute(query, (today,))
        return cursor.fetchall()

def is_empty_table():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM workouts")
        count = cursor.fetchone()[0]
        return count == 0