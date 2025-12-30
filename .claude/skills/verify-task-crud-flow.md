# Skill: Verify Task CRUD Flow

## Metadata
- **Skill ID**: `qa.verify-task-crud-flow`
- **Owner Agent**: QA Agent
- **Project**: Todo App (Phase I)
- **Category**: Quality Assurance - End-to-End Integration Testing
- **Version**: 1.0.0
- **Last Updated**: 2025-12-28

## Purpose

Execute comprehensive end-to-end workflow testing of the Todo App Phase I by simulating realistic user scenarios that combine Create, Read, Update, and Delete operations in sequence. This skill validates that the entire task lifecycle functions correctly when operations are chained together, ensuring the task-manager-agent and task-viewer agent work cohesively as an integrated system.

## When to Use

Use this skill when:
- Validating complete feature implementation before user acceptance testing
- After integrating task-manager-agent and task-viewer components
- Before major releases or milestone deployments
- When testing user stories or acceptance criteria
- After refactoring that affects multiple CRUD operations
- As part of regression testing after bug fixes
- When validating that specifications in spec.md are fully met
- As a quality gate before marking tasks as complete in tasks.md

Do NOT use this skill for:
- Unit testing individual operations (use `validate-task-operations` instead)
- Data consistency testing in isolation (use `test-task-data-integrity` instead)
- Performance or load testing under high concurrency
- UI/UX testing or frontend validation

## Inputs

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `workflow_scenarios` | array | No | `["all"]` | Scenarios to test: `"basic_crud"`, `"user_journey"`, `"edge_cases"`, `"error_recovery"`, `"all"` |
| `storage_type` | string | No | `"in-memory"` | Storage implementation: `"in-memory"`, `"file-based"`, `"database"` |
| `verify_intermediate_states` | boolean | No | `true` | Verify state after each step in workflow |
| `simulate_delays` | boolean | No | `false` | Add realistic delays between operations (for timing-sensitive tests) |
| `parallel_workflows` | boolean | No | `false` | Test multiple user workflows running simultaneously |
| `verbose_output` | boolean | No | `false` | Enable detailed step-by-step logs |
| `stop_on_first_failure` | boolean | No | `false` | Halt workflow testing on first failed scenario |

### Input Example
```json
{
  "workflow_scenarios": ["basic_crud", "user_journey"],
  "storage_type": "in-memory",
  "verify_intermediate_states": true,
  "simulate_delays": false,
  "parallel_workflows": false,
  "verbose_output": true,
  "stop_on_first_failure": false
}
```

## Step-by-Step Process

### Phase 1: Scenario Preparation (2-3 minutes)

**Step 1.1: Load Agent Specifications**
- Read `.claude/agents/task-manager-agent.md` for CRUD operation contracts
- Read `.claude/agents/task-viewer.md` for query operation contracts
- Extract expected behaviors:
  - Success response formats
  - Error response formats
  - State transition rules
  - Data validation rules
- Build operation call signatures and expected outcomes

**Step 1.2: Initialize Test Environment**
- Set up storage based on `storage_type`
- Verify storage is clean (no pre-existing tasks)
- Initialize test context:
  ```python
  test_context = {
    "storage": storage_instance,
    "task_manager": TaskManagerAgent(storage_instance),
    "task_viewer": TaskViewerAgent(storage_instance),
    "created_task_ids": [],
    "scenario_results": []
  }
  ```
- Prepare test data fixtures for workflows

**Step 1.3: Define Workflow Scenarios**

**Scenario 1: Basic CRUD Workflow**
```
User Goal: Create a task, view it, update it, then delete it
Steps:
  1. Create task "Buy milk"
  2. Read task by ID
  3. Update task to mark completed
  4. Read task again to verify update
  5. Delete task
  6. Verify task no longer exists
Expected Outcome: All operations succeed, data consistent throughout
```

**Scenario 2: Multi-Task Management Workflow**
```
User Goal: Manage multiple tasks with filtering
Steps:
  1. Create 5 tasks (3 incomplete, 2 complete)
  2. List all tasks, verify count = 5
  3. Filter by completed=false, verify count = 3
  4. Filter by completed=true, verify count = 2
  5. Update one incomplete task to completed
  6. Re-filter by completed=false, verify count = 2
  7. Delete all completed tasks (now 3 total)
  8. List all tasks, verify count = 2 (only incomplete remain)
Expected Outcome: Filters accurate, operations don't interfere
```

