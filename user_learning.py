import sqlite3

class UserLearning:
    def __init__(self, db_name="user_errors.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS errors (
                word TEXT PRIMARY KEY,
                correction TEXT,
                frequency INTEGER DEFAULT 1
            )
        """)
        self.conn.commit()
    
    def log_error(self, incorrect, correct):
        self.cursor.execute("SELECT frequency FROM errors WHERE word = ?", (incorrect,))
        row = self.cursor.fetchone()
        if row:
            self.cursor.execute("UPDATE errors SET frequency = frequency + 1 WHERE word = ?", (incorrect,))
        else:
            self.cursor.execute("INSERT INTO errors (word, correction, frequency) VALUES (?, ?, 1)", (incorrect, correct))
        self.conn.commit()
    
    def get_correction(self, word):
        self.cursor.execute("SELECT correction FROM errors WHERE word = ?", (word,))
        row = self.cursor.fetchone()
        return row[0] if row else None
