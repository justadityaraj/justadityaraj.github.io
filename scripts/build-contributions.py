#!/usr/bin/env python3
"""Regenerate the "Open Source Contributions" section of index.html from GitHub.

Pulls every PR authored by USER, keeps the ones raised against *other people's*
repos, splits them into Merged / Open, and splices the rendered cards straight
into index.html between the oss:* marker comments. Static output on purpose:
no client-side fetch, so the cards survive JS-off, stay indexable, and the
existing GSAP scroll animation still finds them in the DOM at parse time.

Run `python3 scripts/build-contributions.py --selfcheck` to exercise the pure
logic without touching the network.
"""

import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from html import escape
from pathlib import Path

USER = "justadityaraj"
# `is:public` is load-bearing, not cosmetic: run with a token that can see
# private repos (a personal one, say) and the search would otherwise hand back
# client and internal work to publish on a public page.
SEARCH_Q = f"type:pr+author:{USER}+is:public"
ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
API = "https://api.github.com"

CARDS_START = "<!-- oss:cards:start -->"
CARDS_END = "<!-- oss:cards:end -->"
SHIPPED_START = "<!-- oss:shipped:start -->"
SHIPPED_END = "<!-- oss:shipped:end -->"

# Trailing "(closes #123)" noise that reads as clutter on a card.
ISSUE_REF = re.compile(r"\s*\((?:closes|close|fixes|fix|resolves|resolve)\s+#\d+\)\s*$", re.I)


def api_get(path):
    req = urllib.request.Request(
        path if path.startswith("http") else f"{API}{path}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": f"{USER}-site-contributions",
            **({"Authorization": f"Bearer {os.environ['GH_TOKEN']}"} if os.environ.get("GH_TOKEN") else {}),
        },
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def fetch_prs():
    """Every public PR authored by USER, across all pages."""
    items, page = [], 1
    while True:
        batch = api_get(f"/search/issues?q={SEARCH_Q}&per_page=100&page={page}")["items"]
        items += batch
        if len(batch) < 100:
            return items
        page += 1


def drop_private(prs, repos):
    """Second, independent guard on the same leak. Belt and braces."""
    return [p for p in prs if not repos[p["repo"]]["private"]]


def fmt_stars(n):
    if n < 1000:
        return str(n)
    k = n / 1000
    return (f"{k:.1f}".rstrip("0").rstrip(".") if k < 10 else str(round(k))) + "k"


def fmt_date(iso):
    d = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    return f"{d:%b} {d.day}, {d.year}"


def bucket(prs):
    """Split into (merged, open), dropping own repos and rejected PRs.

    Own repos are excluded because merging your own PR is not a contribution;
    closed-but-unmerged PRs are excluded because a portfolio shows what landed
    and what is still in flight, not what was turned down.
    """
    merged, opened = [], []
    for pr in prs:
        repo = "/".join(pr["html_url"].split("/")[3:5])
        if repo.split("/")[0].lower() == USER.lower():
            continue
        row = {
            "repo": repo,
            "number": pr["number"],
            "url": pr["html_url"],
            "title": ISSUE_REF.sub("", pr["title"]),
        }
        merged_at = (pr.get("pull_request") or {}).get("merged_at")
        if merged_at:
            merged.append({**row, "sort": merged_at, "state": "merged", "when": f"Merged {fmt_date(merged_at)}"})
        elif pr["state"] == "open":
            opened.append({**row, "sort": pr["created_at"], "state": "open", "when": f"Opened {fmt_date(pr['created_at'])}"})
    merged.sort(key=lambda r: r["sort"], reverse=True)
    opened.sort(key=lambda r: r["sort"], reverse=True)
    return merged, opened


BADGE_ICON = {
    "merged": '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M5.45 5.154A4.25 4.25 0 0 0 9.25 7.5h1.378a2.251 2.251 0 1 1 0 1.5H9.25A5.734 5.734 0 0 1 5 7.123v3.505a2.25 2.25 0 1 1-1.5 0V5.372a2.25 2.25 0 1 1 1.95-.218ZM4.25 13.5a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Zm8.5-4.5a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5ZM5 3.25a.75.75 0 1 0 0 .005V3.25Z"/></svg>',
    "open": '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M1.5 3.25a2.25 2.25 0 1 1 3 2.122v5.256a2.251 2.251 0 1 1-1.5 0V5.372A2.25 2.25 0 0 1 1.5 3.25Zm5.677-.177L9.573.677A.25.25 0 0 1 10 .854V2.5h1A2.5 2.5 0 0 1 13.5 5v5.628a2.251 2.251 0 1 1-1.5 0V5a1 1 0 0 0-1-1h-1v1.646a.25.25 0 0 1-.427.177L7.177 3.427a.25.25 0 0 1 0-.354ZM3.75 2.5a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5Zm0 9.5a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5Zm8.25.75a.75.75 0 1 0 1.5 0 .75.75 0 0 0-1.5 0Z"/></svg>',
}