**Scenario 3: Partial Update Workflow**
```
User Goal: Update individual task fields independently
Steps:
  1. Create task {"title": "Original", "description": "Desc", "completed": false}
  2. Update title to "Updated Title"
  3. Verify description and completed unchanged
  4. Update completed to true
  5. Verify title and description still unchanged
  6. Update description to "New Description"
  7. Verify title and completed still reflect previous updates
Expected Outcome: Partial updates preserve other fields
```

**Scenario 4: Error Recovery Workflow**
```
User Goal: Recover from errors without corrupting data
Steps:
  1. Create valid task (id=1)
  2. Attempt to create task with empty title → should fail
  3. Verify task 1 still exists and unchanged
  4. Attempt to update non-existent task 999 → should fail
  5. Verify task 1 still exists and unchanged
  6. Attempt to delete non-existent task 999 → should fail
  7. Verify task 1 still exists and unchanged
  8. Successfully delete task 1
  9. Verify task 1 no longer exists
Expected Outcome: Failed operations don't corrupt valid data
```

**Scenario 5: Task Lifecycle Journey**
```
User Goal: Complete real-world task management flow
Steps:
  1. Create task "Submit project report" (incomplete)
  2. Create task "Review team feedback" (incomplete)
  3. Create task "Update presentation slides" (incomplete)
  4. List all tasks, verify 3 pending
  5. Mark "Review team feedback" as complete
  6. List incomplete tasks, verify 2 pending
  7. Update "Submit project report" title to "Submit final project report"
  8. Mark "Submit final project report" as complete
  9. List incomplete tasks, verify 1 pending ("Update presentation slides")
  10. Complete "Update presentation slides"
  11. List all tasks, verify all 3 are complete
  12. Archive (delete) all completed tasks
  13. List all tasks, verify list is empty
Expected Outcome: Realistic workflow completes successfully
```

**Scenario 6: Edge Cases Workflow**
```
User Goal: Handle boundary conditions gracefully
Steps:
  1. Create task with title exactly 200 characters → should succeed
  2. Create task with description exactly 1000 characters → should succeed
  3. Attempt to create task with title 201 characters → should fail
  4. Attempt to create task with description 1001 characters → should fail
  5. Create task with whitespace in title "  Test  " → should trim to "Test"
  6. Create task with special characters in title "Task #1: @urgent!" → should succeed
  7. Update task to have empty description → should succeed (optional field)
  8. Attempt to update task to have empty title → should fail (required field)
Expected Outcome: Boundaries respected, no crashes or data corruption
```

**Scenario 7: Concurrent User Workflow** (if parallel_workflows=true)
```
User Goal: Multiple users managing tasks simultaneously
Steps:
  User A:
    1. Create task "User A Task 1"
    2. Create task "User A Task 2"
    3. Mark "User A Task 1" complete
  User B (simultaneously):
    1. Create task "User B Task 1"
    2. List all tasks (should see both users' tasks)
    3. Update "User B Task 1" description

  Final Verification:
    - Total tasks = 3
    - User A has 2 tasks (1 complete, 1 incomplete)
    - User B has 1 task (incomplete)
    - No data cross-contamination between users
Expected Outcome: Concurrent operations don't interfere
```

### Phase 2: Workflow Execution (10-20 minutes)

**Step 2.1: Execute Each Scenario**
For each scenario in `workflow_scenarios`:

1. **Pre-Scenario Setup**
   - Clear storage (fresh state for each scenario)
   - Initialize scenario-specific test data if needed
   - Record start time and initial storage state

2. **Step-by-Step Execution**
   - Execute each step in the scenario sequentially
   - For each step:
     ```python
     step_result = {
       "step_number": 1,
       "operation": "create_task",
       "input": {"title": "Buy milk", "description": ""},
       "expected_output": {"success": true, "message": "...", "data": {...}},
       "actual_output": None,
       "status": "pending",
       "execution_time_ms": 0
     }
     ```
   - Call appropriate agent method (task_manager or task_viewer)
   - Capture actual output
   - Compare actual vs. expected output

