#!/usr/bin/env python3
"""
Content Sources Scraper v1.1 — RSS/Atom scraping das fontes do content-sources.md
Integra com o cron job de curadoria diária do Hermes

Usage: python3 content-sources-scraper.py [output_json] [tier]
  output_json: path para output (default: /root/.hermes/cron/scraped-content.json)
  tier: 1 (Tier 1 only), 2 (Tier 1+2), all (default: all)
"""

import json
import re
import sys
import time
from datetime import datetime
from urllib.parse import urlparse

import requests

# === CONFIG ===
OUTPUT_FILE = "/root/.hermes/cron/scraped-content.json"
SOURCES_FILE = "/root/.hermes/content-sources/content-sources.md"
MAX_ITEMS_PER_SOURCE = 5
REQUEST_TIMEOUT = 12
USER_AGENT = "Mozilla/5.0 (compatible; HermesContentBot/1.0)"

TIER_FILTER = "all"
if len(sys.argv) > 2:
    TIER_FILTER = sys.argv[2]
elif len(sys.argv) > 1:
    OUTPUT_FILE = sys.argv[1]

# === Helpers ===

def decode_html(text: str) -> str:
    """Decode common HTML entities."""
    if not text:
        return ""
    entities = {
        '&#8220;': '"', '&#8221;': '"', '&#8217;': "'", '&#8211;': '–',
        '&#8230;': '…', '&amp;': '&', '&quot;': '"', '&lt;': '<', '&gt;': '>',
        '&nbsp;': ' ', '&mdash;': '—', '&#39;': "'",
    }
    for entity, char in entities.items():
        text = text.replace(entity, char)
    # Strip <![CDATA[...]]> wrappers
    text = re.sub(r'<!\[CDATA\[(.*?)\]\]>', r'\1', text, flags=re.DOTALL)
    return text


def strip_tags(text: str) -> str:
    """Remove HTML tags from text."""
    if not text:
        return ""
    return re.sub(r'<[^>]+>', '', text)


def extract_rss_items(content: str) -> list:
    """Extract items from RSS 2.0 or Atom feed."""
    items = []

    # Try RSS 2.0 <item>
    for item in re.findall(r'<item>(.*?)</item>', content, re.DOTALL)[:MAX_ITEMS_PER_SOURCE]:
        title = re.search(r'<title[^>]*>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>', item, re.DOTALL)
        link = re.search(r'<link[^>]*>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</link>', item, re.DOTALL)
        desc = re.search(r'<description[^>]*>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</description>', item, re.DOTALL)
        pubdate = re.search(r'<pubDate>(.*?)</pubDate>', item)
        title_text = decode_html(title.group(1).strip()) if title else ""
        if title_text:
            items.append({
                "title": title_text,
                "link": link.group(1).strip() if link else "",
                "description": strip_tags(decode_html(desc.group(1))).strip()[:300] if desc else "",
                "pubdate": pubdate.group(1).strip() if pubdate else "",
            })

    # Fallback: Atom <entry>
    if not items:
        for entry in re.findall(r'<entry>(.*?)</entry>', content, re.DOTALL)[:MAX_ITEMS_PER_SOURCE]:
            title = re.search(r'<title[^>]*>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>', entry, re.DOTALL)
            link = re.search(r'<link[^>]*href="([^"]+)"', entry)
            summary = re.search(r'<summary[^>]*>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</summary>', entry, re.DOTALL)
            content_tag = re.search(r'<content[^>]*>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</content>', entry, re.DOTALL)
            published = re.search(r'<published>(.*?)</published>', entry)
            title_text = decode_html(title.group(1).strip()) if title else ""
            if title_text:
                desc_text = strip_tags(decode_html(summary.group(1))).strip()[:300] if summary else \
                    strip_tags(decode_html(content_tag.group(1))).strip()[:300] if content_tag else ""
                items.append({
                    "title": title_text,
                    "link": link.group(1).strip() if link else "",
                    "description": desc_text,
                    "pubdate": published.group(1).strip() if published else "",
                })

    return items


def fetch_feed(name: str, url: str, tier: str) -> dict:
    """Fetch and parse a single RSS/Atom feed."""
    result = {
        "source": name,
        "url": url,
        "tier": tier,
        "items": [],
        "fetched_at": datetime.utcnow().isoformat() + "Z",
        "item_count": 0,
        "error": None,
    }

    def try_fetch(u: str) -> str:
        resp = requests.get(u, timeout=REQUEST_TIMEOUT, headers={"User-Agent": USER_AGENT}, allow_redirects=True)
        resp.raise_for_status()
        return resp.text

    content = None
    fetched_url = url

    try:
        content = try_fetch(url)

        # If HTML, look for autodiscovery or try /feed
        if '<html' in content[:300].lower():
            autodiscovery_url = None
            for link_match in re.findall(r'<link[^>]+>', content, re.IGNORECASE):
                if ('application/rss' in link_match or 'application/atom' in link_match):
                    href_m = re.search(r'href=["\']([^"\']+)["\']', link_match)
                    if href_m:
                        autodiscovery_url = href_m.group(1)
                        break

            if autodiscovery_url:
                if autodiscovery_url.startswith('/'):
                    from urllib.parse import urlparse
                    parsed = urlparse(url)
                    autodiscovery_url = f"{parsed.scheme}://{parsed.netloc}{autodiscovery_url}"
                fetched_url = autodiscovery_url
                content = try_fetch(autodiscovery_url)
            else:
                # Try /feed as fallback for common CMS (substack, ghost, wordpress)
                feed_url = url.rstrip('/') + '/feed'
                try:
                    content = try_fetch(feed_url)
                    fetched_url = feed_url
                except Exception:
                    pass

        items = extract_rss_items(content)
        result["items"] = items
        result["item_count"] = len(items)
        result["url"] = fetched_url  # update to actual feed URL

    except Exception as e:
        result["error"] = str(e)[:100]

    return result


