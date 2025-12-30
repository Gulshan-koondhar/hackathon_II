# Skill: Test Task Data Integrity

## Metadata
- **Skill ID**: `qa.test-task-data-integrity`
- **Owner Agent**: QA Agent
- **Project**: Todo App (Phase I)
- **Category**: Quality Assurance - Data Integrity & Consistency
- **Version**: 1.0.0
- **Last Updated**: 2025-12-28

## Purpose

Verify that task data maintains consistency, accuracy, and integrity throughout its lifecycle in the Todo App Phase I. This skill tests that task IDs remain unique, task state transitions are valid, concurrent operations don't corrupt data, and storage operations preserve data fidelity. It focuses on data-level guarantees rather than operation-level validation.

## When to Use

Use this skill when:
- Implementing or modifying storage mechanisms (in-memory, file-based, database)
- Before deploying updates that affect task persistence or retrieval
- After refactoring data access layers or storage adapters
- When investigating data corruption or inconsistency bug reports
- As part of integration testing after database schema changes
- Before switching storage backends (e.g., in-memory to file-based)
- When validating data migration scripts or data import/export features
- As a pre-release quality gate for data-critical changes

Do NOT use this skill for:
- Testing business logic or validation rules (use `validate-task-operations` instead)
- UI/UX validation or user interaction testing
- API contract testing (use dedicated API testing skills)
- Performance benchmarking or load testing

## Inputs

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `storage_type` | string | No | `"in-memory"` | Storage implementation: `"in-memory"`, `"file-based"`, `"database"` |
| `test_concurrency` | boolean | No | `true` | Test concurrent operation handling |
| `test_persistence` | boolean | No | `true` | Test data persistence across operations |
| `test_recovery` | boolean | No | `true` | Test data recovery from corruption scenarios |
| `sample_size` | integer | No | `100` | Number of tasks for large-scale tests (1-1000) |
| `corruption_scenarios` | array | No | `["all"]` | Scenarios to test: `"id_collision"`, `"state_corruption"`, `"orphaned_data"`, `"duplicate_entries"`, `"all"` |
| `verbose_output` | boolean | No | `false` | Enable detailed test execution logs |

### Input Example
```json
{
  "storage_type": "file-based",
  "test_concurrency": true,
  "test_persistence": true,
  "test_recovery": true,
  "sample_size": 50,
  "corruption_scenarios": ["id_collision", "state_corruption"],
  "verbose_output": true
}
```

## Step-by-Step Process

### Phase 1: Environment Setup and Baseline (2-3 minutes)

**Step 1.1: Storage Configuration**
- Initialize storage based on `storage_type`:
  - **In-Memory**: Create fresh task list in memory
  - **File-Based**: Create temporary test directory, initialize JSON file
  - **Database**: Create test database/schema, establish connection
- Verify storage is empty and accessible
- Record storage location/identifier for cleanup

**Step 1.2: Test Data Preparation**
- Generate deterministic test task set:
  ```python
  test_tasks = [
    {"id": 1, "title": "Task Alpha", "description": "First test task", "completed": False},
    {"id": 2, "title": "Task Beta", "description": "Second test task", "completed": False},
    {"id": 3, "title": "Task Gamma", "description": "Third test task", "completed": True},
    # ... up to sample_size
  ]
  ```
- Create baseline checksums for data verification:
  - Task count checksum
  - ID sequence checksum
  - Content hash for each task
- Store baseline for comparison in later phases

**Step 1.3: Integrity Constraint Definition**
- Define immutable data rules to verify:
  - **ID Uniqueness**: No two tasks can share the same ID
  - **ID Monotonicity**: New task IDs must be > max existing ID
  - **State Validity**: Completed field is always boolean
  - **No Orphans**: All tasks in storage are complete objects (no missing required fields)
  - **Referential Integrity**: Task references (if Phase I has relationships) are valid
  - **Content Preservation**: Task content doesn't change unless explicitly updated

### Phase 2: Integrity Test Execution (8-15 minutes)

