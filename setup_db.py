import sqlite3

conn = sqlite3.connect("vulnerable_social.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);
""")

cursor.execute("""
CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    likes INTEGER DEFAULT 0
);
""")

cursor.execute("""
CREATE TABLE follows (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    follower_id INTEGER NOT NULL,
    followed_id INTEGER NOT NULL
);
""")

default_users = [
    ("admin", "admin"),
    ("alice", "alice"),
    ("bob", "bob")
]

for user in default_users:
    cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", user)

conn.commit()
conn.close()

print("Database setup complete!")
