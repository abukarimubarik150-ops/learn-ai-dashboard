import sqlite3
from database import get_connection


def register_user(username, password, fullname, role):
    """Registers a new user into the database if the username doesn't already exist."""
    if not username or not password or not fullname:
        return False, "All fields are required."

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Check if username already exists
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        if cursor.fetchone() is not None:
            conn.close()
            return False, "Username already taken. Please choose another."

        # Insert new user with default XP (0) and Streak (0)
        cursor.execute("""
            INSERT INTO users (username, password, fullname, role, xp, streak)
            VALUES (?, ?, ?, ?, 0, 0)
        """, (username, password, fullname, role))

        conn.commit()
        conn.close()
        return True, "Account created successfully! Please switch to the Login tab."

    except Exception as e:
        return False, f"Registration error: {e}"


def login_user(username, password):
    """Authenticates an existing user and returns their profile details."""
    if not username or not password:
        return False, "Please enter both username and password."

    try:
        conn = get_connection()

        # CRITICAL FIX: Forces sqlite3 to return rows that accept string index keys!
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Query the user record
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user is None:
            return False, "Username not found."

        # Direct password match verification
        if password == user["password"]:
            return True, {
                "username": user["username"],
                "fullname": user["fullname"],
                "role": user["role"],
                "xp": user["xp"],
                "streak": user["streak"]
            }
        else:
            return False, "Incorrect password."

    except Exception as e:
        return False, f"Authentication error: {e}"