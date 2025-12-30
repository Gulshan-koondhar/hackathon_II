# Data Model: 001-todo-cli

This document defines the core data entities and validation rules for the In-Memory Todo CLI.

## Task Entity

The `Task` is represented as a Python dictionary for simplicity and interoperability between agents.

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `id` | `int` | Unique identifier | Sequential, non-reusable, starts at 1 |
| `title` | `str` | Short task summary | Required, 1-200 chars, stripped |
| `description` | `str` | Detailed notes | Optional, max 1000 chars, defaults to "" |
| `completed` | `bool` | Completion status | Defaults to `False` |

### Validation Rules

1. **Title**:
   - MUST NOT be empty after stripping whitespace (FR-005, FR-006)
   - MAX length 200 characters (FR-007)
2. **Description**:
   - MAX length 1000 characters (FR-008)
3. **ID**:
   - MUST be a positive integer (FR-032)
   - Incremented by 1 for each new task; never reused even if deleted (FR-028)

## Shared State

The application state is maintained in a single module (`storage.py`) in-memory:

- `TASKS`: `List[Dict]` - Ordered collection of task objects.
- `NEXT_ID`: `int` - Pointer for the next available unique identifier.

## Standard Skill Response

All logic operations (skills) MUST return a dictionary with a consistent structure (FR-009):

```json
{
  "success": "bool",
  "message": "str",
  "data": "any | null"
}
```
