import sqlite3

def setup_database():
    conn = sqlite3.connect('video_detection.db')
    c = conn.cursor()

    # Create tables
    c.execute('''CREATE TABLE IF NOT EXISTS detection
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  class TEXT,
                  timestamp DATETIME)''')

    c.execute('''CREATE TABLE IF NOT EXISTS counting
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  class TEXT,
                  count INTEGER,
                  timestamp DATETIME)''')

    c.execute('''CREATE TABLE IF NOT EXISTS speed
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  class TEXT,
                  speed FLOAT,
                  timestamp DATETIME)''')

    c.execute('''CREATE TABLE IF NOT EXISTS number_plate
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  class TEXT,
                  plate_text TEXT,
                  timestamp DATETIME)''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_database()