import sqlite3
import os


# --- Helper Utilities ---

def get_user_avatar(username):
    """Returns the path to the user's avatar if it exists, otherwise returns a default."""
    pic_dir = os.path.join("uploads", "profile_pics")
    if not os.path.exists(pic_dir):
        os.makedirs(pic_dir)
    for ext in ["png", "jpg", "jpeg"]:
        path = os.path.join(pic_dir, f"{username}.{ext}")
        if os.path.exists(path):
            return path
    return "https://cdn-icons-png.flaticon.com/512/149/149071.png"


def get_connection():
    """Returns a direct relational connection handle to the database file."""
    return sqlite3.connect("learn_ai.db")


# --- Database Initialization ---

def initialize_database():
    """Creates the structural tables required by the platform if they don't exist."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        fullname TEXT NOT NULL,
        role TEXT NOT NULL,
        xp INTEGER DEFAULT 0,
        streak INTEGER DEFAULT 0
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS lessons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT UNIQUE NOT NULL,
        description TEXT NOT NULL,
        difficulty TEXT NOT NULL,
        duration TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS lesson_attachments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lesson_id INTEGER NOT NULL,
        file_name TEXT NOT NULL,
        file_type TEXT NOT NULL,
        file_path_or_url TEXT NOT NULL,
        FOREIGN KEY (lesson_id) REFERENCES lessons(id) ON DELETE CASCADE
    )
    """)

    conn.commit()
    conn.close()


def seed_lessons():
    """Performs an idempotent injection of official GES ICT curriculum items."""
    conn = get_connection()
    cursor = conn.cursor()
    official_syllabus_modules = [
        ("Introduction to Computing", "Explore the fundamental IPOS cycle.", "Beginner", "15 mins"),
        ("Information and Communication Technology (ICT)", "Analyze core IT infrastructures.", "Beginner", "20 mins"),
        ("Relational Database Concepts", "Introduction to structural database designs.", "Intermediate", "35 mins"),
        ("Internet Architectures & Topologies", "Deconstruct global internet infrastructure.", "Intermediate",
         "25 mins"),
        ("Basic Algorithm Design & Logic", "Understand foundational computing logic patterns.", "Advanced", "40 mins")
    ]
    for module in official_syllabus_modules:
        cursor.execute("INSERT OR IGNORE INTO lessons (title, description, difficulty, duration) VALUES (?, ?, ?, ?)",
                       module)
    conn.commit()
    conn.close()


# --- CRUD Operations ---

def get_all_lessons():
    """Retrieves all available lessons from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, description, difficulty, duration FROM lessons")
    results = cursor.fetchall()
    conn.close()
    return results


def update_lesson_in_db(lesson_id, title, description, difficulty, duration):
    """Updates an existing lesson record in the database."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE lessons 
            SET title = ?, description = ?, difficulty = ?, duration = ? 
            WHERE id = ?
        """, (title, description, difficulty, duration, lesson_id))
        conn.commit()
        conn.close()
        return True, "Updated successfully!"
    except Exception as e:
        return False, f"Database error: {e}"


def delete_lesson_from_db(lesson_id):
    """Deletes a lesson and its associated attachments."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        # Delete attachments first to maintain referential integrity
        cursor.execute("DELETE FROM lesson_attachments WHERE lesson_id = ?", (lesson_id,))
        cursor.execute("DELETE FROM lessons WHERE id = ?", (lesson_id,))
        conn.commit()
        conn.close()
        return True, "Lesson deleted successfully!"
    except Exception as e:
        return False, f"Database error: {e}"


def add_lesson_attachment(lesson_id, file_name, file_type, path_or_url):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO lesson_attachments (lesson_id, file_name, file_type, file_path_or_url) VALUES (?, ?, ?, ?)",
        (lesson_id, file_name, file_type, path_or_url))
    conn.commit()
    conn.close()


def get_lesson_attachments(lesson_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, lesson_id, file_name, file_type, file_path_or_url FROM lesson_attachments WHERE lesson_id = ?",
        (lesson_id,))
    results = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "lesson_id": r[1], "file_name": r[2], "file_type": r[3], "file_path_or_url": r[4]} for r in
            results]


# --- Game Logic ---

def update_user_xp(username, xp_to_add):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT xp FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    if row:
        new_xp = row[0] + xp_to_add
        cursor.execute("UPDATE users SET xp = ? WHERE username = ?", (new_xp, username))
        conn.commit()
    conn.close()


def increment_user_streak(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT streak FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    if row:
        new_streak = row[0] + 1
        cursor.execute("UPDATE users SET streak = ? WHERE username = ?", (new_streak, username))
        conn.commit()
    conn.close()


def save_user_quiz_results(username, xp_to_add):
    """
    Saves new XP to the database and cleanly increments user streaks.
    Also returns the updated statistics so Streamlit session state matches perfectly.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Update XP
    cursor.execute("SELECT xp, streak FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    if row:
        old_xp, old_streak = row[0], row[1]
        new_xp = old_xp + xp_to_add
        # Automatically bump streak on quiz completion to reward active daily habits
        new_streak = old_streak + 1

        cursor.execute("""
            UPDATE users 
            SET xp = ?, streak = ? 
            WHERE username = ?
        """, (new_xp, new_streak, username))
        conn.commit()
        conn.close()
        return new_xp, new_streak

    conn.close()
    return 0, 0