**Step 2.1: ID Uniqueness and Sequence Integrity**
```
Test: Sequential ID generation
Action: Add 10 tasks sequentially
Verification:
  - IDs are 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 (no gaps)
  - No duplicate IDs exist
  - Max ID = 10

Test: ID persistence after deletion
Action:
  1. Add tasks 1-5
  2. Delete task 3
  3. Add new task
Verification:
  - New task gets ID 6 (not reusing deleted ID 3)
  - IDs remain: 1, 2, 4, 5, 6
  - ID sequence integrity maintained

Test: Large-scale ID uniqueness
Action: Add sample_size tasks (e.g., 100)
Verification:
  - All 100 tasks have unique IDs
  - IDs form continuous sequence 1-100
  - No collisions detected
  - Query by any ID returns exactly one task

Test: ID collision attempt
Action: Manually insert task with existing ID (bypass add_task validation)
Verification:
  - Storage rejects duplicate ID
  - OR storage overwrites old task (document behavior)
  - Integrity check detects the collision
  - System logs error/warning
```

**Step 2.2: State Consistency Across Operations**
```
Test: State preservation during read
Action:
  1. Create task {"id": 1, "title": "Test", "completed": False}
  2. Read task 10 times consecutively
Verification:
  - All 10 reads return identical data
  - completed remains False
  - title, description unchanged
  - No unexpected state mutations

Test: Atomic state updates
Action:
  1. Update task 1: completed = True
  2. Immediately read task 1
  3. Update task 1: title = "Updated"
  4. Immediately read task 1
Verification:
  - Step 2: completed=True is persisted
  - Step 4: title="Updated" AND completed=True (both changes preserved)
  - No partial updates or rollbacks

Test: State isolation between tasks
Action:
  1. Update task 1: completed = True
  2. Update task 2: title = "Changed"
  3. Read both tasks
Verification:
  - Task 1: only completed changed
  - Task 2: only title changed
  - No cross-contamination of updates
  - All other fields remain original values

Test: Invalid state rejection
Action: Attempt to set completed = "yes" (string instead of boolean)
Verification:
  - Update rejected with error
  - Task state unchanged from before attempt
  - No partial state corruption
  - Storage integrity maintained
```

**Step 2.3: Concurrent Operation Integrity (if test_concurrency=true)**
```
Test: Simultaneous creates
Action: Simulate 5 concurrent add_task calls
Verification:
  - All 5 tasks successfully created
  - All 5 have unique IDs (no collisions)
  - ID sequence is 1-5 (order may vary)
  - No tasks lost or overwritten

Test: Concurrent read-update-read
Action:
  1. Create task 1
  2. Thread A: Read task 1
  3. Thread B: Update task 1 (completed=True)
  4. Thread A: Read task 1 again
Verification:
  - Thread A's second read sees updated state
  - No stale data returned
  - Update is not lost

Test: Concurrent updates to same task
Action:
  1. Create task 1
  2. Thread A: Update task 1 (title="A")
  3. Thread B: Update task 1 (title="B") [simultaneous]
Verification:
  - Final state has one of the titles ("A" or "B")
  - No partial merge (title is complete, not corrupted)
  - Last write wins OR first write wins (document behavior)
  - No data corruption or exceptions

Test: Concurrent delete operations
Action:
  1. Create tasks 1, 2, 3
  2. Thread A: Delete task 2
  3. Thread B: Delete task 2 [simultaneous]
Verification:
  - One operation succeeds, one returns "not found" error
  - Task 2 is deleted (not duplicated or corrupted)
  - Other tasks (1, 3) are unaffected
  - Storage remains consistent
```

**Step 2.4: Persistence and Durability (if test_persistence=true)**
```
Test: Data survives storage reload (file-based/database)
Action:
  1. Add 5 tasks
  2. Record checksums
  3. Close storage connection
  4. Reopen storage connection
  5. Read all tasks
Verification:
  - All 5 tasks present after reload
  - Task data matches original (checksums identical)
  - No data loss or corruption during persistence cycle

Test: Partial write protection
Action:
  1. Add task 1
  2. Simulate storage failure during task 2 write (kill process mid-write)
  3. Restart/reload storage
Verification:
  - Task 1 is fully present and valid
  - Task 2 is either fully present OR completely absent (no partial writes)
  - Storage is not corrupted
  - Can continue adding tasks normally

Test: Large dataset persistence
Action:
  1. Add sample_size tasks (e.g., 100)
  2. Update 20 random tasks
  3. Delete 10 random tasks
  4. Persist to storage
  5. Reload and verify
Verification:
  - Remaining 90 tasks all present
  - Updated tasks reflect changes
  - Deleted tasks absent
  - No extra or missing tasks
  - Data checksums match expected state
```

