import markdown

from urllib.parse import urlparse, parse_qs


def render_markdown(text):
    return markdown.markdown(
        text,
        extensions=[
            "extra",
        ],
    )


def get_youtube_embed_url(url):

    if not url:
        return None

    # Authors often paste a link with stray whitespace or without a
    # scheme (e.g. "youtu.be/<id>"); handle both so the embed still works.
    url = url.strip()

    if "//" not in url:
        url = "https://" + url

    parsed_url = urlparse(url)

    hostname = (parsed_url.hostname or "").lower()

    # Normalise leading "www." / "m." / "music." so mobile, desktop and
    # YouTube Music links all resolve to the same embed.
    for prefix in ("www.", "m.", "music."):
        if hostname.startswith(prefix):
            hostname = hostname[len(prefix):]
            break

    video_id = None

    if hostname == "youtu.be":
        # Short share link: https://youtu.be/<id>?si=...
        video_id = parsed_url.path.lstrip("/").split("/")[0]

    elif hostname in ("youtube.com", "youtube-nocookie.com"):
        path = parsed_url.path

        if path == "/watch":
            # Standard link: https://www.youtube.com/watch?v=<id>
            video_id = parse_qs(parsed_url.query).get("v", [None])[0]

        elif path.startswith(("/embed/", "/shorts/", "/live/", "/v/")):
            # Already-embed, Shorts, Live and legacy /v/ links.
            video_id = path.split("/")[2]

    if not video_id:
        return None

    return f"https://www.youtube.com/embed/{video_id}"