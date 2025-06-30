import sqlite3

# Paths
db_path = "data/trendpulse.db"
schema_path = "src/db/schema.sql"

try:
    conn = sqlite3.connect(db_path)
    with open(schema_path, "r") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()

    print("Database initialized using schema.sql")

except Exception as e:
    print(e)


