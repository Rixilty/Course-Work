import sqlite3

def create_database():
    # This connects to the database/create one if it doesn't already exist
    conn = sqlite3.connect("messages.db")
    cursor = conn.cursor()

    # Create table
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender TEXT NOT NULL,
        message TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        '''
    )

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()