def card(pr):
    return f"""          <a class="oss-card" href="{escape(pr['url'], quote=True)}" target="_blank" rel="noopener">
            <div class="oss-card-top">
              <div class="oss-repo"><strong>{escape(pr['repo'])}</strong> #{pr['number']}</div>
              <span class="oss-badge {pr['state']}">{BADGE_ICON[pr['state']]}{pr['state'].capitalize()}</span>
            </div>
            <div class="oss-pr-title">{escape(pr['title'])}</div>
            <div class="oss-meta">
              <span>&#9733; {pr['stars']}</span>
              <span>{escape(pr['when'])}</span>
            </div>
          </a>"""


def group(title, prs):
    if not prs:
        return ""
    cards = "\n\n".join(card(p) for p in prs)
    return f"""        <div class="oss-group">
          <h3 class="oss-group-title">{title} <span class="oss-group-count">{len(prs)}</span></h3>
          <div class="oss-grid">
{cards}
          </div>
        </div>"""


def splice(html, start, end, body):
    a, b = html.index(start) + len(start), html.index(end)
    return html[:a] + body + html[b:]


def main():
    prs = fetch_prs()
    merged, _ = bucket(prs)

    repos = {}
    for pr in merged:
        if pr["repo"] not in repos:
            repos[pr["repo"]] = api_get(f"/repos/{pr['repo']}")
    merged = drop_private(merged, repos)
    for pr in merged:
        pr["stars"] = fmt_stars(repos[pr["repo"]]["stargazers_count"])

    body = group("Merged", merged)
    html = INDEX.read_text(encoding="utf-8")
    html = splice(html, CARDS_START, CARDS_END, f"\n{body}\n      ")
    html = splice(html, SHIPPED_START, SHIPPED_END, str(len(merged)))
    INDEX.write_text(html, encoding="utf-8")

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    print(f"{len(merged)} merged, {len(repos)} repos at {stamp}")


def selfcheck():
    assert [fmt_stars(n) for n in (0, 541, 1000, 2800, 6700, 9400, 9950, 11000, 105000)] == \
        ["0", "541", "1k", "2.8k", "6.7k", "9.4k", "9.9k", "11k", "105k"]
    assert fmt_date("2026-07-04T06:09:11Z") == "Jul 4, 2026"
    assert ISSUE_REF.sub("", 'feat: add "Ignore Folder" item (closes #8397)') == 'feat: add "Ignore Folder" item'
    assert ISSUE_REF.sub("", "fix: keep (parens) intact") == "fix: keep (parens) intact"

    sample = [
        {"html_url": "https://github.com/a/b/pull/1", "number": 1, "title": "landed", "state": "closed",
         "created_at": "2026-01-01T00:00:00Z", "pull_request": {"merged_at": "2026-02-01T00:00:00Z"}},
        {"html_url": "https://github.com/a/b/pull/2", "number": 2, "title": "in flight", "state": "open",
         "created_at": "2026-03-01T00:00:00Z", "pull_request": {"merged_at": None}},
        {"html_url": "https://github.com/a/b/pull/3", "number": 3, "title": "rejected", "state": "closed",
         "created_at": "2026-01-01T00:00:00Z", "pull_request": {"merged_at": None}},
        {"html_url": f"https://github.com/{USER}/mine/pull/4", "number": 4, "title": "own repo", "state": "open",
         "created_at": "2026-04-01T00:00:00Z", "pull_request": {"merged_at": None}},
    ]
    merged, opened = bucket(sample)
    assert [p["title"] for p in merged] == ["landed"], merged
    assert [p["title"] for p in opened] == ["in flight"], opened

    # A private repo reaching this public page would leak client work.
    assert "is:public" in SEARCH_Q
    mixed = [{"repo": "pub/a"}, {"repo": "priv/b"}]
    assert drop_private(mixed, {"pub/a": {"private": False}, "priv/b": {"private": True}}) == [{"repo": "pub/a"}]

    # PR titles are attacker-controlled text landing in HTML, so it must not break out.
    evil = dict(merged[0], title='<img src=x onerror=alert(1)> & "quotes"', stars="1k")
    assert "<img" not in card(evil) and "&lt;img" in card(evil)

    assert splice("A<!--s-->old<!--e-->B", "<!--s-->", "<!--e-->", "new") == "A<!--s-->new<!--e-->B"
    assert group("Merged", []) == ""
    print("selfcheck ok")


if __name__ == "__main__":
    try:
        selfcheck() if "--selfcheck" in sys.argv else main()
    except urllib.error.HTTPError as e:
        sys.exit(f"github api {e.code}: {e.reason} ({e.url})")

# by Aditya Raj Singh · https://adityarajsingh.com/
