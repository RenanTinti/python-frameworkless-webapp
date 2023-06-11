import sqlite3


def set_database():
    conn = sqlite3.connect("feedback.db")
    c = conn.cursor()

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            type TEXT,
            content TEXT
        )
    """
    )
    conn.commit()


if __name__ == "__main__":
    set_database()
