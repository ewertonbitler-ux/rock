"""Fail when a repository-local Markdown link does not resolve."""

import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"(?<!!)\[[^]]*]\(([^)]+)\)")


def broken_links() -> list[str]:
    broken: list[str] = []
    for document in ROOT.rglob("*.md"):
        if any(part.startswith(".") and part not in {".ai", ".specs"} for part in document.parts):
            continue
        for target in LINK.findall(document.read_text(encoding="utf-8")):
            target = target.strip().split(maxsplit=1)[0].strip("<>")
            if not target or target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            path = unquote(target.split("#", 1)[0])
            if path and not (document.parent / path).resolve().exists():
                broken.append(f"{document.relative_to(ROOT)}: {target}")
    return broken


if __name__ == "__main__":
    failures = broken_links()
    if failures:
        raise SystemExit("Broken Markdown links:\n" + "\n".join(failures))
    print("All relative Markdown links resolve.")
