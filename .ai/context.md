---
id: AI-CONTEXT-001
title: Rocky agent context
status: accepted
version: 1.0.0
owners: Rocky maintainers
last_updated: 2026-07-26
---

# Rocky agent context

## Purpose and authority

Rocky makes engineering intent and evidence repository-native. Begin with the
[root navigation](../README.md), then read the artifact governing the requested change. This file
is operational context, not a replacement for the [charter](../docs/charters/RKY-000.md),
[requirements](../docs/prd/PRD-001.md), accepted [decisions](../docs/adr/README.md), or an EPKG SPEC.
If instructions conflict, follow the authority order in the
[handbook](../docs/handbook/REF-001.md) and surface the conflict.

## Working contract

1. Confirm the requested scope and find its EPKG. Do not infer inaccessible ticket or chat content.
2. Read repository instructions, the SPEC, applicable ADRs, relevant source, and tests before editing.
3. Make the smallest coherent change. Do not add speculative domain types or AI-provider coupling.
4. Update the canonical artifact rather than copying policy or terminology elsewhere.
5. Run every command in the TESTS plan and record exact results in REVIEW.
6. Inspect the final diff for contradictions, duplication, placeholders, secrets, broken links, and unrelated work.

Agents may propose changes and evidence; they may not accept ADRs, waive quality gates, expose
secrets, or claim maintainer approval. The [agent catalog](agents.md) defines available roles.
