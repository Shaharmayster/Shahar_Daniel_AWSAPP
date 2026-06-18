import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote, urlparse

from config import DATABASE_URL

PROJECT_ROOT = Path(__file__).resolve().parent.parent

SQLITE_DDL = """
CREATE TABLE IF NOT EXISTS greetings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT NOT NULL,
    greeting_type TEXT NOT NULL,
    recipient TEXT NOT NULL,
    grandma_style TEXT NOT NULL,
    generated_text TEXT NOT NULL
)
"""

MYSQL_DDL = """
CREATE TABLE IF NOT EXISTS greetings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    created_at VARCHAR(64) NOT NULL,
    greeting_type VARCHAR(255) NOT NULL,
    recipient VARCHAR(255) NOT NULL,
    grandma_style VARCHAR(255) NOT NULL,
    generated_text TEXT NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
"""


def _is_mysql():
    return DATABASE_URL.startswith("mysql://")


def _is_sqlite():
    return DATABASE_URL.startswith("sqlite:///")


def _get_sqlite_path():
    db_path = DATABASE_URL[len("sqlite:///") :]
    path = Path(db_path)
    if path.is_absolute():
        return path
    return PROJECT_ROOT / path


def _get_mysql_connection():
    import pymysql

    parsed = urlparse(DATABASE_URL)
    database = parsed.path.lstrip("/")
    if not database:
        raise ValueError("MySQL DATABASE_URL must include a database name")

    return pymysql.connect(
        host=parsed.hostname,
        port=parsed.port or 3306,
        user=parsed.username,
        password=unquote(parsed.password or ""),
        database=database,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )


def _get_connection():
    if _is_sqlite():
        db_path = _get_sqlite_path()
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn
    if _is_mysql():
        return _get_mysql_connection()
    raise ValueError(
        "Unsupported DATABASE_URL. Use sqlite:///local.db or mysql://user:pass@host:3306/db"
    )


def _prepare_sql(sql):
    if _is_mysql():
        return sql.replace("?", "%s")
    return sql


def _execute(conn, sql, params=()):
    sql = _prepare_sql(sql)
    if _is_mysql():
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
        return
    conn.execute(sql, params)


def _fetchall(conn, sql, params=()):
    sql = _prepare_sql(sql)
    if _is_mysql():
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()
    rows = conn.execute(sql, params).fetchall()
    return [dict(row) for row in rows]


def init_db():
    conn = _get_connection()
    try:
        ddl = MYSQL_DDL if _is_mysql() else SQLITE_DDL
        _execute(conn, ddl)
        conn.commit()
    finally:
        conn.close()


def save_greeting(greeting_type, recipient, grandma_style, generated_text):
    created_at = datetime.now(timezone.utc).isoformat()
    conn = _get_connection()
    try:
        _execute(
            conn,
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
        return _fetchall(
            conn,
            """
            SELECT id, created_at, greeting_type, recipient, grandma_style, generated_text
            FROM greetings
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        )
    finally:
        conn.close()
