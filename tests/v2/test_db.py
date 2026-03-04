from __future__ import annotations

import sqlite3
import tempfile
from pathlib import Path

import pytest

from herald.db import Database


@pytest.fixture
def db(tmp_path):
    d = Database(tmp_path / "test.db")
    yield d
    d.close()


def test_database_creates_tables(db):
    tables = {
        row[0]
        for row in db.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
    }
    required = {
        "sources",
        "articles",
        "mentions",
        "article_topics",
        "stories",
        "story_articles",
        "story_topics",
        "pipeline_runs",
    }
    assert required.issubset(tables), f"Missing tables: {required - tables}"


def test_database_creates_fts(db):
    vtables = {
        row[0]
        for row in db.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
    }
    assert "articles_fts" in vtables
    assert "stories_fts" in vtables


def test_database_foreign_keys_enabled(db):
    row = db.execute("PRAGMA foreign_keys").fetchone()
    assert row[0] == 1, "foreign_keys should be ON"


def test_database_wal_mode(db):
    row = db.execute("PRAGMA journal_mode").fetchone()
    assert row[0] == "wal", "journal_mode should be WAL"


def test_database_transaction(db):
    db.execute("INSERT INTO sources (id, name, weight) VALUES ('s1', 'Test', 0.5)")
    with db.transaction():
        db.execute(
            "INSERT INTO articles "
            "(id, url_original, url_canonical, title, origin_source_id, "
            " collected_at, score_base, scored_at, story_type) "
            "VALUES ('a1', 'http://x.com', 'http://x.com', 'T', 's1', 1000, 0.5, 1000, 'news')"
        )
    row = db.execute("SELECT id FROM articles WHERE id='a1'").fetchone()
    assert row is not None, "article should be committed"


def test_database_transaction_rollback(db):
    db.execute("INSERT INTO sources (id, name, weight) VALUES ('s2', 'Src', 0.3)")
    with pytest.raises(Exception):
        with db.transaction():
            db.execute(
                "INSERT INTO articles "
                "(id, url_original, url_canonical, title, origin_source_id, "
                " collected_at, score_base, scored_at, story_type) "
                "VALUES ('a2', 'http://y.com', 'http://y.com', 'U', 's2', 2000, 0.3, 2000, 'news')"
            )
            raise RuntimeError("forced rollback")
    row = db.execute("SELECT id FROM articles WHERE id='a2'").fetchone()
    assert row is None, "article should have been rolled back"


def test_fts5_available(db):
    db.execute("INSERT INTO sources (id, name, weight) VALUES ('s3', 'FTS Src', 0.4)")
    db.execute(
        "INSERT INTO articles "
        "(id, url_original, url_canonical, title, origin_source_id, "
        " collected_at, score_base, scored_at, story_type) "
        "VALUES ('a3', 'http://z.com', 'http://z.com', 'Python Releases 3.14', 's3', 3000, 0.4, 3000, 'release')"
    )
    rows = db.execute(
        "SELECT rowid FROM articles_fts WHERE articles_fts MATCH 'Python'"
    ).fetchall()
    assert len(rows) >= 1, "FTS5 search should return at least one result"


def test_database_reopen_idempotent(tmp_path):
    """Schema init must be idempotent — opening existing DB should not fail."""
    db_path = tmp_path / "reopen.db"
    db1 = Database(db_path)
    db1.execute("INSERT INTO sources (id, name, weight) VALUES ('s1', 'Src', 0.5)")
    db1.close()

    db2 = Database(db_path)
    row = db2.execute("SELECT id FROM sources WHERE id='s1'").fetchone()
    assert row is not None, "data from first session should persist"
    db2.close()


def test_database_nonexistent_parent_raises(tmp_path):
    """Database() must raise FileNotFoundError for missing parent dir."""
    bad_path = tmp_path / "nonexistent" / "sub" / "db.db"
    with pytest.raises(FileNotFoundError):
        Database(bad_path)


def test_database_foreign_key_enforcement(db):
    """Foreign key constraint must block orphan inserts."""
    with pytest.raises(sqlite3.IntegrityError):
        db.execute(
            "INSERT INTO story_articles (story_id, article_id) "
            "VALUES ('nonexistent_story', 'nonexistent_article')"
        )


def test_database_context_manager(tmp_path):
    """Database supports with-statement for automatic cleanup."""
    db_path = tmp_path / "ctx.db"
    with Database(db_path) as db:
        db.execute("INSERT INTO sources (id, name, weight) VALUES ('s1', 'Src', 0.5)")
        row = db.execute("SELECT id FROM sources WHERE id='s1'").fetchone()
        assert row is not None
