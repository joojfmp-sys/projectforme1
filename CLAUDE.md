# CaptureOS AI Project Instructions

## Purpose

CaptureOS is an AI-assisted Proposal Operations and Capture Management system.

Its purpose is to automate as much of the proposal lifecycle as possible while maintaining accuracy, transparency, and human oversight.

The objective is not to build AI for the sake of AI.

The objective is to build a practical business system that consistently produces qualified opportunities, supports bid decisions, and generates high-quality proposal drafts with minimal manual effort.

Every feature must contribute directly to this objective.

---

# Business Goal

CaptureOS should automate the workflow from opportunity discovery through proposal generation.

The desired workflow is:

Discovery
→ Verification
→ Validation
→ Qualification
→ Human Approval
→ Proposal Generation

The system should reduce manual work, improve consistency, and increase proposal throughput without unnecessary complexity.

---

# Design Philosophy

The system must remain simple.

Prefer simple solutions over complex ones.

Do not introduce additional architecture, abstraction, or AI agents unless there is a clear business need.

Every component must have a measurable purpose.

If something does not significantly improve automation, accuracy, reliability, or maintainability, it should not be added.

This project values simplicity over cleverness.

---

# Core Principles

1. One AI Agent = One Responsibility.

Each AI agent should perform one clearly defined task.

2. Every agent produces structured output.

Agents should return structured data rather than long conversational responses whenever possible.

3. One Source of Truth.

The Opportunity.json schema is the primary data model used throughout the system.

All agents read from it and update it.

Do not create multiple competing schemas.

4. Human Approval Required.

Proposal generation should never begin automatically.

Human approval is required before proposal creation.

5. Automation First.

Whenever repetitive work can be automated reliably, automate it.

---

# AI Agents

The system currently contains only five AI agents.

Do not add more agents unless explicitly instructed.

1. Discovery Agent

Purpose:
Find new proposal opportunities from approved sources.

Output:
Basic opportunity information.

---

2. Verification Agent

Purpose:
Verify that opportunities are legitimate and active.

Examples:
- Source is valid
- Opportunity is open
- Required documents exist
- Deadline exists

Output:
Verified / Not Verified.

---

3. Validation Agent

Purpose:
Clean and normalize opportunity data.

Responsibilities include:
- duplicate detection
- missing fields
- normalization
- business rule validation

Output:
Validated opportunity record.

---

4. Qualification Agent

Purpose:
Determine whether an opportunity is worth pursuing.

Responsibilities include:
- strategic fit
- estimated value
- risk
- confidence score
- recommendation

Output:
Qualification score and recommendation.

---

5. Proposal Agent

Purpose:
Generate proposal assets only after human approval.

Examples:
- compliance matrix
- proposal outline
- SME questions
- proposal draft

---

# Workflow

The workflow must always remain:

Discovery

↓

Verification

↓

Validation

↓

Qualification

↓

CaptureOS Dashboard

↓

Human Approval

↓

Proposal Generation

Do not change this workflow without approval.

---

# Repository Structure

Maintain the approved repository structure.

Do not create new folders without approval.

Do not rename folders.

Do not reorganize files.

Keep the repository clean.

---

# Coding Philosophy

Prefer readability over cleverness.

Prefer maintainability over optimization.

Avoid unnecessary abstractions.

Avoid premature optimization.

Build only what is needed today.

Future expansion should be easy but should not complicate today's implementation.

---

# Documentation Standards

Every major component should clearly describe:

Purpose

Inputs

Outputs

Responsibilities

Failure Conditions

Dependencies

Assumptions

Avoid unnecessary documentation.

Documentation should help future maintenance.

---

# Prompt Design Standards

Prompts should be:

clear

deterministic

repeatable

focused on one responsibility

Avoid vague instructions.

Avoid unnecessary conversational language.

Prefer structured outputs.

---

# Error Handling

Agents should fail gracefully.

If required information is missing:

identify it

report it

request clarification

never invent missing information

Accuracy is more important than completion.

---

# Constraints

Do not invent requirements.

Do not invent workflows.

Do not invent architecture.

Do not create additional AI agents.

Do not create unnecessary configuration files.

Do not overengineer solutions.

Always ask before making significant architectural changes.

---

# Success Criteria

CaptureOS is successful when:

Opportunity discovery requires minimal manual work.

Verified opportunities are accurate.

Duplicate opportunities are eliminated.

Qualification recommendations are consistent.

Proposal generation begins only after approval.

The repository remains clean and understandable.

The system is easy to maintain and expand.

---

# Working Style

When asked to implement something:

Think first.

Keep solutions simple.

Explain reasoning when appropriate.

Implement only the requested scope.

If multiple approaches exist, recommend the simplest one that satisfies the business objective.

When uncertain, ask rather than assume.

The goal is to build a production-quality business system, not a technology demonstration.
