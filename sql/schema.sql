PRAGMA foreign_keys = ON; -- This enforces foreign key constraints

CREATE TABLE IF NOT EXISTS athletes (
    -- Gives a unique ID to each athlete in auto-increments and the datatype is an int.
    -- This is the primary key (row identifier)
    athlete_id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name TEXT NOT NULL, -- name must exist (can't be NULL) and the datatype is text.
    age INTEGER,
    bodyweight_lbs REAL, -- The datatype is a float (REAL)
    training_experience_years REAL,
    preferred_units TEXT DEFUALT 'lbs', -- If user doesn't specify then the default is lbs because we are in America lol
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Automatically records when row is created (useful for tracking history, time-based analysis)
);

CREATE TABLE IF NOT EXISTS exercises (
    exercise_id INTEGER PRIMARY KEY AUTOINCREMENT,
    exercise_name TEXT NOT NULL UNIQUE, -- Unique means that no duplicates are allowed 
    movement_category TEXT NOT NULL -- Is the movement a squat, bench, deadlift, accessory?
);

CREATE TABLE IF NOT EXISTS workout (
    workout_id INTEGER PRIMARY KEY AUTOINCREMENT,
    athlete_id INTEGER NOT NULL,
    workout_date DATE NOT NULL,
    session_type TEXT, -- push/pull/legs/upper body/ etc.
    duration_minutes INTEGER, -- User interface idea: this gets filled in automatically based on when he user starts and ends there workout and there should be a button for this.
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (athlete_id) REFERENCES athletes(athlete_id) -- enoforces that every workout must belong to a real athlete
   
);

CREATE TABLE IF NOT EXISTS workout_sets (
    set_id INTEGER PRIMARY KEY AUTOINCREMENT,
    workout_id INTEGER NOT NULL,
    exercise_id INTEGER NOT NULL,
    set_number INTEGER NOT NULL,
    reps INTEGER NOT NULL,
    weight_amount REAL NOT NULL,
    rpe REAL,
    rir REAL, 
    completed_flag INTEGER DEFAULT 1, -- 1 is completed, 0 is failed
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (workout_id) REFERENCES workouts(workout_id),
    FOREIGN KEY (exercise_id) REFERENCES exercises(exercise_id)
);

CREATE TABLE IF NOT EXISTS readiness_logs (
    readiness_id INTEGER PRIMARY KEY AUTOINCREMENT,
    athlete_id INTEGER NOT NULL,
    log_date DATE NOT NULL,
    sleep_hours REAL,
    fatigue_rating INTEGER,
    soreness_rating INTEGER,
    stress_rating INTEGER,
    motivation_rating INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (athlete_id) REFERENCES athletes(athlete_id)
);
