import sqlite3
import os
from datetime import datetime


DB_PATH = "data/autitrack.db"


def initialize_database():

    os.makedirs(
        "data",
        exist_ok=True
    )

    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS observations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            observation TEXT NOT NULL,
            context TEXT,
            activity TEXT,
            domains TEXT,
            observed_behavior TEXT,
            trigger TEXT,
            summary TEXT,
            created_at TEXT
        )
        """
    )

    connection.commit()

    connection.close()


def add_observation(
    date,
    observation,
    context,
    activity,
    domains,
    observed_behavior,
    trigger,
    summary
):

    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO observations (
            date,
            observation,
            context,
            activity,
            domains,
            observed_behavior,
            trigger,
            summary,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            date,
            observation,
            context,
            activity,
            "|".join(domains),
            "|".join(observed_behavior),
            trigger,
            summary,
            datetime.now().isoformat(),
        )
    )

    connection.commit()

    connection.close()


def get_observations():

    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            date,
            observation,
            context,
            activity,
            domains,
            observed_behavior,
            trigger,
            summary,
            created_at
        FROM observations
        ORDER BY date DESC
        """
    )

    rows = cursor.fetchall()

    connection.close()

    columns = [
        "id",
        "date",
        "observation",
        "context",
        "activity",
        "domains",
        "observed_behavior",
        "trigger",
        "summary",
        "created_at",
    ]

    return rows, columns
