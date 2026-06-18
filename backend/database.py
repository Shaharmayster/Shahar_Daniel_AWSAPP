import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from config import DATABASE_URL

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _get_sqlite_path():
    if not DATABASE_URL.startswith("sqlite:///"):
        raise ValueError(
            "Phase 1 supports SQLite only. Set DATABASE_URL to sqlite:///local.db"
        )

    db_path = DATABASE_URL[len("sqlite:///") :]
    path = Path(db_path)
    if path.is_absolute():
        return path
    return PROJECT_ROOT / path


def _get_connection():
    db_path = _get_sqlite_path()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = _get_connection()
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS greetings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                greeting_type TEXT NOT NULL,
                recipient TEXT NOT NULL,
                grandma_style TEXT NOT NULL,
                generated_text TEXT NOT NULL
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


def save_greeting(greeting_type, recipient, grandma_style, generated_text):
    created_at = datetime.now(timezone.utc).isoformat()
    conn = _get_connection()
    try:
        conn.execute(
            """
            INSERT INTO greetings (
                created_at, greeting_type, recipient, grandma_style, generated_text
            ) VALUES (?, ?, ?, ?, ?)
            """,
            (created_at, greeting_type, recipient, grandma_style, generated_text),
        )
        conn.commit()
    finally:
        conn.close()


def get_recent_greetings(limit=20):
    conn = _get_connection()
    try:
        rows = conn.execute(
            """
            SELECT id, created_at, greeting_type, recipient, grandma_style, generated_text
            FROM greetings
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()
