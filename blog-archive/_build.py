#!/usr/bin/env python3
"""Back up the adityarajsingh.com WordPress blog into this repo.

Pulls every published post from the public WP REST API and writes a
self-contained archive next to this script:

    posts/   one Markdown file per post (YAML frontmatter + body)
    images/  every featured & inline image, pulled local
    raw/     the exact REST API JSON (posts, categories, tags, media)
    index.md table of every post
    README.md

Re-runnable: just run `python3 _build.py` to refresh the archive in place.
No credentials needed — the REST API is public. Requires `pandoc` on PATH
for HTML -> Markdown conversion.
"""

import datetime
import html
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://adityarajsingh.com/wp-json/wp/v2"
SITE = "https://adityarajsingh.com"
UA = "Mozilla/5.0 (blog-archive-bot; +https://adityarajsingh.com/)"

HERE = Path(__file__).resolve().parent
POSTS_DIR = HERE / "posts"
IMG_DIR = HERE / "images"
RAW_DIR = HERE / "raw"

POST_FIELDS = "id,date,modified,slug,link,title,content,excerpt,featured_media,categories,tags"


# --- HTTP helpers ------------------------------------------------------------

def fetch(url):
    """Return raw bytes for a URL."""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def fetch_json(url):
    return json.loads(fetch(url).decode("utf-8"))


def fetch_all(endpoint, fields):
    """Fetch every item from a paginated WP REST collection."""
    items = []
    page = 1
    while True:
        url = f"{API}/{endpoint}?per_page=100&page={page}&_fields={fields}"
        try:
            batch = fetch_json(url)
        except urllib.error.HTTPError as err:
            if err.code == 400:  # asked for a page past the last one
                break
            raise
        if not batch:
            break
        items.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return items


# --- text / markdown helpers -------------------------------------------------

def strip_html(raw):
    """Collapse an HTML fragment to clean one-line plain text."""
    text = re.sub(r"<[^>]+>", " ", raw)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def html_to_md(body):
    """Convert an HTML fragment to GitHub-flavored Markdown via pandoc."""
    result = subprocess.run(
        ["pandoc", "-f", "html", "-t", "gfm", "--wrap=none"],
        input=body.encode("utf-8"),
        capture_output=True,
    )
    if result.returncode != 0:
        print(f"  ! pandoc failed: {result.stderr.decode()[:200]}")
        return body  # fall back to raw HTML rather than lose content
    return result.stdout.decode("utf-8").strip()


def frontmatter(**fields):
    """Build a YAML frontmatter block. json.dumps yields valid YAML scalars."""
    lines = ["---"]
    for key, value in fields.items():
        if value is None or value == [] or value == "":
            continue
        lines.append(f"{key}: {json.dumps(value, ensure_ascii=False)}")
    lines.append("---")
    return "\n".join(lines)


# --- image helpers -----------------------------------------------------------

def local_image_name(post_id, url, kind, idx=0):
    base = os.path.basename(urllib.parse.urlparse(url).path)
    ext = os.path.splitext(base)[1] or ".jpg"
    suffix = "featured" if kind == "featured" else f"inline-{idx}"
    return f"{post_id}-{suffix}{ext}"


def download_image(url, dest):
    if dest.exists():
        return True
    try:
        dest.write_bytes(fetch(url))
        return True
    except Exception as err:  # noqa: BLE001 - log and keep going
        print(f"  ! image failed {url}: {err}")
        return False


# --- main --------------------------------------------------------------------

