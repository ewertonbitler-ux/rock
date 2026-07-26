---
id: EPKG-0003-PROMPT
title: Knowledge Asset Core Domain execution guidance
status: proposed
version: 0.1.0
owners: Rocky maintainers
last_updated: 2026-07-26
epkg: EPKG-0003
issue: BIT-466
preparation_issue: BIT-470
---

# EPKG-0003 execution guidance

Implement BIT-466 from a clean checkout containing the accepted foundation files and proposed
architecture baseline listed in this package's [SPEC](SPEC.md). This guidance is provider-neutral
and requires no Jira, Confluence, private chat, or other inaccessible context. If any required
repository source is absent or conflicts with the SPEC, stop, record the commit SHA and conflict,
and do not invent missing requirements.

## Required reading and preconditions

Before editing, confirm a clean or understood worktree and read, in order:

1. [agent context](../../../.ai/context.md), root [README](../../../README.md),
   [handbook](../../../docs/handbook/REF-001.md), and [glossary](../../../docs/glossary.md);
2. [ARCH-001](../../../docs/architecture/ARCH-001.md),
   [CAT-001](../../../docs/catalog/CAT-001.md), and
   [ADR-001](../../../docs/adr/ADR-001.md) through
   [ADR-003](../../../docs/adr/ADR-003.md);
3. [EPKG-0001](../EPKG-0001/README.md), [EPKG-0002](../EPKG-0002/README.md), and this package in
   README, SPEC, PROMPT, TESTS, REVIEW order;
4. all current `src`, `tests`, templates, Makefile, `pyproject.toml`, and CI workflow files.

The SPEC is the normative implementation contract. Preserve unrelated work and make the smallest
coherent implementation.

## Execution contract

- Implement only `KnowledgeAsset`, its justified values/errors, the enumerated application use
  cases, and the minimal abstract repository port.
- Do not implement or alias runtime `Artifact`. Do not add speculative infrastructure, adapters,
  generic CRUD, persistence, frameworks, integrations, parsing, orchestration, or empty layers.
- Keep the core independent of Markdown, repository files, URLs, Git, providers, and external
  identity systems. Use test-local doubles rather than production in-memory repositories.
- Cover every item required by [TESTS](TESTS.md), including the entire lifecycle matrix and import
  boundaries. Update ARCH-001 and CAT-001 only after runtime evidence exists and only with factual
  status.
- Run the exact commands in TESTS. Record the command, exit code, and exact salient output in
  [REVIEW](REVIEW.md); never mark an unexecuted check as passed. Inspect the complete diff and every
  changed link, and record findings and deferrals.
- Prepare a commit whose message references BIT-466 and EPKG-0003, then prepare a pull request
  targeting `main` with scope, decisions, exact validation evidence, risks, and deferrals. Do not
  claim maintainer acceptance or merge.
