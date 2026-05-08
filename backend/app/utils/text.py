import re


EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def split_bullets(text: str) -> list[str]:
    items = [line.strip("-• \t") for line in text.splitlines()]
    return [i for i in items if i]
