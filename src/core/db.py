import sqlite3
import os
from pathlib import Path

DB_NAME = "database.db"

def get_db_path() -> Path:
    storage = os.getenv("FLET_APP_STORAGE_DATA")
    base = Path(storage) if storage else Path(__file__).resolve().parent / "data"
    base.mkdir(parents=True, exist_ok=True)
    return base / DB_NAME

SCHEMA = """
CREATE TABLE IF NOT EXISTS books (
    id             INTEGER PRIMARY KEY,
    title          TEXT    NOT NULL,
    description    TEXT,
    page_count     INTEGER,
    isbn           TEXT,
    language       TEXT,
    published_year INTEGER,
    cover_url      TEXT,
    cover_path     TEXT,
    spine_color    TEXT,
    status         TEXT    NOT NULL DEFAULT 'want'
                           CHECK (status IN ('want', 'reading', 'read')),
    rating         INTEGER CHECK (rating BETWEEN 1 AND 5),
    finished_at    TEXT,
    note           TEXT,
    source         TEXT,
    external_id    TEXT,
    created_at     TEXT    NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS authors (
    id   INTEGER PRIMARY KEY,
    name TEXT    NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS book_authors (
    book_id   INTEGER NOT NULL REFERENCES books(id)   ON DELETE CASCADE,
    author_id INTEGER NOT NULL REFERENCES authors(id) ON DELETE CASCADE,
    position  INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (book_id, author_id)
);

CREATE TABLE IF NOT EXISTS shelves (
    id       INTEGER PRIMARY KEY,
    name     TEXT    NOT NULL,
    kind     TEXT    NOT NULL,
    position INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS shelf_items (
    id           INTEGER PRIMARY KEY,
    shelf_id     INTEGER NOT NULL REFERENCES shelves(id) ON DELETE CASCADE,
    kind         TEXT    NOT NULL CHECK (kind IN ('book', 'decor')),
    book_id      INTEGER UNIQUE REFERENCES books(id) ON DELETE CASCADE,
    decor_type   TEXT,
    position     INTEGER NOT NULL,
    display_mode TEXT    NOT NULL DEFAULT 'spine'
                         CHECK (display_mode IN ('spine', 'cover')),
    CHECK (
        (kind = 'book'  AND book_id IS NOT NULL AND decor_type IS NULL)
        OR
        (kind = 'decor' AND book_id IS NULL AND decor_type IS NOT NULL)
    )
);

CREATE TABLE IF NOT EXISTS settings (
    key   TEXT PRIMARY KEY,
    value TEXT
);

CREATE INDEX IF NOT EXISTS idx_books_status      ON books(status);
CREATE INDEX IF NOT EXISTS idx_shelf_items_shelf ON shelf_items(shelf_id);
"""


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(get_db_path())
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = get_connection()
    try:
        conn.executescript(SCHEMA)
        conn.commit()
    finally:
        conn.close()