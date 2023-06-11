import sqlite3


def clear_database():
    conn = sqlite3.connect("feedback.db")
    c = conn.cursor()

    c.execute("DELETE FROM feedback")
    conn.commit()

    conn.close()


if __name__ == "__main__":
    clear_database()
