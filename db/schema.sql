CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic TEXT NOT NULL,
    difficulty TEXT NOT NULL,
    exercise_type TEXT NOT NULL,
    language TEXT NOT NULL,
    total_score REAL NOT NULL,
    max_score INTEGER NOT NULL,
    is_uncertain BOOLEAN NOT NULL,
    summary TEXT NOT NULL,
    answer TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS failed_criteria (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER NOT NULL REFERENCES sessions(id),
    criterion_id TEXT NOT NULL,
    label TEXT NOT NULL,
    points_possible INTEGER NOT NULL,
    reasoning TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