**Step 2.5: Recovery from Corruption (if test_recovery=true)**
```
Scenario: ID collision detection
Setup: Manually corrupt storage to have two tasks with id=5
Action: Run integrity check
Verification:
  - Collision detected and reported
  - System suggests remediation (e.g., reassign IDs)
  - Corruption logged with specific IDs

Scenario: State corruption detection
Setup: Set completed field to invalid value (e.g., null, string "yes")
Action: Load task and attempt operation
Verification:
  - Invalid state detected on load
  - System rejects invalid task or auto-corrects
  - Error logged with task ID and invalid field
  - Other tasks unaffected

Scenario: Orphaned data cleanup
Setup: Create task with missing required field (e.g., no "title")
Action: Run integrity scan
Verification:
  - Orphaned/malformed task detected
  - System reports incomplete data structure
  - Option to repair (add default title) or remove
  - Task count reflects cleaned state

Scenario: Duplicate entry removal
Setup: Duplicate same task object in storage
Action: Deduplicate operation
Verification:
  - Duplicate detected (same ID appearing twice)
  - One instance removed, one preserved
  - Final task count is correct
  - No data loss from valid tasks
```

**Step 2.6: Referential Integrity (if applicable in Phase I)**
```
Test: Task relationships (if Phase I has task dependencies)
Action:
  1. Create parent task 1
  2. Create child task 2 (depends on task 1)
  3. Delete parent task 1
Verification:
  - Delete blocked OR child task dependency updated/cleared
  - No orphaned references
  - System enforces referential integrity rules
  - Data model consistency maintained

Test: Cascade operations (if supported)
Action:
  1. Create task with subtasks
  2. Delete parent task with cascade option
Verification:
  - Parent and all children deleted
  - No orphaned subtasks
  - Storage reflects complete cascade
  - Integrity check passes
```

### Phase 3: Analysis and Reporting (3-5 minutes)

**Step 3.1: Integrity Metrics Calculation**
- Count integrity violations by category:
  - ID collisions
  - State inconsistencies
  - Orphaned data
  - Referential integrity violations
  - Persistence failures
- Calculate data fidelity score:
  ```
  Fidelity Score = (Total Tests - Violations) / Total Tests × 100%
  ```
- Assess severity of each violation (Critical, High, Medium, Low)

**Step 3.2: Corruption Impact Analysis**
For each detected issue:
```
Violation: ID Collision
Affected Records: Task ID 5 (2 instances)
Severity: CRITICAL
Impact: Data corruption - Task 5 content ambiguous, retrieval returns wrong data
Root Cause: ID generator not checking for existing IDs before assignment
Data at Risk: 2 tasks, potential for user data loss
Remediation: Implement ID uniqueness check in add_task method
```

**Step 3.3: Recommendations Generation**
- Prioritize fixes by severity and impact
- Suggest preventive measures (constraints, validation, tests)
- Provide code snippets for common fixes
- Reference affected files and line numbers
- Estimate remediation effort (low/medium/high)

**Step 3.4: Baseline Comparison**
- Compare final state to baseline checksums
- Report any unexpected data changes
- Verify no silent data corruption occurred during testing
- Confirm test isolation (no interference between tests)

## Output

### Success Output Format
```json
{
  "status": "PASS",
  "integrity_score": 100,
  "summary": {
    "storage_type": "in-memory",
    "total_tests": 22,
    "passed": 22,
    "failed": 0,
    "violations_detected": 0,
    "execution_time_seconds": 12.7
  },
  "test_categories": {
    "id_integrity": {"passed": 4, "failed": 0},
    "state_consistency": {"passed": 4, "failed": 0},
    "concurrency": {"passed": 4, "failed": 0},
    "persistence": {"passed": 3, "failed": 0},
    "corruption_recovery": {"passed": 4, "failed": 0},
    "referential_integrity": {"passed": 3, "failed": 0}
  },
  "data_fidelity": {
    "tasks_created": 100,
    "tasks_preserved": 100,
    "data_loss_incidents": 0,
    "corruption_incidents": 0,
    "checksum_mismatches": 0
  },
  "storage_metrics": {
    "read_operations": 450,
    "write_operations": 180,
    "delete_operations": 20,
    "errors_encountered": 0,
    "average_operation_time_ms": 2.3
  },
  "recommendations": [
    "Data integrity verified for in-memory storage",
    "System ready for production deployment",
    "Consider implementing automated integrity checks in production",
    "Add monitoring for ID sequence anomalies"
  ]
}
```

