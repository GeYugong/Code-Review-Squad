from app.core.context_builder import collect_context


def test_collect_context_from_file_list(tmp_path):
    a = tmp_path / "a.py"
    a.write_text("print('a')", encoding="utf-8")
    b = tmp_path / "b.md"
    b.write_text("# title", encoding="utf-8")

    text = collect_context(
        repo_root=str(tmp_path),
        files=["a.py", "b.md"],
        max_files=10,
        max_chars_per_file=100,
    )
    assert "File: a.py" in text
    assert "File: b.md" in text


def test_collect_context_ignores_outside_file(tmp_path):
    inside = tmp_path / "a.py"
    inside.write_text("print('x')", encoding="utf-8")
    outside = tmp_path.parent / "outside.py"
    outside.write_text("print('y')", encoding="utf-8")
    try:
        text = collect_context(repo_root=str(tmp_path), files=["a.py", "../outside.py"])
        assert "File: a.py" in text
        assert "outside.py" not in text
    finally:
        if outside.exists():
            outside.unlink()
