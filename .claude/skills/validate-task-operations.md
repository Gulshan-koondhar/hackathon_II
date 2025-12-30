# Skill: Validate Task Operations

## Metadata
- **Skill ID**: `qa.validate-task-operations`
- **Owner Agent**: QA Agent
- **Project**: Todo App (Phase I)
- **Category**: Quality Assurance - Functional Validation
- **Version**: 1.0.0
- **Last Updated**: 2025-12-28

## Purpose

Systematically validate that all CRUD (Create, Read, Update, Delete) operations on Todo tasks behave correctly according to the specifications defined in the `task-manager-agent` and `task-viewer` agents. This skill ensures data validation rules are enforced, error handling works as expected, and success responses conform to the standardized format.

## When to Use

Use this skill when:
- A new task management feature has been implemented or modified
- Before deploying changes to task CRUD operations
- After refactoring the task-manager-agent or task-viewer logic
- When validating that validation rules (title length, ID format, etc.) are correctly enforced
- As part of the pre-deployment quality gate in the CI/CD pipeline
- When investigating bug reports related to task operations
- After merging pull requests that touch task management code

Do NOT use this skill for:
- Performance testing (use dedicated performance testing skills)
- User interface validation (use UI testing skills)
- Load testing or stress testing scenarios

## Inputs

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `test_scope` | string | No | `"all"` | Scope of validation: `"all"`, `"create"`, `"read"`, `"update"`, `"delete"` |
| `storage_type` | string | No | `"in-memory"` | Storage implementation to test: `"in-memory"`, `"file-based"`, `"database"` |
| `include_edge_cases` | boolean | No | `true` | Whether to include boundary and edge case tests |
| `verbose_output` | boolean | No | `false` | Enable detailed test execution logs |
| `fail_fast` | boolean | No | `false` | Stop testing on first failure |

### Input Example
```json
{
  "test_scope": "create",
  "storage_type": "in-memory",
  "include_edge_cases": true,
  "verbose_output": true,
  "fail_fast": false
}
```

## Step-by-Step Process

### Phase 1: Pre-Validation Setup (2-3 minutes)

**Step 1.1: Environment Initialization**
- Verify task-manager-agent.md exists at `.claude/agents/task-manager-agent.md`
- Verify task-viewer.md exists at `.claude/agents/task-viewer.md`
- Parse validation rules from both agent specifications:
  - Title constraints: non-empty, max 200 characters
  - Description constraints: optional, max 1000 characters
  - ID constraints: positive integers only
  - Completion status: boolean values only
- Initialize test storage with clean state (empty task list)
- Set up test data fixtures based on project requirements

**Step 1.2: Test Case Preparation**
- Generate test cases based on `test_scope` parameter:
  - **Create operations**: valid tasks, empty titles, oversized titles, oversized descriptions
  - **Read operations**: existing IDs, non-existent IDs, invalid ID formats
  - **Update operations**: partial updates, full updates, no-field updates, invalid fields
  - **Delete operations**: existing tasks, non-existent tasks, invalid IDs
- If `include_edge_cases` is true, add boundary tests:
  - Title exactly 200 characters
  - Title 201 characters (should fail)
  - Description exactly 1000 characters
  - Description 1001 characters (should fail)
  - ID = 0 (should fail)
  - ID = -1 (should fail)
  - Whitespace-only titles (should fail)

**Step 1.3: Validation Criteria Setup**
- Define expected response structure for all operations:
  ```python
  {
    "success": bool,
    "message": str,
    "data": any | None
  }
  ```
- Define success/failure criteria for each operation type
- Prepare assertion checks for response validation

### Phase 2: Execute Validation Tests (5-10 minutes)

