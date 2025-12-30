# Implementation Plan: 001-todo-cli (Phase 1 In-Memory Todo CLI)

**Branch**: `001-todo-cli` | **Date**: 2025-12-30 | **Spec**: `/specs/001-todo-cli/spec.md`
**Input**: Phase 1 – In-Memory Todo CLI (Spec-Driven Development)

## Summary

Implement a minimal, correct in-memory Todo application using a CLI menu loop. The system will favor simplicity, using standard Python data structures (list/dict) for storage and a suite of "domain intelligence" agents/skills for logic. The interaction will be menu-driven (numbered user input).

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: None (Standard Library only)
**Storage**: In-memory (Python `list` of `dict` objects)
**Testing**: `pytest`
**Target Platform**: CLI (Windows/macOS/Linux)
**Project Type**: Single project / CLI app
**Performance Goals**: Instant response (<100ms) for CRUD operations
**Constraints**: No persistence, no external dependencies, non-reusable sequential IDs
**Scale/Scope**: Support 1000+ tasks in a single session

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **Specification-First**: spec.md is comprehensive and reviewed.
- [x] **Phase Discipline**: Only Phase 1 operations (Add, Update, Delete, List, Toggle) are included.
- [x] **Simplicity**: No database, no web UI, no complex patterns.
- [x] **Reusable Domain Intelligence**: Logic isolated into TaskManager, TaskViewer, TaskAnalytics agents.
- [x] **Deterministic**: standardized dictionary returns for all logic units.
- [x] **TDD**: pytest environment will be established first.

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-cli/
├── plan.md              # This file
├── data-model.md        # Core data structures (Task dict)
├── quickstart.md        # Instructions for Hackathon evaluators
├── contracts/           # Skill/Agent interfaces
│   ├── task_manager.md
│   ├── task_viewer.md
│   └── task_analytics.md
└── tasks.md             # Testable work packages
```

### Source Code (repository root)

```text
agents/             # Logic units (Domain Intelligence)
├── __init__.py
├── manager.py      # TaskManagerAgent (Add, Update, Delete, Toggle)
├── viewer.py       # TaskViewerAgent (List, Format)
└── analytics.py    # TaskAnalyticsAgent (Stats/Counts)
storage.py          # Shared in-memory list and next_id counter
main.py             # CLI Menu loop orchestration

tests/                  # TDD tests
├── conftest.py
├── test_manager.py
├── test_viewer.py
├── test_analytics.py
└── test_e2e.py         # Scenario validations from spec
```

**Structure Decision**: A simple package-based structure separating Domain Logic (agents) from Interface (main.py) and State (storage). This allows easy extension for future phases while remaining minimal for Phase 1.

## Complexity Tracking

*No violations identified.*
