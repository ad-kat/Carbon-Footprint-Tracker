from sqlalchemy import create_engine, text
from datetime import datetime
import os

db_string = "sqlite:///carbon_footprint.db"
engine = create_engine(db_string)

def init_db():
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                fullname TEXT,
                email_id TEXT
            )
        """))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS carbon_footprint (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                carbon_emission REAL,
                measurement_date TEXT
            )
        """))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS household_data (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                total_members INTEGER,
                house_size REAL,
                waste_production REAL
            )
        """))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS daily_activities (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                wastepoints REAL,
                drivekms REAL,
                meal TEXT,
                laundry TEXT,
                utensils TEXT,
                date TEXT
            )
        """))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS offsets (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                walk TEXT,
                carpool TEXT,
                cycle TEXT,
                tree TEXT,
                pubtrans TEXT,
                recycle TEXT,
                cleanup TEXT,
                date TEXT
            )
        """))
        # Seed a default user so the app doesn't break
        existing = conn.execute(text("SELECT * FROM users WHERE user_id=1")).fetchone()
        if not existing:
            conn.execute(text("""
                INSERT INTO users (user_id, username, fullname, email_id)
                VALUES (1, 'demo', 'Demo User', 'demo@example.com')
            """))
            conn.execute(text("""
                INSERT INTO carbon_footprint (user_id, carbon_emission, measurement_date)
                VALUES (1, 0.0, '2024-01-01')
            """))
            conn.execute(text("""
                INSERT INTO household_data (user_id, total_members, house_size, waste_production)
                VALUES (1, 1, 0.0, 0.0)
            """))
        conn.commit()

# Initialize on import
init_db()


def load_basicinfo_from_db():
    with engine.connect() as conn:
        query = """SELECT users.user_id, username, fullname, email_id,
                   carbon_emission, measurement_date, total_members,
                   house_size, waste_production
                   FROM users, carbon_footprint, household_data
                   WHERE users.user_id=1
                   AND carbon_footprint.user_id=1
                   AND household_data.user_id=1"""
        result = conn.execute(text(query))
        finfo = []
        for row in result.all():
            finfo.append([str(item) for item in row])
        return finfo


def load_users_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM users"))
        return [list(row) for row in result.all()]


def load_activities_from_db():
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM daily_activities WHERE user_id=1"))
        fdata = []
        for row in result.all():
            fdata.append([str(item) for item in row])
        return fdata


def load_offsets_from_db():
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM offsets WHERE user_id=1"))
        fdata = []
        for row in result.all():
            fdata.append([str(item) for item in row])
        return fdata


def upload_offsets(data):
    with engine.connect() as conn:
        date = datetime.now().strftime('%Y-%m-%d')
        conn.execute(text("""
            INSERT INTO offsets
            (user_id, walk, carpool, cycle, tree, pubtrans, recycle, cleanup, date)
            VALUES (1, :walk, :carpool, :cycle, :tree, :pubtrans, :recycle, :cleanup, :date)
        """), {**data, 'date': date})
        conn.commit()


def upload_today(data):
    with engine.connect() as conn:
        date = datetime.now().strftime('%Y-%m-%d')
        conn.execute(text("""
            INSERT INTO daily_activities
            (user_id, wastepoints, drivekms, meal, laundry, utensils, date)
            VALUES (1, :waste, :kms, :meal, :laundry, :utensils, :date)
        """), {**data, 'date': date})
        conn.commit()
