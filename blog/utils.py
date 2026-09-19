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

    parsed_url = urlparse(url)

    if parsed_url.hostname in ["www.youtube.com", "youtube.com"]:
        video_id = parse_qs(
            parsed_url.query
        ).get(
            "v",
            [None]
        )[0]

    elif parsed_url.hostname == "youtu.be":
        video_id = parsed_url.path.lstrip("/")

    else:
        return None

    if not video_id:
        return None

    return f"https://www.youtube.com/embed/{video_id}"