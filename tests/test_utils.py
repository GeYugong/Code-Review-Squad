from app.core.utils import try_parse_json


def test_try_parse_json_handles_fenced_json():
    raw = """```json
{"a": 1, "b": ["x"]}
```"""
    parsed = try_parse_json(raw)
    assert isinstance(parsed, dict)
    assert parsed["a"] == 1


def test_try_parse_json_keeps_non_json():
    raw = "not json"
    parsed = try_parse_json(raw)
    assert parsed == raw
