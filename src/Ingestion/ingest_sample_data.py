#Goal: This script connects to the database and inserts sample data to ensure that 
#the database and inserting into it from python works

from pathlib import Path
import sqlite3


def get_connection() -> sqlite3.Connection:
    """Create and return a connection to the SQLite database."""
    project_root = Path(__file__).resolve().parents[2]
    db_path = project_root / "powerlifting.db"
    conn = sqlite3.connect(db_path) #Creates connection to the database 
    conn.execute("PRAGMA foreign_keys = ON;") #Turns on foreign key enforcement 
    #SQLite will pay attention to relational rules
    return conn

def insert_athlete(conn: sqlite3.Connection) -> int:
    """Insert one sample athlete and return the athlete.id"""
    cursor = conn.cursor() #Use cursor to send SQL commands to the database
    cursor.execute(
        """
        INSERT INTO athletes (
            name,
            age,
            bodyweight_lbs,
            training_experience_years,
            preferred_units
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        ("Farah", 22, 150, 7, "lbs")
    )
    athlete_id = cursor.lastrowid #Grabs the id of the row that was just inserted 
    print(f"Inserted athlete with athlete_id={athlete_id}")
    return athlete_id

def seed_exercises(conn: sqlite3.Connection) -> None:
    """Insert a few common exercises into the exercise table"""
    cursor = conn.cursor()
    exercises = [
        ("Back Squat", "squat"),
        ("Bench Press", "bench"),
        ("Romanian Deadlift", "deadlift"),
        ("Overhead Press", "accessory"),
    ]
    cursor.executemany(
        """
        INSERT OR IGNORE INTO exercises (exercise_name, movement_category)
        VALUES (?, ?)
        """,
        exercises
    )

    print("Seeded exercises table.")

def get_exercise_id(conn: sqlite3.Connection, exercise_name: str) -> int:
    """Look up and return an exercise_id by exercise name."""
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT exercise_id
        FROM exercises
        WHERE exercise_name = ?
        """,
        (exercise_name,)
    )

    row = cursor.fetchone()  # correct spelling

    if row is None:
        raise ValueError(f"Exercise '{exercise_name}' not found in exercises table.")

    return row[0]

def insert_workout(conn: sqlite3.Connection, athlete_id: int) -> int:
    """Insert one workout and return the workout_id."""
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO workout (
            athlete_id,
            workout_date,
            session_type,
            duration_minutes,
            notes
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (athlete_id, "2026-03-25", "Lower Body", 90, "Felt solid overall.")
    )

    workout_id = cursor.lastrowid
    print(f"Inserted workout with workout_id={workout_id}")
    return workout_id

def insert_workout_sets(conn: sqlite3.Connection, workout_id: int) -> None:
    """Insert sample workout sets for a workout."""
    cursor = conn.cursor()

    squat_id = get_exercise_id(conn, "Back Squat")
    bench_id = get_exercise_id(conn, "Bench Press")

    sets_to_insert = [
        (workout_id, squat_id, 1, 5, 100.0, 7.5, 2.5, 3, 1),
        (workout_id, squat_id, 2, 5, 105.0, 8.0, 2, 3, 1),
        (workout_id, squat_id, 3, 5, 107.5, 8.5, 1.5, 3, 1),
        (workout_id, bench_id, 1, 5, 60.0, 7.0, 3, 2, 1),
        (workout_id, bench_id, 2, 5, 62.5, 7.5, 2.5, 2, 1),
        (workout_id, bench_id, 3, 5, 65.0, 8.0, 2, 2, 1),
    ]

    cursor.executemany(
        """
        INSERT INTO workout_sets (
            workout_id,
            exercise_id,
            set_number,
            reps,
            weight_amount,
            rpe,
            rir, 
            rest_time, 
            completed_flag
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        sets_to_insert
    )

    print("Inserted workout sets.")

def insert_readiness_log(conn: sqlite3.Connection, athlete_id: int) -> None:
    """Insert one sample readiness log."""
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO readiness_logs (
            athlete_id,
            log_date,
            sleep_hours,
            fatigue_rating,
            soreness_rating,
            stress_rating,
            motivation_rating
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (athlete_id, "2026-03-25", 7.5, 4, 3, 2, 8)
    )

    print("Inserted readiness log.")

def main() -> None:
    conn = get_connection()

    try:
        athlete_id = insert_athlete(conn)
        seed_exercises(conn)
        workout_id = insert_workout(conn, athlete_id)
        insert_workout_sets(conn, workout_id)
        insert_readiness_log(conn, athlete_id)

        conn.commit()
        print("Sample data ingestion completed successfully.")

    except Exception as e:
        conn.rollback()
        print(f"Error during ingestion: {e}")
        raise

    finally:
        conn.close()


if __name__ == "__main__":
    main()

