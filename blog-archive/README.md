# Blog archive — adityarajsingh.com

A full backup of every published post on
[adityarajsingh.com/blog](https://adityarajsingh.com/blog/), captured from the
public WordPress REST API.

- **Posts:** 42
- **Last generated:** 2026-06-30 01:40 IST
- **Source:** `https://adityarajsingh.com/wp-json/wp/v2/posts`

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
