import sqlite3
import json
# Connect to database
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Create users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

# Create history table
cursor.execute("""
CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_email TEXT NOT NULL,
    disease TEXT,
    confidence REAL,
    image TEXT,
    date TEXT,
    FOREIGN KEY (user_email) REFERENCES users(email)
)
""")

# Save changes
conn.commit()
conn.close()

print("Database created successfully!")