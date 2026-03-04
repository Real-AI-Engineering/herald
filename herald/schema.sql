CREATE TABLE IF NOT EXISTS sources (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    url TEXT,
    weight REAL NOT NULL DEFAULT 0.2,
    category TEXT CHECK(category IN ('community','official','aggregator'))
);

CREATE TABLE IF NOT EXISTS articles (
    id TEXT PRIMARY KEY,
    url_original TEXT NOT NULL,
    url_canonical TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    origin_source_id TEXT NOT NULL REFERENCES sources(id),
    published_at INTEGER,
    collected_at INTEGER NOT NULL,
    points INTEGER NOT NULL DEFAULT 0 CHECK(points >= 0),
    story_type TEXT NOT NULL DEFAULT 'news'
        CHECK(story_type IN ('news','release','research','opinion','tutorial')),
    score_base REAL NOT NULL,
    scored_at INTEGER NOT NULL,
    extra TEXT CHECK(extra IS NULL OR json_valid(extra))
);

CREATE TABLE IF NOT EXISTS mentions (
    article_id TEXT NOT NULL REFERENCES articles(id) ON DELETE CASCADE,
    source_id TEXT NOT NULL REFERENCES sources(id),
    url TEXT NOT NULL,
    points INTEGER NOT NULL DEFAULT 0,
    discovered_at INTEGER NOT NULL,
    extra TEXT,
    PRIMARY KEY (article_id, source_id)
);

CREATE TABLE IF NOT EXISTS article_topics (
    article_id TEXT NOT NULL REFERENCES articles(id) ON DELETE CASCADE,
    topic TEXT NOT NULL,
    PRIMARY KEY (article_id, topic)
);
CREATE INDEX IF NOT EXISTS idx_article_topics_topic ON article_topics(topic, article_id);

CREATE TABLE IF NOT EXISTS stories (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    summary TEXT,
    story_type TEXT NOT NULL DEFAULT 'news',
    score REAL NOT NULL,
    canonical_article_id TEXT REFERENCES articles(id) ON DELETE SET NULL,
    first_seen INTEGER NOT NULL,
    last_updated INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active','inactive'))
);

CREATE TABLE IF NOT EXISTS story_articles (
    story_id TEXT NOT NULL REFERENCES stories(id) ON DELETE CASCADE,
    article_id TEXT NOT NULL REFERENCES articles(id) ON DELETE CASCADE,
    PRIMARY KEY (story_id, article_id),
    UNIQUE(article_id)
);

CREATE TABLE IF NOT EXISTS story_topics (
    story_id TEXT NOT NULL REFERENCES stories(id) ON DELETE CASCADE,
    topic TEXT NOT NULL,
    PRIMARY KEY (story_id, topic)
);
CREATE INDEX IF NOT EXISTS idx_story_topics_topic ON story_topics(topic, story_id);

CREATE TABLE IF NOT EXISTS pipeline_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    started_at INTEGER NOT NULL,
    finished_at INTEGER,
    articles_new INTEGER DEFAULT 0,
    articles_updated INTEGER DEFAULT 0,
    stories_created INTEGER DEFAULT 0,
    stories_updated INTEGER DEFAULT 0,
    error TEXT
);

CREATE INDEX IF NOT EXISTS idx_articles_collected_at ON articles(collected_at DESC);
CREATE INDEX IF NOT EXISTS idx_articles_source ON articles(origin_source_id, collected_at DESC);
CREATE INDEX IF NOT EXISTS idx_stories_score ON stories(score DESC);
CREATE INDEX IF NOT EXISTS idx_stories_last_updated ON stories(last_updated DESC);
CREATE INDEX IF NOT EXISTS idx_story_articles_article ON story_articles(article_id, story_id);

CREATE VIRTUAL TABLE IF NOT EXISTS articles_fts USING fts5(title, content=articles, content_rowid=rowid);
CREATE VIRTUAL TABLE IF NOT EXISTS stories_fts USING fts5(title, summary, content=stories, content_rowid=rowid);

-- FTS5 content sync triggers for articles
CREATE TRIGGER IF NOT EXISTS articles_fts_insert AFTER INSERT ON articles BEGIN
    INSERT INTO articles_fts(rowid, title) VALUES (new.rowid, new.title);
END;

CREATE TRIGGER IF NOT EXISTS articles_fts_update AFTER UPDATE ON articles BEGIN
    INSERT INTO articles_fts(articles_fts, rowid, title) VALUES ('delete', old.rowid, old.title);
    INSERT INTO articles_fts(rowid, title) VALUES (new.rowid, new.title);
END;

CREATE TRIGGER IF NOT EXISTS articles_fts_delete AFTER DELETE ON articles BEGIN
    INSERT INTO articles_fts(articles_fts, rowid, title) VALUES ('delete', old.rowid, old.title);
END;

-- FTS5 content sync triggers for stories
CREATE TRIGGER IF NOT EXISTS stories_fts_insert AFTER INSERT ON stories BEGIN
    INSERT INTO stories_fts(rowid, title, summary) VALUES (new.rowid, new.title, new.summary);
END;

CREATE TRIGGER IF NOT EXISTS stories_fts_update AFTER UPDATE ON stories BEGIN
    INSERT INTO stories_fts(stories_fts, rowid, title, summary) VALUES ('delete', old.rowid, old.title, old.summary);
    INSERT INTO stories_fts(rowid, title, summary) VALUES (new.rowid, new.title, new.summary);
END;

CREATE TRIGGER IF NOT EXISTS stories_fts_delete AFTER DELETE ON stories BEGIN
    INSERT INTO stories_fts(stories_fts, rowid, title, summary) VALUES ('delete', old.rowid, old.title, old.summary);
END;
