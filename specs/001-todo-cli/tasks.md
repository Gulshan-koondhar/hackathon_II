# Tasks: 001-todo-cli

**Feature**: Phase 1 In-Memory Todo CLI
**Implementation Strategy**: MVP-first (User Story 1), then incremental delivery of toggle, update, and delete. Standard standardized response format utilized across all agents.

## Phase 1: Setup

- [X] T001 Create project directories: agents/, tests/
- [X] T002 Initialize agents/__init__.py
- [X] T003 [P] Create shared state repository in storage.py
- [X] T004 Setup pytest configuration and fixtures in tests/conftest.py

## Phase 2: Foundational

- [X] T005 [P] Implement base Response structure and shared constants in agents/__init__.py
- [X] T006 [P] Implement Task storage logic and next_id incrementer in storage.py

## Phase 3: User Story 1 - Add and View Tasks (Priority: P1)

**Goal**: Enable basic task capture and listing.
**Independent Test**: Add task "Buy groceries" and verify it appears in the list output with ID 1.

- [X] T007 [P] [US1] Write unit tests for add_task and list_tasks in tests/test_manager.py and tests/test_viewer.py
- [X] T008 [US1] Implement add_task skill in agents/manager.py
- [X] T009 [US1] Implement list_tasks and format_list skills in agents/viewer.py
- [X] T010 [US1] Implement basic CLI orchestration loop in main.py (Add and List options)
- [X] T011 [US1] Create end-to-end test for add/list flow in tests/test_e2e.py

## Phase 4: User Story 2 - Mark Tasks Complete (Priority: P2)

**Goal**: Enable completion status tracking.
**Independent Test**: Add a task, toggle it, and verify status is "Completed" in list.

- [X] T012 [P] [US2] Write unit tests for toggle_task in tests/test_manager.py
- [X] T013 [US2] Implement toggle_task skill in agents/manager.py
- [X] T014 [US2] Update format_list in agents/viewer.py to visually distinguish completed tasks
- [X] T015 [US2] Add "Toggle Complete" option to CLI menu in main.py

## Phase 5: User Story 3 - Update Task Details (Priority: P3)

**Goal**: Enable modification of existing tasks.
**Independent Test**: Update task title and verify change in list output.

- [X] T016 [P] [US3] Write unit tests for update_task in tests/test_manager.py
- [X] T017 [US3] Implement update_task skill in agents/manager.py
- [X] T018 [US3] Add "Update Task" option to CLI menu in main.py

## Phase 6: User Story 4 - Remove Unwanted Tasks (Priority: P4)

**Goal**: Enable task deletion.
**Independent Test**: Delete a task and verify it no longer appears in list output.

- [X] T019 [P] [US4] Write unit tests for delete_task in tests/test_manager.py
- [X] T020 [US4] Implement delete_task skill in agents/manager.py
- [X] T021 [US4] Add "Delete Task" option to CLI menu in main.py

## Phase 7: Analytics Component (Cross-cutting)

**Goal**: Provide task statistics.
**Independent Test**: Select "Show Stats" and see correct counts for total/pending/completed.

- [X] T022 [P] Write unit tests for analytics in tests/test_analytics.py
- [X] T023 Implement TaskAnalyticsAgent in agents/analytics.py
- [X] T024 Add "Show Stats" option to CLI menu in main.py

## Phase 8: Polish & Final Verification

- [X] T025 [P] Review all error messages for consistency and clarity (FR-033)
- [X] T026 Add "Exit" option and final cleanup to main.py
- [X] T027 Run all tests and verify 100% pass rate
- [X] T028 Perform manual end-to-end walkthrough matching success criteria (SC-001 to SC-010)

## Dependency Graph

```text
Setup [T001-T004]
  └─ Foundational [T005-T006]
      └─ [US1] Add/View [T007-T011]
          ├─ [US2] Toggle [T012-T015]
          ├─ [US3] Update [T016-T018]
          └─ [US4] Delete [T019-T021]
              └─ Analytics [T022-T024]
                  └─ Polish [T025-T028]
```

## Parallel Execution Opportunities

- T003 & T004 (independent setup files)
- T012, T016, T019 (independent skills within manager.py, once US1 is stable)
- T022 & T023 (analytics agent is largely independent of CRUD implementation)
