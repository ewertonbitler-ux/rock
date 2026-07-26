# Rocky Engineering Framework

Rocky is a repository-native framework for turning product intent into reviewable engineering
work. Decisions, requirements, implementation packages, and evidence live together so that a
human or an automated agent can reconstruct why a change exists.

## Start here

- [Product Charter](docs/charters/RKY-000.md) — mission, principles, boundaries, and success.
- [Product Definition](docs/prd/PRD-001.md) — users, capabilities, and acceptance criteria.
- [Engineering Handbook](docs/handbook/REF-001.md) — the delivery lifecycle and quality policy.
- [Architecture decisions](docs/adr/README.md) — accepted architectural constraints.
- [Documentation index](docs/README.md) — architecture, catalogs, governance, and product knowledge.
- [System Architecture](docs/architecture/ARCH-001.md) — capability status, contexts, layers, and dependencies.
- [Engineering Asset Catalog](docs/catalog/CAT-001.md) — canonical engineering assets and relationships.
- [Glossary](docs/glossary.md) — canonical terminology.
- [EPKG-0001](.specs/epkg/EPKG-0001/README.md) — the package defining this foundation.
- [EPKG-0002](.specs/epkg/EPKG-0002/README.md) — the architecture baseline package.
- [EPKG-0003](.specs/epkg/EPKG-0003/README.md) — the proposed Knowledge Asset Core Domain package.
- [AI context](.ai/context.md) — bounded, provider-neutral context for coding agents.

## Bootstrap and validation

Rocky requires Python 3.11 or later. The package includes the bounded, persistence-free Knowledge
Asset core domain specified by EPKG-0003; runtime Artifact and infrastructure remain excluded.

```shell
python -m pip install -e '.[dev]'
make check
```

Individual commands are `make lint`, `make type-check`, `make test`, and `make links`. See the
[handbook](docs/handbook/REF-001.md) before proposing a change.
