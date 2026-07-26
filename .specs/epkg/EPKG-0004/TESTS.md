---
id: EPKG-0004-TESTS
title: Engagement Core Domain verification
status: proposed
version: 0.1.0
owners: Rocky maintainers
last_updated: 2026-07-26
epkg: EPKG-0004
---

# EPKG-0004 verification

## Automated checks

Run from the repository root:

```bash
python -m ruff check .
python -m mypy src tests
python -m pytest
python tests/check_markdown_links.py
make check
```

`make check` is the final required quality gate and must complete with exit code zero.

## Required behavior coverage

Tests must verify:

- canonical and invalid Engagement identifiers;
- creation in `draft` with deterministic timestamps;
- the valid lifecycle path and every invalid/terminal transition used by the public API;
- owner and participant conflict prevention;
- duplicate and missing participant handling;
- append-only immutable decision exposure;
- timezone-aware decision validation;
- milestone registration, case-insensitive uniqueness, completion, repeated completion rejection, and
  missing milestone handling;
- completed and cancelled aggregates reject subsequent mutation;
- aggregate collections are exposed as tuples rather than mutable internal collections.

## Architecture inspection

Review the changed source and confirm:

- `src/rocky/engagements/domain.py` imports only standard-library modules and local errors;
- no other Rocky domain is imported;
- no persistence, framework, provider, file, Markdown, Git, network, or integration dependency exists;
- no speculative repository, service, adapter, or event abstraction was introduced;
- the package public contract exports only justified domain types.

## Evidence requirements

Record in [REVIEW](REVIEW.md):

- command executed;
- exit code;
- salient result;
- CI run result and commit SHA;
- any known limitation or deferral.

An unexecuted check must remain marked as not verified.