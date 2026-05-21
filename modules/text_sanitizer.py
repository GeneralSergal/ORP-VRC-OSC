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
    into VRChat-safe ASCII text
    while preserving formatting.
    """

    if not text:
        return ""

    # =====================================================
    # EMOJI REPLACEMENTS
    # =====================================================

    for emoji, replacement in EMOJI_REPLACEMENTS.items():

        text = text.replace(
            emoji,
            replacement
        )

    # =====================================================
    # UNICODE NORMALIZATION
    # =====================================================

    text = unicodedata.normalize(
        "NFKD",
        text
    )

    text = (
        text.encode(
            "ascii",
            "ignore"
        )
        .decode("ascii")
    )

    # =====================================================
    # REMOVE MARKDOWN
    # =====================================================

    text = re.sub(
        r"[*_~`#]",
        "",
        text
    )

    # =====================================================
    # CLEAN LINES
    # =====================================================

    lines = []

    for line in text.splitlines():

        cleaned = re.sub(
            r"\s+",
            " ",
            line
        ).strip()

        if cleaned:
            lines.append(cleaned)

    # preserve spacing
    text = "\n".join(lines)

    return text


def split_chatbox_text(text: str, limit=220):

    chunks = []

    while len(text) > limit:

        split_at = text.rfind(
            " ",
            0,
            limit
        )

        if split_at == -1:
            split_at = limit

        chunks.append(
            text[:split_at].strip()
        )

        text = text[split_at:].strip()

    if text:
        chunks.append(text)

    return chunks