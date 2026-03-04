"""Tests for herald.topics.extract_topics."""
import pytest

from herald.topics import extract_topics


def test_returns_matching_topic():
    result = extract_topics("PyTorch 2.0 Release", {"ai": ["pytorch", "ml"], "python": ["python"]})
    assert result == ["ai"]


def test_empty_topic_rules_returns_empty():
    assert extract_topics("Any Title", {}) == []


def test_no_match_returns_empty():
    result = extract_topics("Rust and Go benchmark", {"ai": ["neural", "pytorch"]})
    assert result == []


def test_multiple_topics_matched():
    result = set(extract_topics("Rust and Python benchmark", {"rust": ["rust"], "python": ["python"], "ai": ["neural"]}))
    assert result == {"rust", "python"}


def test_case_insensitive_title():
    result = extract_topics("PYTORCH new release", {"ai": ["pytorch"]})
    assert result == ["ai"]


def test_case_insensitive_keyword():
    result = extract_topics("pytorch new release", {"ai": ["PyTorch"]})
    assert result == ["ai"]


def test_substring_match():
    result = extract_topics("machine learning paper", {"ai": ["learning"]})
    assert result == ["ai"]


def test_all_topics_when_all_match():
    rules = {"a": ["alpha"], "b": ["beta"]}
    result = extract_topics("alpha and beta together", rules)
    assert set(result) == {"a", "b"}
