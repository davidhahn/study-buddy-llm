import os
from dotenv import load_dotenv
import sqlite3

load_dotenv()


def init_db():
    db_path = os.environ.get("DB_PATH", "")
    connection = sqlite3.connect(db_path)

    with open("db/schema.sql", "r") as f:
        schema = f.read()

    connection.executescript(schema)
    connection.commit()
    connection.close()


if __name__ == "__main__":
    init_db()
