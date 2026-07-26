import ast
from pathlib import Path

ROOT = Path(__file__).parents[1]


def imports(path: Path) -> set[str]:
    tree = ast.parse(path.read_text())
    return {node.module or "" for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)}


def test_domain_has_only_standard_library_and_errors_dependencies() -> None:
    assert imports(ROOT / "src/rocky/knowledge_assets/domain.py") <= {
        "__future__",
        "collections.abc",
        "dataclasses",
        "enum",
        "functools",
        "types",
        "typing",
        "errors",
    }


def test_no_production_adapters_or_excluded_runtime_modules() -> None:
    files = {p.name for p in (ROOT / "src/rocky/knowledge_assets").iterdir()}
    assert files == {
        "__init__.py",
        "domain.py",
        "errors.py",
        "application.py",
        "ports.py",
        "__pycache__",
    } or files == {"__init__.py", "domain.py", "errors.py", "application.py", "ports.py"}
    assert not any(p.stem.lower() == "artifact" for p in (ROOT / "src").rglob("*.py"))
