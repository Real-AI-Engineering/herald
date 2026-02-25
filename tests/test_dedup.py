"""Tests for dedup module."""
from pathlib import Path
import tempfile

def test_seen_urls_add_and_check():
    from pipeline.dedup import SeenUrls
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        path = Path(f.name)
    seen = SeenUrls(path, max_age_days=90)
    seen.add("https://example.com/1")
    assert seen.is_seen("https://example.com/1")
    assert not seen.is_seen("https://example.com/2")

def test_seen_urls_uses_sha256():
    from pipeline.dedup import SeenUrls
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        path = Path(f.name)
    seen = SeenUrls(path, max_age_days=90)
    seen.add("https://example.com")
    seen.save()
    content = path.read_text()
    assert "example.com" not in content

def test_seen_urls_persistence():
    from pipeline.dedup import SeenUrls
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        path = Path(f.name)
    seen1 = SeenUrls(path, max_age_days=90)
    seen1.add("https://example.com/persist")
    seen1.save()
    # Load fresh instance
    seen2 = SeenUrls(path, max_age_days=90)
    assert seen2.is_seen("https://example.com/persist")

def test_title_similarity_detects_duplicates():
    from pipeline.dedup import is_title_duplicate
    titles = ["OpenAI releases GPT-5 with amazing capabilities"]
    assert is_title_duplicate("OpenAI releases GPT-5 with amazing new capabilities", titles)
    assert not is_title_duplicate("Google announces Gemini 3.0", titles)

def test_dedup_items_removes_seen():
    from pipeline.dedup import SeenUrls, dedup_items
    from pipeline.collect import RawItem
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        path = Path(f.name)
    seen = SeenUrls(path, max_age_days=90)
    seen.add("https://example.com/old")
    items = [
        RawItem(url="https://example.com/old", title="Old", source="test", published="2026-02-25"),
        RawItem(url="https://example.com/new", title="New", source="test", published="2026-02-25"),
    ]
    result = dedup_items(items, seen)
    assert len(result) == 1
    assert result[0].url == "https://example.com/new"
