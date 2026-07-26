---
id: EPKG-0002-PROMPT
title: Rocky architecture baseline execution guidance
status: proposed
version: 0.1.0
owners: Rocky maintainers
last_updated: 2026-07-26
epkg: EPKG-0002
issue: BIT-465
---

# EPKG-0002 execution guidance

Act as the Implementer and Documentarian roles in the
[agent catalog](../../../.ai/agents.md). Read the shared [context](../../../.ai/context.md), root
README, handbook, glossary, ADR-001 through ADR-003, then this package [SPEC](SPEC.md). Inspect the
existing templates, tests, Makefile, Python configuration, and CI before editing.

Create a documentation-only architecture baseline and catalog. Separate observable implementation
from plans and hypotheses. Do not turn Artifact, Workspace, persistence, integration, or provider
ideas into runtime types or technology decisions. Preserve EPKG-0001 and link to canonical content.

Run every command in [TESTS](TESTS.md), inspect all Markdown links and the complete diff, then record
only observed results in [REVIEW](REVIEW.md). Do not claim maintainer acceptance.