**Step 2.1: Create Operation Validation**
```
Test: Valid task creation
Input: {"title": "Buy groceries", "description": "Milk, eggs, bread"}
Expected: success=true, data contains task with id=1, completed=false
Validation: Verify task object structure, ID assignment, default completed status

Test: Empty title rejection
Input: {"title": "", "description": "Test"}
Expected: success=false, message="Task title cannot be empty", data=None
Validation: Verify error message accuracy

Test: Title length boundary (200 chars)
Input: {"title": "A" * 200, "description": "Valid"}
Expected: success=true, task created
Validation: Verify 200-character title is accepted

Test: Title length overflow (201 chars)
Input: {"title": "A" * 201, "description": "Invalid"}
Expected: success=false, message="Task title exceeds 200 character limit"
Validation: Verify rejection and error message

Test: Description length boundary (1000 chars)
Input: {"title": "Test", "description": "B" * 1000}
Expected: success=true, task created
Validation: Verify 1000-character description is accepted

Test: Description length overflow (1001 chars)
Input: {"title": "Test", "description": "B" * 1001}
Expected: success=false, message="Task description exceeds 1000 character limit"
Validation: Verify rejection and error message

Test: Whitespace-only title
Input: {"title": "   ", "description": "Test"}
Expected: success=false, message="Task title cannot be empty"
Validation: Verify whitespace trimming and validation
```

**Step 2.2: Read Operation Validation**
```
Setup: Create tasks with IDs 1, 2, 3

Test: Retrieve existing task
Input: task_id=2
Expected: success=true, data contains full task object for ID 2
Validation: Verify all fields present (id, title, description, completed)

Test: Non-existent task retrieval
Input: task_id=999
Expected: success=false, message="Task with ID 999 does not exist", data=None
Validation: Verify error message includes specific ID

Test: Invalid ID format (negative)
Input: task_id=-5
Expected: success=false, message="Task ID must be a positive integer"
Validation: Verify ID validation before lookup

Test: Invalid ID format (zero)
Input: task_id=0
Expected: success=false, message="Task ID must be a positive integer"
Validation: Verify zero is rejected as invalid
```

**Step 2.3: Update Operation Validation**
```
Setup: Create task with ID 1: {"title": "Original", "description": "Desc", "completed": false}

Test: Partial update (title only)
Input: update_task(1, title="Updated Title")
Expected: success=true, data shows title="Updated Title", description and completed unchanged
Validation: Verify partial update preserves other fields

Test: Partial update (completed status only)
Input: update_task(1, completed=true)
Expected: success=true, data shows completed=true, title and description unchanged
Validation: Verify status toggle works correctly

Test: Full update (all fields)
Input: update_task(1, title="New", description="New Desc", completed=true)
Expected: success=true, data reflects all changes
Validation: Verify all fields updated correctly

Test: No fields provided
Input: update_task(1)
Expected: success=false, message="No fields specified for update"
Validation: Verify empty update is rejected

Test: Update non-existent task
Input: update_task(999, title="Test")
Expected: success=false, message="Task with ID 999 does not exist"
Validation: Verify existence check happens before update

Test: Update with invalid title
Input: update_task(1, title="")
Expected: success=false, message="Task title cannot be empty"
Validation: Verify validation applies to updates

Test: Update with oversized title
Input: update_task(1, title="A" * 201)
Expected: success=false, message="Task title exceeds 200 character limit"
Validation: Verify length validation on updates

Test: Update with invalid completed type
Input: update_task(1, completed="yes")
Expected: success=false, message="Completion status must be true or false"
Validation: Verify boolean type enforcement
```

**Step 2.4: Delete Operation Validation**
```
Setup: Create tasks with IDs 1, 2, 3

Test: Delete existing task
Input: delete_task(2)
Expected: success=true, message confirms deletion, data contains deleted task info
Validation: Verify task no longer retrievable after deletion

Test: Delete non-existent task
Input: delete_task(999)
Expected: success=false, message="Task with ID 999 does not exist"
Validation: Verify error message for missing task

Test: Delete with invalid ID format
Input: delete_task(-1)
Expected: success=false, message="Task ID must be a positive integer"
Validation: Verify ID validation before deletion

Test: Delete already deleted task
Input: delete_task(2) [second time]
Expected: success=false, message="Task with ID 2 does not exist"
Validation: Verify idempotency and proper error handling
```

