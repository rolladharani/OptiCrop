import sqlite3
import os
from werkzeug.security import generate_password_hash

DB_PATH = 'opticrop.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON;")

    # 1. Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'Farmer'
        )
    ''')

    # 2. SoilData Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS soil_data (
            soil_id INTEGER PRIMARY KEY AUTOINCREMENT,
            nitrogen REAL NOT NULL,
            phosphorous REAL NOT NULL,
            potassium REAL NOT NULL,
            temperature REAL NOT NULL,
            humidity REAL NOT NULL,
            ph REAL NOT NULL,
            rainfall REAL NOT NULL,
            season TEXT,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL
        )
    ''')

    # 3. Crops Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS crops (
            crop_id INTEGER PRIMARY KEY AUTOINCREMENT,
            crop_name TEXT NOT NULL UNIQUE,
            crop_type TEXT,
            season TEXT,
            optimal_ph REAL,
            water_requirement REAL
        )
    ''')

    # 4. Datasets Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS datasets (
            dataset_id INTEGER PRIMARY KEY AUTOINCREMENT,
            dataset_name TEXT NOT NULL,
            source TEXT,
            total_records INTEGER,
            last_updated TEXT
        )
    ''')

    # 5. MLModels Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ml_models (
            model_id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_name TEXT NOT NULL,
            accuracy REAL,
            dataset_id INTEGER,
            FOREIGN KEY (dataset_id) REFERENCES datasets(dataset_id) ON DELETE CASCADE
        )
    ''')

    # 6. Predictions Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            prediction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            soil_id INTEGER,
            crop_id INTEGER,
            model_id INTEGER,
            prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            confidence_score REAL,
            FOREIGN KEY (soil_id) REFERENCES soil_data(soil_id) ON DELETE CASCADE,
            FOREIGN KEY (crop_id) REFERENCES crops(crop_id) ON DELETE CASCADE,
            FOREIGN KEY (model_id) REFERENCES ml_models(model_id) ON DELETE CASCADE
        )
    ''')

    # 7. Reports Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            report_id INTEGER PRIMARY KEY AUTOINCREMENT,
            prediction_id INTEGER,
            summary TEXT,
            recommendations TEXT,
            FOREIGN KEY (prediction_id) REFERENCES predictions(prediction_id) ON DELETE CASCADE
        )
    ''')

    # Insert default admin user if not exists
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        hashed_pw = generate_password_hash('admin123')
        cursor.execute("INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)",
                       ('admin', 'admin@opticrop.org', hashed_pw, 'Researcher'))

    # Insert default dataset metadata if not exists
    cursor.execute("SELECT * FROM datasets WHERE dataset_name LIKE '%Agricultural%'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO datasets (dataset_name, source, total_records, last_updated) VALUES (?, ?, ?, ?)",
                       ('Smart Agricultural Production Optimizing Engine', 'Kaggle (chitrakumari25)', 2200, '2026-07-04'))
        dataset_id = cursor.lastrowid
    else:
        cursor.execute("SELECT dataset_id FROM datasets WHERE dataset_name LIKE '%Agricultural%'")
        dataset_id = cursor.fetchone()[0]

    # Insert default ML models metadata
    cursor.execute("SELECT * FROM ml_models WHERE model_name = 'Logistic Regression'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO ml_models (model_name, accuracy, dataset_id) VALUES (?, ?, ?)",
                       ('Logistic Regression', 0.94, dataset_id))
        cursor.execute("INSERT INTO ml_models (model_name, accuracy, dataset_id) VALUES (?, ?, ?)",
                       ('K-Means Clustering', None, dataset_id))

    # Insert default crops lists
    default_crops = [
        ('rice', 'Rainy', 'Rainy', 6.5, 200.0),
        ('maize', 'Grain', 'Winter', 6.2, 100.0),
        ('chickpea', 'Pulse', 'Winter', 7.0, 60.0),
        ('kidneybeans', 'Pulse', 'Winter', 5.8, 80.0),
        ('pigeonpeas', 'Pulse', 'Summer', 6.8, 120.0),
        ('mothbeans', 'Pulse', 'Summer', 7.2, 50.0),
        ('mungbean', 'Pulse', 'Summer', 6.9, 65.0),
        ('blackgram', 'Pulse', 'Summer', 7.1, 70.0),
        ('lentil', 'Pulse', 'Winter', 6.4, 75.0),
        ('pomegranate', 'Fruit', 'Winter', 6.3, 110.0),
        ('banana', 'Fruit', 'Summer/Rainy', 6.0, 150.0),
        ('mango', 'Fruit', 'Summer', 5.7, 90.0),
        ('grapes', 'Fruit', 'Summer/Winter', 6.0, 80.0),
        ('watermelon', 'Fruit', 'Summer', 5.9, 70.0),
        ('muskmelon', 'Fruit', 'Summer', 6.2, 60.0),
        ('apple', 'Fruit', 'Winter', 5.8, 120.0),
        ('orange', 'Fruit', 'Winter/Summer', 6.0, 110.0),
        ('papaya', 'Fruit', 'Summer/Rainy', 6.4, 130.0),
        ('coconut', 'Fruit', 'Rainy', 6.0, 220.0),
        ('cotton', 'Fiber', 'Summer', 6.5, 90.0),
        ('jute', 'Fiber', 'Rainy', 6.8, 180.0),
        ('coffee', 'Beverage', 'Summer', 6.2, 150.0)
    ]

    for crop_info in default_crops:
        cursor.execute("SELECT * FROM crops WHERE crop_name = ?", (crop_info[0],))
        if not cursor.fetchone():
            cursor.execute("INSERT INTO crops (crop_name, crop_type, season, optimal_ph, water_requirement) VALUES (?, ?, ?, ?, ?)",
                           crop_info)

    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == '__main__':
    init_db()
