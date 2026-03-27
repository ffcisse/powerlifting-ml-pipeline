from pathlib import Path
import sqlite3


def get_connection():
    project_root = Path(__file__).resolve().parents[2]
    db_path = project_root / "powerlifting.db"
    return sqlite3.connect(db_path)


def show_tables(cursor):
    print("\n--- Tables in database ---")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(cursor.fetchall())


def show_athletes(cursor):
    print("\n--- Athletes ---")
    cursor.execute("SELECT * FROM athletes;")
    for row in cursor.fetchall():
        print(row)


def show_workouts(cursor):
    print("\n--- Workout ---")
    cursor.execute("SELECT * FROM workout;")
    for row in cursor.fetchall():
        print(row)


def show_sets(cursor):
    print("\n--- Workout Sets (with exercise names) ---")
    cursor.execute(
        """
        SELECT ws.set_id, e.exercise_name, ws.reps, ws.weight_amount, ws.rpe, ws.rir, ws.rest_time
        FROM workout_sets ws
        JOIN exercises e ON ws.exercise_id = e.exercise_id;
        """
    )
    for row in cursor.fetchall():
        print(row)


def main():
    conn = get_connection()
    cursor = conn.cursor()

    show_tables(cursor)
    show_athletes(cursor)
    show_workouts(cursor)
    show_sets(cursor)

    conn.close()


if __name__ == "__main__":
    main()