**Step 2.5: Response Format Validation**
- For every test, verify response structure matches:
  ```python
  {
    "success": bool,
    "message": str,
    "data": any | None
  }
  ```
- Check that `success` is always boolean (never missing or string)
- Check that `message` is always non-empty string
- Check that `data` is None on failures, populated on successes
- Verify no extra keys exist in response dictionary

### Phase 3: Results Analysis and Reporting (2-3 minutes)

**Step 3.1: Generate Test Report**
- Count total tests executed
- Count passed tests (actual matches expected)
- Count failed tests (actual differs from expected)
- Calculate pass rate percentage
- Group failures by category (validation, response format, logic errors)

**Step 3.2: Create Detailed Failure Report**
For each failed test:
```
Test ID: CREATE_003
Operation: Create task with oversized title
Input: {"title": "A" * 201, "description": "Test"}
Expected: {"success": false, "message": "Task title exceeds 200 character limit", "data": None}
Actual: {"success": true, "message": "Task created", "data": {...}}
Failure Type: Validation Rule Not Enforced
Severity: HIGH
Affected Agent: task-manager-agent.md:45-49
```

**Step 3.3: Generate Recommendations**
Based on failures, provide:
- Specific code locations to investigate (file:line references)
- Suggested fixes with code snippets
- Related test cases that might also be affected
- Impact assessment (critical, high, medium, low)
- Remediation priority order

## Output

### Success Output Format
```json
{
  "status": "PASS",
  "summary": {
    "total_tests": 28,
    "passed": 28,
    "failed": 0,
    "skipped": 0,
    "pass_rate": "100%",
    "execution_time_seconds": 8.3
  },
  "coverage": {
    "create_operations": "100%",
    "read_operations": "100%",
    "update_operations": "100%",
    "delete_operations": "100%",
    "edge_cases": "100%"
  },
  "validation_checks": {
    "response_format_compliance": "PASS",
    "error_message_accuracy": "PASS",
    "validation_rules_enforced": "PASS",
    "data_integrity_maintained": "PASS"
  },
  "recommendations": [
    "All validation tests passed. System is ready for deployment.",
    "Consider adding performance benchmarks for operations with large task lists.",
    "Document the validated behavior in integration test suite."
  ]
}
```

### Failure Output Format
```json
{
  "status": "FAIL",
  "summary": {
    "total_tests": 28,
    "passed": 24,
    "failed": 4,
    "skipped": 0,
    "pass_rate": "85.7%",
    "execution_time_seconds": 7.8
  },
  "coverage": {
    "create_operations": "75%",
    "read_operations": "100%",
    "update_operations": "100%",
    "delete_operations": "100%",
    "edge_cases": "66.7%"
  },
  "failures": [
    {
      "test_id": "CREATE_004",
      "operation": "Create task with oversized title",
      "input": {"title": "A repeated 201 times", "description": "Test"},
      "expected": {"success": false, "message": "Task title exceeds 200 character limit", "data": null},
      "actual": {"success": true, "message": "Task created successfully", "data": {"id": 1, "title": "...", "completed": false}},
      "failure_type": "Validation Rule Not Enforced",
      "severity": "HIGH",
      "affected_file": ".claude/agents/task-manager-agent.md:38-42",
      "recommendation": "Add title length validation in add_task method before creating task object"
    },
    {
      "test_id": "CREATE_007",
      "operation": "Create task with whitespace-only title",
      "input": {"title": "   ", "description": "Test"},
      "expected": {"success": false, "message": "Task title cannot be empty", "data": null},
      "actual": {"success": true, "message": "Task created successfully", "data": {"id": 2, "title": "   ", "completed": false}},
      "failure_type": "Whitespace Trimming Not Applied",
      "severity": "MEDIUM",
      "affected_file": ".claude/agents/task-manager-agent.md:37",
      "recommendation": "Apply .strip() to title before validation check"
    }
  ],
  "validation_checks": {
    "response_format_compliance": "PASS",
    "error_message_accuracy": "PASS",
    "validation_rules_enforced": "FAIL",
    "data_integrity_maintained": "PASS"
  },
  "recommendations": [
    "CRITICAL: Fix title length validation in task-manager-agent (CREATE_004)",
    "HIGH: Implement whitespace trimming for title input (CREATE_007)",
    "Re-run validation after fixes to confirm resolution",
    "Consider adding these cases to automated test suite"
  ]
}
```