3. **Intermediate State Verification** (if verify_intermediate_states=true)
   After each step:
   - Query current storage state
   - Verify task count matches expected
   - Verify all tasks have correct data
   - Verify no unexpected tasks exist
   - Check data consistency (IDs unique, no corruption)

4. **Step Outcome Assessment**
   ```python
   if actual_output == expected_output:
       step_result["status"] = "PASS"
   else:
       step_result["status"] = "FAIL"
       step_result["failure_reason"] = calculate_diff(expected, actual)
       if stop_on_first_failure:
           abort_scenario_execution()
   ```

5. **Simulated Delays** (if simulate_delays=true)
   - Add 100-500ms delay between operations
   - Simulates realistic user interaction timing
   - Useful for detecting race conditions or timing bugs

6. **Post-Scenario Validation**
   - Verify final storage state matches scenario expectation
   - Check for data leaks or orphaned tasks
   - Confirm all operations left storage in consistent state

**Step 2.2: Parallel Workflow Testing** (if parallel_workflows=true)
- Spawn multiple workflow executions in separate threads/processes
- Each workflow operates on shared storage
- Verify:
  - No operation interference (User A's update doesn't affect User B's task)
  - Correct task counts (all tasks from all users present)
  - No data corruption or loss
  - Proper isolation between users if multi-tenancy exists

**Step 2.3: Error Accumulation and Logging**
For each failed step:
```python
failure_record = {
  "scenario": "Basic CRUD Workflow",
  "step": 3,
  "operation": "update_task",
  "failure_type": "Unexpected Output",
  "expected": {"success": true, "data": {"completed": true}},
  "actual": {"success": true, "data": {"completed": false}},
  "diff": "Field 'completed' expected true, got false",
  "impact": "Task state not updated correctly",
  "affected_agents": ["task-manager-agent"],
  "timestamp": "2025-12-28T14:35:22Z"
}
```

### Phase 3: Results Analysis and Reporting (3-5 minutes)

**Step 3.1: Aggregate Scenario Results**
```python
summary = {
  "total_scenarios": 7,
  "passed_scenarios": 5,
  "failed_scenarios": 2,
  "total_steps": 48,
  "passed_steps": 43,
  "failed_steps": 5,
  "pass_rate_scenarios": "71.4%",
  "pass_rate_steps": "89.6%"
}
```

**Step 3.2: Categorize Failures**
Group failures by:
- **Operation Type**: Create, Read, Update, Delete
- **Agent**: task-manager-agent, task-viewer
- **Failure Type**: Validation error, unexpected output, exception, timeout
- **Severity**: Blocker (scenario cannot complete), Critical (wrong data), Major (wrong message), Minor (formatting issue)

**Step 3.3: Impact Analysis**
For each failed scenario:
```
Scenario: Multi-Task Management Workflow
Status: FAILED
Failed Steps: Step 6 (Re-filter by completed status)
Root Cause: task-viewer filter logic does not update after task state change
Impact: Users cannot see accurate filtered lists after updating tasks
User Impact: HIGH - Core functionality broken
Affected User Stories: "As a user, I want to filter my tasks by completion status"
Blocker for Release: YES
```

**Step 3.4: Generate Actionable Recommendations**
```
Recommendation 1:
  Priority: CRITICAL
  Issue: Update operations not properly persisting completed status
  Affected File: .claude/agents/task-manager-agent.md:55-61
  Suggested Fix: Verify update_task method calls storage.save() after modification
  Verification Test: Re-run Scenario 2 after fix

Recommendation 2:
  Priority: HIGH
  Issue: Filter results stale after updates
  Affected File: .claude/agents/task-viewer.md:32-38
  Suggested Fix: Ensure filter queries read from current storage state, not cached
  Verification Test: Re-run Scenario 2 and Scenario 5 after fix
```

**Step 3.5: Traceability Matrix**
Map failed scenarios to:
- Specification requirements (from spec.md if exists)
- Task IDs (from tasks.md if exists)
- User stories or acceptance criteria
- Agents and methods involved

```
Failed Scenario: Basic CRUD Workflow (Step 3)
├─ Spec Requirement: REQ-002 "Users can mark tasks as complete"
├─ Task ID: TASK-015 "Implement task update functionality"
├─ User Story: US-003 "As a user, I want to mark tasks complete"
├─ Affected Agent: task-manager-agent.update_task()
└─ Root Cause: completed field not persisted to storage
```

## Output

### Success Output Format
```json
{
  "status": "PASS",
  "summary": {
    "total_scenarios": 7,
    "passed_scenarios": 7,
    "failed_scenarios": 0,
    "total_steps": 52,
    "passed_steps": 52,
    "failed_steps": 0,
    "pass_rate_scenarios": "100%",
    "pass_rate_steps": "100%",
    "execution_time_seconds": 18.4
  },
  "scenarios": [
    {
      "name": "Basic CRUD Workflow",
      "status": "PASS",
      "steps": 6,
      "passed": 6,
      "failed": 0,
      "execution_time_ms": 2100
    },
    {
      "name": "Multi-Task Management Workflow",
      "status": "PASS",
      "steps": 8,
      "passed": 8,
      "failed": 0,
      "execution_time_ms": 3200
    },
    {
      "name": "Partial Update Workflow",
      "status": "PASS",
      "steps": 7,
      "passed": 7,
      "failed": 0,
      "execution_time_ms": 2400
    },
    {
      "name": "Error Recovery Workflow",
      "status": "PASS",
      "steps": 9,
      "passed": 9,
      "failed": 0,
      "execution_time_ms": 2800
    },
    {
      "name": "Task Lifecycle Journey",
      "status": "PASS",
      "steps": 13,
      "passed": 13,
      "failed": 0,
      "execution_time_ms": 4600
    },
    {
      "name": "Edge Cases Workflow",
      "status": "PASS",
      "steps": 8,
      "passed": 8,
      "failed": 0,
      "execution_time_ms": 2700
    },
    {
      "name": "Concurrent User Workflow",
      "status": "PASS",
      "steps": 7,
      "passed": 7,
      "failed": 0,
      "execution_time_ms": 3100
    }
  ],
  "integration_validation": {
    "task_manager_task_viewer_integration": "PASS",
    "storage_consistency": "PASS",
    "state_transitions": "PASS",
    "error_handling": "PASS"
  },
  "recommendations": [
    "All workflow scenarios passed successfully",
    "System ready for user acceptance testing",
    "Consider adding these scenarios to automated regression suite",
    "Document workflows as example usage in user guide"
  ]
}
```

### Failure Output Format
```json
{
  "status": "FAIL",
  "summary": {
    "total_scenarios": 7,
    "passed_scenarios": 5,
    "failed_scenarios": 2,
    "total_steps": 52,
    "passed_steps": 46,
    "failed_steps": 6,
    "pass_rate_scenarios": "71.4%",
    "pass_rate_steps": "88.5%",
    "execution_time_seconds": 16.7
  },
  "scenarios": [
    {
      "name": "Basic CRUD Workflow",
      "status": "PASS",
      "steps": 6,
      "passed": 6,
      "failed": 0,
      "execution_time_ms": 2100
    },
    {
      "name": "Multi-Task Management Workflow",
      "status": "FAIL",
      "steps": 8,
      "passed": 6,
      "failed": 2,
      "execution_time_ms": 3000,
      "failures": [
        {
          "step": 6,
          "operation": "filter_tasks(completed=false)",
          "expected": {"success": true, "data": [{"id": 1}, {"id": 4}]},
          "actual": {"success": true, "data": [{"id": 1}, {"id": 3}, {"id": 4}]},
          "issue": "Filter returned incorrect count (3 instead of 2) after update",
          "severity": "CRITICAL"
        },
        {
          "step": 8,
          "operation": "list_all_tasks()",
          "expected": {"success": true, "data": "2 tasks"},
          "actual": {"success": true, "data": "3 tasks"},
          "issue": "Task count incorrect after deletions",
          "severity": "CRITICAL"
        }
      ]
    },
    {
      "name": "Partial Update Workflow",
      "status": "FAIL",
      "steps": 7,
      "passed": 4,
      "failed": 3,
      "execution_time_ms": 2200,
      "failures": [
        {
          "step": 3,
          "operation": "read_task(1)",
          "expected": {"data": {"title": "Updated Title", "description": "Desc", "completed": false}},
          "actual": {"data": {"title": "Updated Title", "description": "", "completed": false}},
          "issue": "Description field was cleared during title update (should be preserved)",
          "severity": "CRITICAL"
        }
      ]
    }
  ],
  "integration_validation": {
    "task_manager_task_viewer_integration": "FAIL",
    "storage_consistency": "FAIL",
    "state_transitions": "PASS",
    "error_handling": "PASS"
  },
  "failure_analysis": {
    "critical_issues": 2,
    "high_issues": 1,
    "medium_issues": 3,
    "low_issues": 0,
    "blockers_for_release": 2
  },
  "root_causes": [
    {
      "issue": "Filter results not updating after task state change",
      "affected_scenarios": ["Multi-Task Management Workflow"],
      "affected_agent": "task-viewer",
      "affected_file": ".claude/agents/task-viewer.md:32-38",
      "root_cause": "Filter method caches results or doesn't reload storage",
      "fix_priority": "CRITICAL",
      "estimated_effort": "MEDIUM"
    },
    {
      "issue": "Partial updates clearing other fields",
      "affected_scenarios": ["Partial Update Workflow"],
      "affected_agent": "task-manager-agent",
      "affected_file": ".claude/agents/task-manager-agent.md:55-61",
      "root_cause": "update_task replaces entire object instead of merging fields",
      "fix_priority": "CRITICAL",
      "estimated_effort": "LOW"
    }
  ],
  "recommendations": [
    "CRITICAL: Fix partial update logic to preserve unmodified fields",
    "CRITICAL: Fix filter refresh after task updates",
    "HIGH: Add integration test for filter accuracy after updates",
    "Re-run verify-task-crud-flow after fixes to confirm resolution",
    "Consider code review of task-manager-agent.update_task method"
  ],
  "traceability": [
    {
      "failed_scenario": "Multi-Task Management Workflow",
      "spec_requirement": "REQ-004: Filter tasks by completion status",
      "task_id": "TASK-020",
      "user_story": "US-005: As a user, I want to view only incomplete tasks",
      "blocked": true
    },
    {
      "failed_scenario": "Partial Update Workflow",
      "spec_requirement": "REQ-002: Update task fields independently",
      "task_id": "TASK-015",
      "user_story": "US-003: As a user, I can update task details",
      "blocked": true
    }
  ]
}
```

### Console Output (when verbose_output=true)
```
🔄 Todo App Phase I - CRUD Flow Verification
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Test Configuration:
   Scenarios: basic_crud, user_journey (2 selected)
   Storage: in-memory
   Intermediate Verification: enabled
   Parallel Workflows: disabled

⚙️  Phase 1: Setup (2.1s)
   ✓ Loaded task-manager-agent specification
   ✓ Loaded task-viewer specification
   ✓ Initialized in-memory storage
   ✓ Prepared 2 workflow scenarios

🔄 Phase 2: Execution (14.5s)

SCENARIO 1: Basic CRUD Workflow
   Step 1: Create task "Buy milk"
      → create_task(title="Buy milk", description="")
      ✓ Task created with ID 1
      ✓ Storage state: 1 task
   Step 2: Read task by ID
      → get_task(1)
      ✓ Retrieved task 1 successfully
      ✓ Data matches created task
   Step 3: Update task to mark completed
      → update_task(1, completed=True)
      ✓ Task updated successfully
      ✓ Storage state: 1 task, task 1 completed=True
   Step 4: Read task again to verify update
      → get_task(1)
      ✓ Task 1 shows completed=True
   Step 5: Delete task
      → delete_task(1)
      ✓ Task deleted successfully
      ✓ Storage state: 0 tasks
   Step 6: Verify task no longer exists
      → get_task(1)
      ✓ Task not found (expected)

   ✅ SCENARIO 1 PASSED (6/6 steps) - 2.3s

SCENARIO 2: Task Lifecycle Journey
   Step 1: Create task "Submit project report"
      → create_task(title="Submit project report", description="", completed=False)
      ✓ Task created with ID 1
   Step 2: Create task "Review team feedback"
      → create_task(title="Review team feedback", description="", completed=False)
      ✓ Task created with ID 2
   Step 3: Create task "Update presentation slides"
      → create_task(title="Update presentation slides", description="", completed=False)
      ✓ Task created with ID 3
      ✓ Storage state: 3 tasks, all incomplete
   Step 4: List all tasks
      → list_all_tasks()
      ✓ Retrieved 3 tasks
   Step 5: Mark "Review team feedback" as complete
      → update_task(2, completed=True)
      ✓ Task 2 marked complete
   Step 6: List incomplete tasks
      → filter_tasks(completed=False)
      ✓ Retrieved 2 incomplete tasks (IDs 1, 3)
   Step 7: Update "Submit project report" title
      → update_task(1, title="Submit final project report")
      ✓ Title updated
   Step 8: Mark "Submit final project report" as complete
      → update_task(1, completed=True)
      ✓ Task 1 marked complete
   Step 9: List incomplete tasks
      → filter_tasks(completed=False)
      ✓ Retrieved 1 incomplete task (ID 3)
   Step 10: Complete "Update presentation slides"
      → update_task(3, completed=True)
      ✓ Task 3 marked complete
   Step 11: List all tasks
      → list_all_tasks()
      ✓ Retrieved 3 tasks, all complete
   Step 12: Archive all completed tasks
      → delete_task(1), delete_task(2), delete_task(3)
      ✓ All tasks deleted
      ✓ Storage state: 0 tasks
   Step 13: Verify empty list
      → list_all_tasks()
      ✓ Task list empty (expected)

   ✅ SCENARIO 2 PASSED (13/13 steps) - 4.8s

📊 Phase 3: Results (1.2s)

SUMMARY:
   Scenarios: 2/2 passed (100%)
   Steps: 19/19 passed (100%)
   Execution Time: 14.5s

INTEGRATION CHECKS:
   ✓ task-manager ↔ task-viewer integration
   ✓ Storage consistency maintained
   ✓ State transitions valid
   ✓ Error handling correct

✅ ALL WORKFLOWS PASSED

🎯 Recommendations:
   • System ready for user acceptance testing
   • Consider adding to automated regression suite
   • Document workflows as usage examples

📄 Full report: .claude/reports/verify-task-crud-flow-2025-12-28-144000.json
```

## Failure Handling

### Failure Scenario 1: Agent Specification Missing
**Condition**: Required agent files not found
**Detection**: File existence check in Step 1.1
**Response**:
```json
{
  "status": "ERROR",
  "error_type": "MISSING_AGENT_SPECS",
  "message": "Cannot verify workflows without agent specifications",
  "missing_files": [
    ".claude/agents/task-manager-agent.md",
    ".claude/agents/task-viewer.md"
  ],
  "resolution": "Ensure both agent specification files exist before running verification",
  "exit_code": 1
}
```
**Recovery**: Abort execution, instruct user to create agent files

### Failure Scenario 2: Scenario Execution Timeout
**Condition**: Scenario exceeds 5-minute timeout
**Detection**: Timeout wrapper around scenario execution
**Response**:
```json
{
  "status": "TIMEOUT",
  "scenario": "Multi-Task Management Workflow",
  "completed_steps": 5,
  "total_steps": 8,
  "timeout_seconds": 300,
  "last_successful_step": "Filter by completed=true",
  "hung_operation": "update_task(3, completed=True)",
  "message": "Scenario exceeded maximum execution time",
  "possible_causes": [
    "Infinite loop in update_task method",
    "Deadlock in storage layer",
    "Resource exhaustion"
  ],
  "resolution": "Investigate hung operation, check logs for deadlock or infinite loop"
}
```
**Recovery**: Terminate scenario, continue with next scenario unless `stop_on_first_failure=true`

### Failure Scenario 3: Storage State Corruption Mid-Workflow
**Condition**: Intermediate state verification detects corruption
**Detection**: State check in Step 2.1 (substep 3)
**Response**:
```json
{
  "status": "CRITICAL",
  "error_type": "STORAGE_CORRUPTION_DETECTED",
  "scenario": "Basic CRUD Workflow",
  "step": 3,
  "issue": "Task count mismatch after update operation",
  "expected_state": {"task_count": 1, "task_ids": [1]},
  "actual_state": {"task_count": 2, "task_ids": [1, 2]},
  "message": "Storage corrupted during workflow execution",
  "impact": "Cannot trust subsequent test results",
  "resolution": "Investigate update_task method for duplicate creation bug",
  "abort_scenario": true
}
```
**Recovery**: Abort current scenario, optionally continue with fresh storage for next scenario

### Failure Scenario 4: Invalid Workflow Scenario Parameter
**Condition**: Unknown scenario name in `workflow_scenarios`
**Detection**: Input validation during scenario loading
**Response**:
```json
{
  "status": "ERROR",
  "error_type": "INVALID_SCENARIO",
  "message": "Unknown workflow scenario requested",
  "invalid_scenarios": ["task_sharing", "advanced_filters"],
  "valid_scenarios": [
    "basic_crud",
    "user_journey",
    "edge_cases",
    "error_recovery",
    "all"
  ],
  "resolution": "Use valid scenario names from the list above",
  "exit_code": 2
}
```
**Recovery**: Abort execution, prompt user for valid scenario names

### Failure Scenario 5: Parallel Workflow Collision
**Condition**: Concurrent workflows interfere with each other
**Detection**: Post-workflow validation finds unexpected state
**Response**:
```json
{
  "status": "FAIL",
  "error_type": "WORKFLOW_INTERFERENCE",
  "message": "Parallel workflows corrupted each other's data",
  "workflow_a": "User A workflow",
  "workflow_b": "User B workflow",
  "interference_details": {
    "workflow_a_task_lost": {"id": 2, "title": "User A Task 2"},
    "workflow_b_task_corrupted": {"id": 3, "title": "User B Task 1", "issue": "Title overwritten by workflow A"}
  },
  "root_cause": "Concurrent operations not properly isolated",
  "impact": "Parallel execution mode cannot be trusted",
  "resolution": "Fix concurrency issues in storage layer or disable parallel_workflows"
}
```
**Recovery**: Mark parallel test as failed, disable parallel mode for remaining tests

### Failure Scenario 6: Expected vs. Actual Mismatch (Typical Failure)
**Condition**: Operation returns unexpected result
**Detection**: Output comparison in Step 2.1 (substep 4)
**Response**:
```json
{
  "status": "FAIL",
  "scenario": "Partial Update Workflow",
  "step": 3,
  "operation": "update_task(1, title='Updated')",
  "expected_output": {
    "success": true,
    "data": {"id": 1, "title": "Updated", "description": "Desc", "completed": false}
  },
  "actual_output": {
    "success": true,
    "data": {"id": 1, "title": "Updated", "description": "", "completed": false}
  },
  "diff": {
    "field": "description",
    "expected": "Desc",
    "actual": "",
    "issue": "Field was cleared instead of preserved"
  },
  "severity": "CRITICAL",
  "continue_scenario": true
}
```
**Recovery**: Log failure, continue with remaining steps unless `stop_on_first_failure=true`

---

## Usage Notes

- This skill is **deterministic** for single-threaded workflows (same inputs → same results)
- Parallel workflows may have non-deterministic timing but should always maintain data consistency
- Each scenario runs with fresh storage to ensure test isolation
- Can be integrated into CI/CD pipeline for automated regression testing
- Recommended to run after completing all CRUD implementation tasks
- Combine with `validate-task-operations` and `test-task-data-integrity` for complete QA coverage

## Agent Integration

This skill is owned by the **QA Agent** and can be invoked via:
```bash
/qa verify-task-crud-flow --scenarios basic_crud user_journey --verbose true
```

Or programmatically:
```python
qa_agent.execute_skill(
    skill_id="qa.verify-task-crud-flow",
    params={
        "workflow_scenarios": ["basic_crud", "user_journey"],
        "storage_type": "in-memory",
        "verify_intermediate_states": True,
        "simulate_delays": False,
        "parallel_workflows": False,
        "verbose_output": True,
        "stop_on_first_failure": False
    }
)
```