def parse_sources_from_md() -> list:
    """Parse RSS feed URLs from content-sources.md table format.

    Table format:
    | **Name** | Foco | Frequência | Status | URL |

    We extract: name, url from cells where status is ✅ Ativo.
    """
    feeds = []

    with open(SOURCES_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Find section headers to determine tier
    current_section = ""
    section_tiers = {
        "Newsletters Globais": "1",
        "Twitter": "1",
        "Perfis no Twitter": "1",
        "Brasil": "1",
        "Podcast": "2",
        "AI": "3",
        "Wealth": "3",
        "Dados": "3",
    }

    for line in lines:
        # Section header
        section_match = re.match(r'^## \S (.+)', line)
        if section_match:
            current_section = section_match.group(1).strip()
            continue

        # Skip separator lines
        if re.match(r'^---\s*$', line) or re.match(r'^\|\s*[-|]+\s*$', line):
            continue

        # Table row — format: | (empty) | **Name** | Foco | Freq | Status | URL |
        cells_raw = [c.strip() for c in line.split('|')[1:-1]]
        # Remove empty cells (from leading/trailing pipes)
        cells = [c for c in cells_raw if c and not re.match(r'^[-|]+$', c)]

        if len(cells) < 4:
            continue

        # cells = [name, foco, freq, status, url]
        status_cell = cells[-2]
        url_cell = cells[-1]

        # Check if active
        if '✅' not in status_cell:
            continue

        # Extract name (remove ** bold markers)
        name_cell = cells[0]
        name = re.sub(r'\*\*(.+?)\*\*', r'\1', name_cell).strip()
        if not name:
            name = name_cell.strip()

        # Extract URL (must be a valid http URL)
        url = url_cell.strip()
        if not url.startswith('http'):
            continue
        # Skip placeholder/ticket links
        if any(x in url for x in ['ticket', 'example', 'place']):
            continue

        # Determine tier
        tier = "3"
        name_lower = name.lower()
        section_lower = current_section.lower()

        if any(x in name_lower for x in ['tomasz', 'not boring', 'lenny', 'stratechery', 'tunguz',
                                          'florian', 'theodoro', 'arlo almeida', 'alexlazar', 'benedict evans',
                                          'chamath', 'jason calacanis', 'paul graham', 'naval']):
            tier = "1"
        elif any(x in name_lower for x in ['first round', 'acquired', 'masters of scale',
                                            'carta', 'morning brew', 'neofeed', 'brazil journal',
                                            'startupi', 'all-in', '20 minute vc', 'how i built']):
            tier = "2"
        elif any(x in section_lower for x in ['newsletters', 'twitter', 'brasil', 'perfis']):
            tier = "1"
        elif any(x in section_lower for x in ['podcast']):
            tier = "2"

        feeds.append({"name": name, "url": url, "tier": tier})

    # Deduplicate by URL
    seen = set()
    unique = []
    for f in feeds:
        if f["url"] not in seen:
            seen.add(f["url"])
            unique.append(f)

    return unique


def should_include(tier: str, source_tier: str) -> bool:
    if TIER_FILTER == "1":
        return source_tier == "1"
    elif TIER_FILTER == "2":
        return source_tier in ("1", "2")
    return True


def main():
    print("[scraper] Content Sources Scraper v1.1")
    print(f"[scraper] Tier filter: {TIER_FILTER}")
    print(f"[scraper] Output: {OUTPUT_FILE}")
    print()

    feeds = parse_sources_from_md()
    print(f"[scraper] Found {len(feeds)} feeds to scrape")

    results = []
    total_items = 0
    success_count = 0

    for i, feed in enumerate(feeds):
        name = feed["name"]
        url = feed["url"]
        tier = feed["tier"]

        if not should_include(tier, feed["tier"]):
            continue

        if i > 0 and i % 8 == 0:
            print(f"[scraper] Progress: {i}/{len(feeds)} feeds...")

        result = fetch_feed(name, url, tier)

        if result["error"]:
            print(f"  [warn] {name[:40]}: {result['error'][:60]}")
        else:
            success_count += 1
            total_items += result["item_count"]
            print(f"  [ok] {name[:40]}: {result['item_count']} items")

        results.append(result)
        time.sleep(0.25)

    output = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "tier_filter": TIER_FILTER,
        "feeds": results,
        "stats": {
            "total_feeds": len(feeds),
            "successful_feeds": success_count,
            "total_items": total_items,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print()
    print(f"[scraper] ✅ Done! Scraped {total_items} items from {success_count}/{len(feeds)} feeds")
    print(f"[scraper] 📄 Output: {OUTPUT_FILE}")

    import os
    size = os.path.getsize(OUTPUT_FILE)
    print(f"[scraper] 📦 File size: {size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
