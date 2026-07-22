# CaptureOS

CaptureOS is an AI-assisted Proposal Operations and Capture Management system. It automates the proposal lifecycle — from opportunity discovery through proposal generation — while keeping accuracy, transparency, and human oversight at the center of the process.

## Workflow

Discovery → Verification → Validation → Qualification → Human Approval → Proposal Generation

## Agents

The system uses five single-responsibility AI agents:

- **Discovery** — finds new opportunities from approved sources
- **Verification** — confirms opportunities are legitimate and active
- **Validation** — cleans, deduplicates, and normalizes opportunity data
- **Qualification** — scores opportunities and recommends bid decisions
- **Proposal** — generates proposal assets after human approval

## Data Model

`schemas/Opportunity.json` is the single source of truth used and updated by all agents.

## Repository Structure

- `docs/` — architecture documentation
- `agents/` — agent specifications
- `prompts/` — agent prompts
- `schemas/` — data schemas
- `workflows/` — workflow documentation
- `n8n/` — automation workflows

See `CLAUDE.md` for full project instructions and design principles.