### Failure Output Format
```json
{
  "status": "FAIL",
  "integrity_score": 72.7,
  "summary": {
    "storage_type": "file-based",
    "total_tests": 22,
    "passed": 16,
    "failed": 6,
    "violations_detected": 6,
    "execution_time_seconds": 14.2
  },
  "test_categories": {
    "id_integrity": {"passed": 3, "failed": 1},
    "state_consistency": {"passed": 4, "failed": 0},
    "concurrency": {"passed": 2, "failed": 2},
    "persistence": {"passed": 2, "failed": 1},
    "corruption_recovery": {"passed": 3, "failed": 1},
    "referential_integrity": {"passed": 2, "failed": 1}
  },
  "violations": [
    {
      "violation_id": "ID_COLLISION_001",
      "category": "ID Integrity",
      "severity": "CRITICAL",
      "test_id": "ID_004",
      "description": "ID collision detected after concurrent task creation",
      "details": {
        "colliding_id": 5,
        "instances_found": 2,
        "task_contents": [
          {"id": 5, "title": "Task from Thread A", "completed": false},
          {"id": 5, "title": "Task from Thread B", "completed": false}
        ]
      },
      "impact": "Two distinct tasks share ID 5, causing retrieval ambiguity and potential data loss",
      "root_cause": "ID generator is not thread-safe; concurrent calls generated same ID",
      "affected_code": ".claude/agents/task-manager-agent.md:39-41",
      "remediation": "Implement atomic ID generation with locking mechanism or database sequence",
      "remediation_effort": "MEDIUM",
      "data_at_risk": "2 tasks, user data may be overwritten or lost"
    },
    {
      "violation_id": "PERSIST_002",
      "category": "Persistence",
      "severity": "HIGH",
      "test_id": "PERSIST_002",
      "description": "Partial write detected after simulated failure",
      "details": {
        "task_id": 42,
        "state": "INCOMPLETE",
        "missing_fields": ["description"],
        "file_location": "/tmp/test_tasks.json:line 178"
      },
      "impact": "Task 42 is corrupted in storage; application may crash on load",
      "root_cause": "File writes are not atomic; no transaction support for JSON storage",
      "affected_code": "storage/file-adapter.py:23-31 (if implemented)",
      "remediation": "Use atomic file writes (write to temp file, then rename) or add write-ahead logging",
      "remediation_effort": "MEDIUM",
      "data_at_risk": "1 task corrupted, potential for more under heavy load"
    },
    {
      "violation_id": "CONCUR_003",
      "category": "Concurrency",
      "severity": "HIGH",
      "test_id": "CONCUR_003",
      "description": "Lost update detected during concurrent modifications",
      "details": {
        "task_id": 7,
        "thread_a_update": {"title": "Updated by A"},
        "thread_b_update": {"completed": true},
        "final_state": {"title": "Updated by A", "completed": false},
        "lost_update": "completed=true from Thread B"
      },
      "impact": "Thread B's update was silently lost; task completion not recorded",
      "root_cause": "Read-modify-write cycle is not atomic; no optimistic concurrency control",
      "affected_code": ".claude/agents/task-manager-agent.md:51-61 (update_task)",
      "remediation": "Implement version field or timestamp-based optimistic locking",
      "remediation_effort": "HIGH",
      "data_at_risk": "Any concurrent updates to same task"
    }
  ],
  "data_fidelity": {
    "tasks_created": 100,
    "tasks_preserved": 98,
    "data_loss_incidents": 2,
    "corruption_incidents": 1,
    "checksum_mismatches": 3
  },
  "storage_metrics": {
    "read_operations": 450,
    "write_operations": 180,
    "delete_operations": 20,
    "errors_encountered": 6,
    "average_operation_time_ms": 3.1
  },
  "recommendations": [
    "CRITICAL: Fix ID collision in concurrent scenarios (ID_COLLISION_001) - High user impact",
    "HIGH: Implement atomic file writes to prevent corruption (PERSIST_002)",
    "HIGH: Add concurrency control for update operations (CONCUR_003)",
    "Consider switching to database storage for better ACID guarantees",
    "Add integration tests specifically for concurrent operations",
    "Implement health check to detect corruption in production"
  ],
  "priority_fixes": [
    {
      "order": 1,
      "violation_id": "ID_COLLISION_001",
      "rationale": "Critical severity, affects data uniqueness guarantees, high user impact"
    },
    {
      "order": 2,
      "violation_id": "PERSIST_002",
      "rationale": "High severity, can cause application crashes, data corruption risk"
    },
    {
      "order": 3,
      "violation_id": "CONCUR_003",
      "rationale": "High severity, silent data loss, affects concurrent usage"
    }
  ]
}
```

