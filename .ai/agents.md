---
id: AI-AGENTS-001
title: Rocky agent catalog
status: accepted
version: 1.0.0
owners: Rocky maintainers
last_updated: 2026-07-26
---

# Rocky agent catalog

Roles are capabilities, not vendor products. One person or tool may perform multiple roles, but
review independence should match the risk of the change. Every role follows the shared
[context](context.md).

| Role | Responsibilities | Required inputs | Outputs | Must not |
| --- | --- | --- | --- | --- |
| **Planner** | Trace the request, identify constraints, and propose bounded work. | Charter, PRD, ADRs, issue context. | Scope and ordered plan. | Invent missing requirements or approve decisions. |
| **Implementer** | Change code and documentation to satisfy the SPEC. | Accepted plan, EPKG SPEC, repository source. | Minimal diff and command log. | Expand scope or bypass repository checks. |
| **Verifier** | Execute TESTS and investigate failures. | Diff, TESTS, runnable environment. | Reproducible results and residual risks. | Alter acceptance criteria to make results pass. |
| **Reviewer** | Check traceability, correctness, safety, and clarity. | Governing artifacts, diff, evidence. | Findings and recommendation. | Claim human acceptance or conceal uncertainty. |
| **Documentarian** | Maintain navigation, terminology, and non-duplicative guidance. | Canonical artifacts and changed behavior. | Accurate linked documentation. | Create competing definitions. |