def main():
    for directory in (POSTS_DIR, IMG_DIR, RAW_DIR):
        directory.mkdir(parents=True, exist_ok=True)

    print("Fetching posts, categories, tags ...")
    posts = fetch_all("posts", POST_FIELDS)
    categories = fetch_all("categories", "id,name,slug")
    tags = fetch_all("tags", "id,name,slug")
    cat_map = {c["id"]: c["name"] for c in categories}
    tag_map = {t["id"]: t["name"] for t in tags}
    print(f"  {len(posts)} posts, {len(categories)} categories, {len(tags)} tags")

    media_ids = sorted({p["featured_media"] for p in posts if p.get("featured_media")})
    media = []
    if media_ids:
        ids = ",".join(map(str, media_ids))
        media = fetch_json(f"{API}/media?include={ids}&per_page=100&_fields=id,source_url,mime_type")
    media_map = {m["id"]: m for m in media}
    print(f"  {len(media)} featured-image media records")

    # Save the faithful raw source first.
    for name, data in (
        ("posts.json", posts),
        ("categories.json", categories),
        ("tags.json", tags),
        ("media.json", media),
    ):
        (RAW_DIR / name).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    print("Writing posts ...")
    img_count = 0
    for post in posts:
        pid = post["id"]
        date = post["date"][:10]
        slug = post["slug"]
        title = html.unescape(post["title"]["rendered"])
        body = post["content"]["rendered"]

        featured_path = None
        fm_id = post.get("featured_media")
        if fm_id and fm_id in media_map:
            url = media_map[fm_id]["source_url"]
            name = local_image_name(pid, url, "featured")
            if download_image(url, IMG_DIR / name):
                featured_path = f"../images/{name}"
                img_count += 1

        for idx, url in enumerate(re.findall(r'<img[^>]+src="([^"]+)"', body)):
            name = local_image_name(pid, url, "inline", idx)
            if download_image(url, IMG_DIR / name):
                body = body.replace(url, f"../images/{name}")
                img_count += 1

        # Drop responsive-image attributes so no remote asset URLs survive.
        body = re.sub(r'\s+(?:srcset|sizes)="[^"]*"', "", body)

        block = frontmatter(
            title=title,
            date=post["date"],
            modified=post["modified"],
            slug=slug,
            original_url=post["link"],
            categories=[cat_map.get(c, str(c)) for c in post.get("categories", [])],
            tags=[tag_map.get(t, str(t)) for t in post.get("tags", [])],
            excerpt=strip_html(post["excerpt"]["rendered"]),
            featured_image=featured_path,
        )
        document = f"{block}\n\n# {title}\n\n{html_to_md(body)}\n"
        (POSTS_DIR / f"{date}-{slug}.md").write_text(document, encoding="utf-8")

    print(f"  wrote {len(posts)} posts, {img_count} images")
    write_index(posts)
    write_readme(posts)
    print("Done.")


def write_index(posts):
    ordered = sorted(posts, key=lambda p: p["date"], reverse=True)
    rows = [
        "# Blog archive index",
        "",
        f"{len(posts)} posts from [adityarajsingh.com/blog](https://adityarajsingh.com/blog/), newest first.",
        "",
        "| # | Date | Title | Archive | Original |",
        "|---|------|-------|---------|----------|",
    ]
    for i, post in enumerate(ordered, 1):
        date = post["date"][:10]
        title = html.unescape(post["title"]["rendered"]).replace("|", "\\|")
        fname = f"{date}-{post['slug']}.md"
        rows.append(f"| {i} | {date} | {title} | [md](posts/{fname}) | [link]({post['link']}) |")
    rows.append("")
    rows.append("<!-- by [Aditya Raj Singh](https://adityarajsingh.com/) -->")
    (HERE / "index.md").write_text("\n".join(rows) + "\n", encoding="utf-8")


def write_readme(posts):
    stamp = datetime.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %Z")
    text = f"""# Blog archive — adityarajsingh.com

A full backup of every published post on
[adityarajsingh.com/blog](https://adityarajsingh.com/blog/), captured from the
public WordPress REST API.

- **Posts:** {len(posts)}
- **Last generated:** {stamp}
- **Source:** `{SITE}/wp-json/wp/v2/posts`

## Layout

| Path | What |
|------|------|
| `posts/` | One Markdown file per post — `YYYY-MM-DD-slug.md`, YAML frontmatter + body. |
| `images/` | Featured and inline images, pulled local so each post is self-contained. |
| `raw/` | The exact REST API JSON (`posts`, `categories`, `tags`, `media`) — faithful source. |
| `index.md` | Table of every post, newest first. |
| `_build.py` | The script that produced all of the above. |

## Refresh the backup

```bash
cd blog-archive
python3 _build.py
```

Pulls the latest posts and rewrites the archive in place. No credentials
needed; requires `pandoc` on PATH for HTML to Markdown conversion.

<!-- by [Aditya Raj Singh](https://adityarajsingh.com/) -->
"""
    (HERE / "README.md").write_text(text, encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())

# by Aditya Raj Singh — https://adityarajsingh.com/
