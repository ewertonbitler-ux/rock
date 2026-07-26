# Rocky Engineering Framework

Rocky is a repository-native framework for turning product intent into reviewable engineering
work. Decisions, requirements, implementation packages, and evidence live together so that a
human or an automated agent can reconstruct why a change exists.

## Start here

- [Product Charter](docs/charters/RKY-000.md) — mission, principles, boundaries, and success.
- [Product Definition](docs/prd/PRD-001.md) — users, capabilities, and acceptance criteria.
- [Engineering Handbook](docs/handbook/REF-001.md) — the delivery lifecycle and quality policy.
- [Architecture decisions](docs/adr/README.md) — accepted architectural constraints.
- [Glossary](docs/glossary.md) — canonical terminology.
- [EPKG-0001](.specs/epkg/EPKG-0001/README.md) — the package defining this foundation.
- [AI context](.ai/context.md) — bounded, provider-neutral context for coding agents.

## Bootstrap and validation

Rocky requires Python 3.11 or later. The package deliberately contains metadata only; product
domain classes are outside this foundation issue.

```shell
python -m pip install -e '.[dev]'
make check
```

Individual commands are `make lint`, `make type-check`, `make test`, and `make links`. See the
[handbook](docs/handbook/REF-001.md) before proposing a change.