### Console Output (when verbose_output=true)
```
🔍 Todo App Phase I - Task Operations Validation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Test Configuration:
   Scope: all operations
   Storage: in-memory
   Edge Cases: enabled
   Fail Fast: disabled

⚙️  Phase 1: Setup
   ✓ Loaded task-manager-agent specification
   ✓ Loaded task-viewer specification
   ✓ Initialized test storage
   ✓ Generated 28 test cases

🧪 Phase 2: Execution

CREATE OPERATIONS (7 tests)
   ✓ CREATE_001: Valid task creation
   ✓ CREATE_002: Empty title rejection
   ✓ CREATE_003: Title length boundary (200 chars)
   ✗ CREATE_004: Title length overflow (201 chars) - FAILED
   ✓ CREATE_005: Description length boundary (1000 chars)
   ✓ CREATE_006: Description length overflow (1001 chars)
   ✗ CREATE_007: Whitespace-only title - FAILED

READ OPERATIONS (4 tests)
   ✓ READ_001: Retrieve existing task
   ✓ READ_002: Non-existent task retrieval
   ✓ READ_003: Invalid ID format (negative)
   ✓ READ_004: Invalid ID format (zero)

UPDATE OPERATIONS (9 tests)
   ✓ UPDATE_001: Partial update (title only)
   ✓ UPDATE_002: Partial update (completed only)
   ✓ UPDATE_003: Full update (all fields)
   ✓ UPDATE_004: No fields provided
   ✓ UPDATE_005: Update non-existent task
   ✓ UPDATE_006: Update with invalid title
   ✓ UPDATE_007: Update with oversized title
   ✓ UPDATE_008: Update with invalid completed type
   ✓ UPDATE_009: Idempotent update (same data)

DELETE OPERATIONS (4 tests)
   ✓ DELETE_001: Delete existing task
   ✓ DELETE_002: Delete non-existent task
   ✓ DELETE_003: Delete with invalid ID
   ✓ DELETE_004: Delete already deleted task

RESPONSE FORMAT (4 tests)
   ✓ FORMAT_001: Response structure compliance
   ✓ FORMAT_002: Success boolean type
   ✓ FORMAT_003: Message string presence
   ✓ FORMAT_004: Data field consistency

📊 Phase 3: Results
   Total: 28 | Passed: 24 | Failed: 4 | Pass Rate: 85.7%

❌ VALIDATION FAILED - 4 test(s) failed

🔧 Top Priority Fixes:
   1. [HIGH] task-manager-agent.md:38-42 - Add title length validation
   2. [MEDIUM] task-manager-agent.md:37 - Implement whitespace trimming

📄 Full report: .claude/reports/validate-task-operations-2025-12-28-143022.json
```

## Failure Handling

### Failure Scenario 1: Agent Specification Files Missing
**Condition**: `task-manager-agent.md` or `task-viewer.md` not found
**Detection**: File existence check in Step 1.1 fails
**Response**:
```json
{
  "status": "ERROR",
  "error_type": "MISSING_SPECIFICATIONS",
  "message": "Cannot validate operations without agent specifications",
  "missing_files": [
    ".claude/agents/task-manager-agent.md"
  ],
  "resolution": "Ensure agent specification files exist before running validation",
  "exit_code": 1
}
```
**Recovery**: Abort validation, instruct user to create agent files first

### Failure Scenario 2: Invalid Test Scope Parameter
**Condition**: `test_scope` value not in `["all", "create", "read", "update", "delete"]`
**Detection**: Input validation in parameter parsing
**Response**:
```json
{
  "status": "ERROR",
  "error_type": "INVALID_INPUT",
  "message": "Invalid test_scope parameter",
  "provided_value": "modify",
  "valid_values": ["all", "create", "read", "update", "delete"],
  "resolution": "Use one of the valid test_scope values",
  "exit_code": 2
}
```
**Recovery**: Abort validation, prompt user for valid input

