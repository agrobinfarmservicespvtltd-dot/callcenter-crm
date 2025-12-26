import sqlite3

def init_db():
    conn = sqlite3.connect("crm.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS calls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT,
        phone_number TEXT,
        agent_name TEXT,
        call_status TEXT,
        notes TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS agents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    # default agent (first time)
    cursor.execute("""
    INSERT OR IGNORE INTO agents (username, password)
    VALUES ('agent1', '1234')
    """)

    conn.commit()
    conn.close()