from __future__ import annotations

from pathlib import Path
from typing import Iterable


DEFAULT_INCLUDE = ["*.py", "*.md", "*.txt", "*.yaml", "*.yml", "*.json", "*.toml"]
DEFAULT_EXCLUDE_DIRS = {".git", ".venv", "venv", "node_modules", "dist", "build", "__pycache__"}


def collect_context(
    repo_root: str = ".",
    files: list[str] | None = None,
    include_globs: list[str] | None = None,
    max_files: int = 20,
    max_chars_per_file: int = 5000,
) -> str:
    root = Path(repo_root).resolve()
    if not root.exists() or not root.is_dir():
        raise ValueError(f"Invalid repo_root: {repo_root}")

    include_globs = include_globs or DEFAULT_INCLUDE
    selected = _resolve_files(root, files, include_globs)
    selected = selected[: max(0, max_files)]

    chunks: list[str] = []
    for path in selected:
        try:
            rel = path.relative_to(root)
        except ValueError:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        text = text[: max(0, max_chars_per_file)]
        chunks.append(f"File: {rel.as_posix()}\n\n{text}")

    return "\n\n".join(chunks)


def _resolve_files(root: Path, files: list[str] | None, include_globs: Iterable[str]) -> list[Path]:
    if files:
        out: list[Path] = []
        for entry in files:
            path = (root / entry).resolve()
            if _is_inside(path, root) and path.exists() and path.is_file():
                out.append(path)
        return sorted(set(out))

    found: list[Path] = []
    for pattern in include_globs:
        for path in root.rglob(pattern):
            if not path.is_file():
                continue
            if _is_excluded(path, root):
                continue
            found.append(path)
    return sorted(set(found))


def _is_inside(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def _is_excluded(path: Path, root: Path) -> bool:
    try:
        rel_parts = path.relative_to(root).parts
    except ValueError:
        return True
    return any(part in DEFAULT_EXCLUDE_DIRS for part in rel_parts)
