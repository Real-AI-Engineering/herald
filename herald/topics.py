"""Topic extraction for herald v2 ingest pipeline."""
from __future__ import annotations


def extract_topics(title: str, topic_rules: dict[str, list[str]]) -> list[str]:
    t = title.lower()
    return [topic for topic, keywords in topic_rules.items() if any(kw.lower() in t for kw in keywords)]
