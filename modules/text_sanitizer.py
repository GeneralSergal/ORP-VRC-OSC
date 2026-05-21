# =========================================================
# ORP Text Sanitizer
# =========================================================

import re
import unicodedata


EMOJI_REPLACEMENTS = {
    "🐾": "*paw*",
    "🌟": "*sparkle*",
    "✨": "*shine*",
    "💫": "*twirl*",
    "🎉": "*celebrate*",
    "😜": ";P",
    "👾": "[gremlin]",
    "🧦": "[sock]",
    "🚀": "[zoom]",
    "💀": "[skull]",
    "❤️": "<3",
    "❤": "<3",
    "😊": ":)",
    "😈": ">:)",
    "🔥": "[fire]",
}


def sanitize_for_vrchat(text: str) -> str:
    """
    Converts unicode/emojis/markdown
    into VRChat-safe ASCII text.
    """

    if not text:
        return ""

    # emoji replacements
    for emoji, replacement in EMOJI_REPLACEMENTS.items():
        text = text.replace(emoji, replacement)

    # normalize unicode
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")

    # remove markdown formatting
    text = re.sub(r"[*_~`#]", "", text)

    # clean whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text


def split_chatbox_text(text: str, limit=140):
    """
    Splits long text into VRChat-safe chunks.
    """

    chunks = []

    while len(text) > limit:

        split_at = text.rfind(" ", 0, limit)

        if split_at == -1:
            split_at = limit

        chunks.append(text[:split_at].strip())

        text = text[split_at:].strip()

    if text:
        chunks.append(text)

    return chunks