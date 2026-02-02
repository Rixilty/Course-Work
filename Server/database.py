import sqlite3

def create_database():
    # This connects to the database/create one if it doesn't already exist
    conn = sqlite3.connect("logins.db")
    cursor = conn.cursor()

    # Create table
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS logins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
        )
        '''
    )
    # I used "UNIQUE" for username so no 2 people can have the same username

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()