### Console Output (when verbose_output=true)
```
🔒 Todo App Phase I - Data Integrity Testing
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Test Configuration:
   Storage: file-based
   Concurrency Tests: enabled
   Persistence Tests: enabled
   Recovery Tests: enabled
   Sample Size: 50 tasks
   Corruption Scenarios: id_collision, state_corruption

⚙️  Phase 1: Setup (2.3s)
   ✓ Initialized file-based storage
   ✓ Created test directory: /tmp/todo-test-1735384200
   ✓ Generated 50 test tasks
   ✓ Calculated baseline checksums
   ✓ Defined integrity constraints

🧪 Phase 2: Execution (11.9s)

ID INTEGRITY (4 tests)
   ✓ ID_001: Sequential ID generation
   ✓ ID_002: ID persistence after deletion
   ✓ ID_003: Large-scale ID uniqueness (50 tasks)
   ✗ ID_004: ID collision during concurrent creates - FAILED
      └─ 2 tasks assigned ID 5 simultaneously

STATE CONSISTENCY (4 tests)
   ✓ STATE_001: State preservation during reads
   ✓ STATE_002: Atomic state updates
   ✓ STATE_003: State isolation between tasks
   ✓ STATE_004: Invalid state rejection

CONCURRENCY (4 tests)
   ✓ CONCUR_001: Simultaneous creates
   ✗ CONCUR_002: Concurrent read-update-read - FAILED
      └─ Stale data returned after update
   ✗ CONCUR_003: Concurrent updates to same task - FAILED
      └─ Lost update detected (completed status)
   ✓ CONCUR_004: Concurrent delete operations

PERSISTENCE (3 tests)
   ✓ PERSIST_001: Data survives storage reload
   ✗ PERSIST_002: Partial write protection - FAILED
      └─ Incomplete task found after simulated crash
   ✓ PERSIST_003: Large dataset persistence

CORRUPTION RECOVERY (4 tests)
   ✓ RECOVER_001: ID collision detection
   ✓ RECOVER_002: State corruption detection
   ✓ RECOVER_003: Orphaned data cleanup
   ✗ RECOVER_004: Duplicate entry removal - FAILED
      └─ Duplicates not automatically resolved

REFERENTIAL INTEGRITY (3 tests)
   ✓ REF_001: Task relationships maintained
   ✗ REF_002: Cascade operations - FAILED
      └─ Orphaned subtasks after parent deletion
   ✓ REF_003: Foreign key validation

📊 Phase 3: Analysis (1.0s)

INTEGRITY METRICS:
   Overall Score: 72.7% (16/22 passed)
   Data Fidelity: 98% (2 tasks lost)
   Violations Detected: 6

VIOLATION BREAKDOWN:
   Critical: 1 (ID collision)
   High: 3 (Persistence, Concurrency ×2)
   Medium: 2 (Recovery, Referential)
   Low: 0

❌ DATA INTEGRITY COMPROMISED - 6 violation(s) detected

🔧 Priority Fixes:
   1. [CRITICAL] ID_COLLISION_001 - Thread-safe ID generation
   2. [HIGH] PERSIST_002 - Atomic file writes
   3. [HIGH] CONCUR_003 - Optimistic concurrency control

📄 Full report: .claude/reports/test-task-data-integrity-2025-12-28-143500.json
📊 Violation details: .claude/reports/violations-2025-12-28-143500.json
```

## Failure Handling

### Failure Scenario 1: Storage Initialization Failure
**Condition**: Cannot initialize specified storage type
**Detection**: Exception during Step 1.1
**Response**:
```json
{
  "status": "ERROR",
  "error_type": "STORAGE_INIT_FAILED",
  "message": "Failed to initialize file-based storage",
  "storage_type": "file-based",
  "error_details": "PermissionError: Cannot write to /tmp/todo-test/",
  "resolution": "Check write permissions or use different storage type",
  "fallback_available": "in-memory",
  "exit_code": 1
}
```
**Recovery**: Offer to retry with in-memory storage, or abort

### Failure Scenario 2: Baseline Checksum Mismatch
**Condition**: Test data doesn't match expected baseline after operations
**Detection**: Checksum comparison in Step 3.4
**Response**:
```json
{
  "status": "WARNING",
  "warning_type": "CHECKSUM_MISMATCH",
  "message": "Data changed unexpectedly during testing",
  "expected_checksum": "a3f8b9c2d1e4...",
  "actual_checksum": "d8e2a1f9c3b4...",
  "affected_tasks": [5, 12, 23],
  "possible_causes": [
    "Test interference (tests not properly isolated)",
    "Background process modified storage",
    "Non-deterministic task generation"
  ],
  "impact": "Test results may be unreliable",
  "recommendation": "Review test isolation and retry"
}
```
**Recovery**: Flag results as potentially unreliable, suggest retry

