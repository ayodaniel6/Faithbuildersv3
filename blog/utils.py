"""Small helper functions shared by the blog views.

Kept deliberately dependency-light and framework-agnostic so they are
easy to unit test in isolation.
"""

import markdown

from urllib.parse import urlparse, parse_qs


def render_markdown(text):
    """Render a Markdown string to HTML.

    The ``extra`` extension adds the commonly wanted features
    (tables, fenced code blocks, footnotes, etc.) so authors can write
    rich post bodies without touching HTML.
    """
    return markdown.markdown(
        text,
        extensions=[
            "extra",
        ],
    )


# Hostnames (minus any leading ``www.`` / ``m.`` / ``music.``) that we treat
# as YouTube. ``youtube-nocookie.com`` is included so already-embedded links
# are recognised too.
_YOUTUBE_HOSTS = ("youtube.com", "youtube-nocookie.com")

# Path prefixes on youtube.com that carry the video id as the second segment,
# e.g. ``/embed/<id>``, ``/shorts/<id>``, ``/live/<id>``, ``/v/<id>``.
_YOUTUBE_ID_IN_PATH = ("/embed/", "/shorts/", "/live/", "/v/")


def get_youtube_video_id(url):
    """Extract the 11-character video id from any common YouTube link.

    Handles the formats an author is likely to paste:
    ``youtube.com/watch?v=<id>``, ``youtu.be/<id>``, Shorts, Live,
    ``/embed/`` and legacy ``/v/`` links. Returns ``None`` when the URL
    is empty or is not a recognisable YouTube link.
    """
    if not url:
        return None

    # Authors often paste a link with stray whitespace or without a
    # scheme (e.g. "youtu.be/<id>"); tidy both so parsing still works.
    url = url.strip()

    if "//" not in url:
        url = "https://" + url

    parsed_url = urlparse(url)
    hostname = (parsed_url.hostname or "").lower()

    # Normalise leading "www." / "m." / "music." so mobile, desktop and
    # YouTube Music links all resolve to the same video.
    for prefix in ("www.", "m.", "music."):
        if hostname.startswith(prefix):
            hostname = hostname[len(prefix):]
            break

    # Short share link: https://youtu.be/<id>?si=...
    if hostname == "youtu.be":
        return parsed_url.path.lstrip("/").split("/")[0] or None

    if hostname in _YOUTUBE_HOSTS:
        path = parsed_url.path

        # Standard link: https://www.youtube.com/watch?v=<id>
        if path == "/watch":
            return parse_qs(parsed_url.query).get("v", [None])[0]

        # Embed / Shorts / Live / legacy links carry the id in the path.
        if path.startswith(_YOUTUBE_ID_IN_PATH):
            return path.split("/")[2]

    return None


def get_youtube_embed_url(url):
    """Turn a YouTube link into an embeddable player URL, or ``None``.

    Uses the privacy-enhanced ``youtube-nocookie.com`` domain and
    ``rel=0`` so the player only suggests more videos from the same
    channel once the clip ends.
    """
    video_id = get_youtube_video_id(url)

    if not video_id:
        return None

    return f"https://www.youtube-nocookie.com/embed/{video_id}?rel=0"
