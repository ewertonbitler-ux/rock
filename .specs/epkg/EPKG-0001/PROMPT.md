---
id: EPKG-0001-PROMPT
title: Rocky Engineering Framework foundation execution guidance
status: accepted
version: 1.0.0
owners: Rocky maintainers
last_updated: 2026-07-26
epkg: EPKG-0001
---

# EPKG-0001 execution guidance

Act as the Implementer role in the [agent catalog](../../../.ai/agents.md). Read the
[shared context](../../../.ai/context.md), then the package [SPEC](SPEC.md), governing product
artifacts, ADRs, current bootstrap files, workflows, and tests. Preserve working behavior.

Create only the artifacts and navigation required by the SPEC. Use the glossary exactly, keep
metadata consistent, and replace repeated explanations with relative links to canonical sources.
Do not create domain classes or provider-specific AI code/configuration.

Run the commands in [TESTS](TESTS.md), inspect the complete diff, and update
[REVIEW](REVIEW.md) with factual results. Report uncertainty; never fabricate evidence or maintainer
approval.