### Failure Scenario 3: Storage Initialization Failure
**Condition**: Cannot initialize test storage (memory allocation, file permissions, etc.)
**Detection**: Exception during storage setup in Step 1.1
**Response**:
```json
{
  "status": "ERROR",
  "error_type": "STORAGE_INITIALIZATION_FAILED",
  "message": "Failed to initialize test storage",
  "storage_type": "in-memory",
  "error_details": "MemoryError: Cannot allocate memory for task list",
  "resolution": "Check system resources and retry, or use alternative storage type",
  "exit_code": 3
}
```
**Recovery**: Abort validation, suggest troubleshooting steps

### Failure Scenario 4: Test Execution Timeout
**Condition**: Individual test exceeds 30-second timeout
**Detection**: Timeout wrapper around each test execution
**Response**:
```json
{
  "status": "PARTIAL",
  "summary": {
    "total_tests": 28,
    "passed": 12,
    "failed": 0,
    "skipped": 16,
    "timed_out": 1,
    "pass_rate": "N/A"
  },
  "timeout_details": {
    "test_id": "UPDATE_003",
    "timeout_seconds": 30,
    "reason": "Test execution exceeded maximum allowed time",
    "last_operation": "update_task(1, title='...', description='...', completed=true)"
  },
  "recommendations": [
    "Investigate UPDATE_003 for infinite loops or blocking operations",
    "Check if task-manager-agent has performance issues with updates",
    "Re-run validation with increased timeout if necessary"
  ]
}
```
**Recovery**: Skip timed-out test, continue with remaining tests unless `fail_fast=true`

### Failure Scenario 5: Assertion Framework Unavailable
**Condition**: Required testing utilities or assertion libraries not available
**Detection**: Import checks during initialization
**Response**:
```json
{
  "status": "ERROR",
  "error_type": "MISSING_DEPENDENCIES",
  "message": "Required testing framework components are unavailable",
  "missing_components": ["assertion_helpers", "test_fixtures"],
  "resolution": "Install required dependencies or use built-in assertion methods",
  "fallback_available": true,
  "exit_code": 4
}
```
**Recovery**: Fall back to basic assertion methods (manual comparisons), log warning, continue

### Failure Scenario 6: Fail-Fast Mode Triggered
**Condition**: `fail_fast=true` and first test failure occurs
**Detection**: Test fails and fail_fast flag is set
**Response**:
```json
{
  "status": "ABORTED",
  "summary": {
    "total_tests": 28,
    "passed": 2,
    "failed": 1,
    "skipped": 25,
    "pass_rate": "N/A"
  },
  "first_failure": {
    "test_id": "CREATE_004",
    "operation": "Create task with oversized title",
    "failure_type": "Validation Rule Not Enforced",
    "severity": "HIGH"
  },
  "message": "Validation aborted due to fail-fast mode",
  "recommendations": [
    "Fix CREATE_004 failure first",
    "Re-run with fail_fast=false to discover all issues"
  ]
}
```
**Recovery**: Stop execution immediately, report partial results

---

## Usage Notes

- This skill is **deterministic**: Given the same inputs and agent specifications, it will always produce the same test results
- Test execution order is fixed to ensure reproducibility
- All test data is generated programmatically, no external data files required
- Skill can be run in CI/CD pipeline with JSON output for automated quality gates
- Recommended to run after any changes to `.claude/agents/task-manager-agent.md` or `.claude/agents/task-viewer.md`
- Can be combined with `test-task-data-integrity.md` skill for comprehensive validation

## Agent Integration

This skill is owned by the **QA Agent** and can be invoked via:
```bash
/qa validate-task-operations --scope all --verbose true
```

Or programmatically:
```python
qa_agent.execute_skill(
    skill_id="qa.validate-task-operations",
    params={
        "test_scope": "all",
        "storage_type": "in-memory",
        "include_edge_cases": True,
        "verbose_output": True,
        "fail_fast": False
    }
)
```
