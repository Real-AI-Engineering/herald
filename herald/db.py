from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path


_SCHEMA = Path(__file__).parent / "schema.sql"


class Database:
    def __init__(self, path: Path) -> None:
        if not path.parent.exists():
            raise FileNotFoundError(f"Parent directory does not exist: {path.parent}")
        self._conn = sqlite3.connect(str(path), isolation_level=None)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute("PRAGMA foreign_keys=ON")
        self._conn.execute("PRAGMA busy_timeout=5000")
        self._apply_schema()

    def _apply_schema(self) -> None:
        schema = _SCHEMA.read_text()
        self._conn.executescript(schema)

    def execute(self, sql: str, params: tuple = ()) -> sqlite3.Cursor:
        return self._conn.execute(sql, params)

    def executemany(self, sql: str, params) -> sqlite3.Cursor:
        return self._conn.executemany(sql, params)

    @contextmanager
    def transaction(self):
        self._conn.execute("BEGIN IMMEDIATE")
        try:
            yield self._conn
            self._conn.execute("COMMIT")
        except Exception:
            self._conn.execute("ROLLBACK")
            raise

    def close(self) -> None:
        self._conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False
