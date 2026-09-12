#!/usr/bin/env python3
"""Collect a compact, deduplicated AI weekly source pack.

Uses public Google News RSS queries plus Hacker News Algolia. The output is
bounded so an LLM can draft the weekly digest without ingesting large pages.
"""

from __future__ import annotations

import argparse
import json
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime

UA = "Mozilla/5.0 (compatible; ai-digest-source-collector/1.0)"
QUERIES = [
    'AI model release when:7d',
    'AI tools launch when:7d',
    'OpenAI OR Anthropic OR Google DeepMind OR Meta AI when:7d',
    'AI agent developer tools when:7d',
]


def fetch(url: str, timeout: int = 20) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read()


def clean(value: str | None) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def parse_date(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        dt = parsedate_to_datetime(value)
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except (TypeError, ValueError):
        return None


def google_news(cutoff: datetime) -> list[dict]:
    items: list[dict] = []
    for query in QUERIES:
        params = urllib.parse.urlencode({"q": query, "hl": "en-US", "gl": "US", "ceid": "US:en"})
        root = ET.fromstring(fetch(f"https://news.google.com/rss/search?{params}"))
        for item in root.findall("./channel/item"):
            published = parse_date(item.findtext("pubDate"))
            if published and published < cutoff:
                continue
            source = item.find("source")
            items.append({
                "title": clean(item.findtext("title")),
                "url": clean(item.findtext("link")),
                "source": clean(source.text if source is not None else "Google News"),
                "published": published.isoformat() if published else None,
                "channel": "google_news",
            })
    return items


def hacker_news(cutoff: datetime) -> list[dict]:
    cutoff_ts = int(cutoff.timestamp())
    params = urllib.parse.urlencode({
        "query": "AI OR LLM OR agent",
        "tags": "story",
        "numericFilters": f"created_at_i>{cutoff_ts}",
        "hitsPerPage": 50,
    })
    payload = json.loads(fetch(f"https://hn.algolia.com/api/v1/search_by_date?{params}"))
    items = []
    for hit in payload.get("hits", []):
        url = hit.get("url") or f"https://news.ycombinator.com/item?id={hit.get('objectID')}"
        items.append({
            "title": clean(hit.get("title")),
            "url": url,
            "source": "Hacker News",
            "published": hit.get("created_at"),
            "points": hit.get("points") or 0,
            "comments": hit.get("num_comments") or 0,
            "channel": "hacker_news",
        })
    return items


def dedupe(items: list[dict]) -> list[dict]:
    seen: set[str] = set()
    result = []
    for item in items:
        key = re.sub(r"[^a-z0-9]+", " ", item["title"].lower()).strip()
        key = " ".join(key.split()[:14])
        if not key or key in seen:
            continue
        seen.add(key)
        result.append(item)
    return result


def rank(item: dict) -> tuple:
    official = int(any(name in item["source"].lower() for name in (
        "openai", "anthropic", "google", "microsoft", "meta", "github", "nvidia", "ibm", "nasa"
    )))
    engagement = item.get("points", 0) + item.get("comments", 0)
    return official, engagement, item.get("published") or ""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=7)
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    args = parser.parse_args()

    cutoff = datetime.now(timezone.utc) - timedelta(days=args.days)
    errors = []
    collected = []
    for name, collector in (("google_news", google_news), ("hacker_news", hacker_news)):
        try:
            collected.extend(collector(cutoff))
        except Exception as exc:  # keep the other source usable
            errors.append({"source": name, "error": str(exc)[:300]})

    items = sorted(dedupe(collected), key=rank, reverse=True)[: args.limit]
    if args.format == "json":
        print(json.dumps({"cutoff": cutoff.isoformat(), "count": len(items), "errors": errors, "items": items}, ensure_ascii=False, indent=2))
    else:
        print(f"# AI weekly source pack\n\nCutoff: {cutoff.isoformat()}  \nItems: {len(items)}")
        if errors:
            print(f"\nCollector warnings: `{json.dumps(errors, ensure_ascii=False)}`")
        for item in items:
            meta = item["source"]
            if item.get("published"):
                meta += f" · {item['published'][:10]}"
            if item.get("points") or item.get("comments"):
                meta += f" · {item.get('points', 0)} points · {item.get('comments', 0)} comments"
            print(f"\n- [{item['title']}]({item['url']}) — {meta}")
    return 0 if items else 1


if __name__ == "__main__":
    raise SystemExit(main())
