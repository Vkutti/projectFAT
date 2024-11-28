import sqlite3

# Connect to SQLite database
connection = sqlite3.connect("FAT.db")
cursor = connection.cursor()

# Create a table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# Insert some data
cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("John Doe", 30))
cursor.executemany("INSERT INTO users (name, age) VALUES (?, ?)", [("Alice", 25), ("Bob", 22)])

# Commit changes
connection.commit()

# Query and print data
cursor.execute("SELECT * FROM users")
for row in cursor.fetchall():
    print(row)

# Update a user's age
cursor.execute("UPDATE users SET age = ? WHERE name = ?", (35, "John Doe"))
connection.commit()

# Delete a user
cursor.execute("DELETE FROM users WHERE name = ?", ("Alice",))
connection.commit()

# Close connection
connection.close()
