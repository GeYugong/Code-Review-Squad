import json
from typing import Any


def _strip_code_fence(text: str) -> str:
    text = text.strip()
    if text.startswith("```") and text.endswith("```"):
        lines = text.splitlines()
        if len(lines) >= 3:
            return "\n".join(lines[1:-1]).strip()
    return text


def try_parse_json(text: str) -> Any:
    """
    Best-effort: extract the first JSON object/array from model output.
    """
    if not text:
        return text
    text = _strip_code_fence(text)

    # quick path
    if (text.startswith("{") and text.endswith("}")) or (text.startswith("[") and text.endswith("]")):
        try:
            return json.loads(text)
        except Exception:
            return text

    # fallback: find first JSON bracket
    start_candidates = [i for i in [text.find("{"), text.find("[")] if i != -1]
    if not start_candidates:
        return text
    start = min(start_candidates)
    cut = text[start:]
    try:
        return json.loads(cut)
    except Exception:
        return text