### Failure Scenario 3: Concurrency Test Timeout
**Condition**: Concurrent operations deadlock or hang
**Detection**: 60-second timeout on concurrent test execution
**Response**:
```json
{
  "status": "TIMEOUT",
  "test_id": "CONCUR_002",
  "message": "Concurrent update test exceeded timeout",
  "timeout_seconds": 60,
  "threads_completed": 2,
  "threads_hanging": 3,
  "last_operation": "update_task(1, completed=True) from Thread C",
  "suspected_cause": "Deadlock in storage layer",
  "resolution": "Review locking mechanisms, investigate Thread C state",
  "data_impact": "Task 1 may be in inconsistent state"
}
```
**Recovery**: Kill hanging threads, mark test as failed, continue with non-concurrent tests

### Failure Scenario 4: Storage Corruption Unrecoverable
**Condition**: Storage corrupted beyond automatic recovery
**Detection**: Multiple recovery attempts fail in Step 2.5
**Response**:
```json
{
  "status": "CRITICAL",
  "error_type": "UNRECOVERABLE_CORRUPTION",
  "message": "Storage is corrupted and cannot be automatically repaired",
  "corruption_details": {
    "invalid_json": true,
    "missing_data": ["tasks 10-15"],
    "schema_violations": 8
  },
  "impact": "Cannot continue integrity testing",
  "manual_intervention_required": true,
  "suggested_actions": [
    "Backup corrupted storage for forensic analysis",
    "Restore from last known good state",
    "Review logs for corruption trigger event",
    "Run manual data recovery tools"
  ],
  "exit_code": 2
}
```
**Recovery**: Abort testing, preserve corrupted state for analysis, notify user

### Failure Scenario 5: Sample Size Too Large for Environment
**Condition**: Requested sample_size exceeds available memory/storage
**Detection**: Memory/disk allocation failure during test data generation
**Response**:
```json
{
  "status": "ERROR",
  "error_type": "RESOURCE_EXHAUSTED",
  "message": "Cannot generate requested sample size",
  "requested_sample_size": 10000,
  "maximum_feasible": 2500,
  "resource_limit": "Memory: 512MB available, 2GB required",
  "resolution": "Reduce sample_size parameter to <= 2500",
  "auto_adjust": false,
  "exit_code": 3
}
```
**Recovery**: Abort and ask user to reduce sample_size, or offer to auto-adjust with confirmation

### Failure Scenario 6: Test Isolation Violation
**Condition**: Tests interfere with each other's data
**Detection**: Post-test cleanup finds unexpected tasks
**Response**:
```json
{
  "status": "WARNING",
  "warning_type": "TEST_ISOLATION_VIOLATED",
  "message": "Tests are not properly isolated",
  "unexpected_tasks": [
    {"id": 999, "title": "Leftover from previous test"}
  ],
  "affected_tests": ["STATE_002", "PERSIST_001"],
  "impact": "Test results may be unreliable due to data pollution",
  "recommendation": "Review test cleanup procedures, ensure fresh state for each test",
  "continue_testing": true
}
```
**Recovery**: Log warning, continue testing but flag results as potentially compromised

---

## Usage Notes

- This skill is **deterministic** for single-threaded tests; concurrent tests may have timing-dependent outcomes
- All corruption scenarios are safe (use test storage, never production data)
- Can be run in CI/CD pipeline with JSON output for automated quality gates
- Combine with `validate-task-operations` for comprehensive quality assurance
- Recommended to run after storage layer changes or before major releases
- Test data is cleaned up automatically unless `--preserve-test-data` flag is used

## Agent Integration

This skill is owned by the **QA Agent** and can be invoked via:
```bash
/qa test-task-data-integrity --storage file-based --sample-size 50
```

Or programmatically:
```python
qa_agent.execute_skill(
    skill_id="qa.test-task-data-integrity",
    params={
        "storage_type": "file-based",
        "test_concurrency": True,
        "test_persistence": True,
        "test_recovery": True,
        "sample_size": 50,
        "corruption_scenarios": ["all"],
        "verbose_output": True
    }
)
```
