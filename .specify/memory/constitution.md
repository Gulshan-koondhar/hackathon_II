<!--
SYNC IMPACT REPORT: Constitution Update
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Version Change: N/A → 1.0.0
Rationale: Initial constitution ratification for Phase 1 In-Memory Todo CLI

Modified Principles:
  - All principles newly defined (no prior version)

Added Sections:
  - Core Principles (6 principles)
  - Technical Constraints
  - Development Workflow
  - Governance

Removed Sections: None (initial version)

Templates Requiring Updates:
  ✅ plan-template.md - Constitution Check section already present
  ✅ spec-template.md - No constitution-specific dependencies
  ✅ tasks-template.md - Task structure aligns with principles

Follow-up TODOs: None

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
-->

# Phase 1 In-Memory Todo CLI Constitution

## Core Principles

### I. Specification-First Development (NON-NEGOTIABLE)

**All behavior MUST be defined in written specifications before any code is written.**

- Every feature MUST have a complete specification in Markdown format documenting:
  - User scenarios with acceptance criteria
  - Functional requirements with unique IDs (FR-XXX)
  - Success criteria that are measurable and testable
  - Edge cases and error conditions
- Specifications MUST be unambiguous—no room for interpretation or guessing
- Code generation MUST strictly follow the written specification with zero deviation
- Human developers MUST NOT manually write code; all implementation is spec-driven
- Any ambiguity in specifications MUST be resolved through clarification before implementation begins

**Rationale**: Spec-first ensures deterministic, predictable behavior and enables AI-driven code generation without interpretation errors.

### II. Phase Discipline (NON-NEGOTIABLE)

**Strict adherence to Phase 1 scope boundaries—no features, optimizations, or extensions beyond the defined scope.**

- Phase 1 scope is limited to EXACTLY these five operations:
  1. Add a task
  2. Update a task
  3. Delete a task
  4. List all tasks
  5. Toggle task completion status
- Any feature, optimization, or extension beyond Phase 1 scope MUST be rejected immediately
- No "just in case" code, no premature abstractions, no forward-looking architecture
- No persistence mechanisms (files, databases) of any kind in Phase 1
- No user accounts, authentication, authorization, or multi-user support
- No web interfaces, APIs, or non-CLI interaction methods
- Performance optimization beyond functional correctness is out of scope

**Rationale**: Phase discipline prevents scope creep, over-engineering, and complexity that undermines simplicity and predictability.

### III. Simplicity Over Over-Engineering (NON-NEGOTIABLE)

**Choose the simplest solution that meets the specification—reject abstractions, patterns, or complexity without clear justification.**

- Start with the most direct implementation: lists, dictionaries, simple functions
- Abstractions (classes, design patterns, frameworks) MUST be justified by:
  - Specification requirement that cannot be met with simpler approach
  - Explicit complexity budget approval with documented rationale
- YAGNI (You Aren't Gonna Need It) is the default stance—no speculative features
- If two solutions meet the spec, choose the one with fewer lines and fewer concepts
- No dependencies beyond Python 3.13+ standard library unless explicitly required by spec

**Rationale**: Simplicity ensures maintainability, clarity, and reduces bugs. Over-engineering creates unnecessary cognitive load and technical debt.

### IV. Reusable Domain Intelligence

**Domain rules, constraints, and business logic MUST be explicitly documented and reusable across implementations.**

- Domain rules MUST be captured in specification documents, not buried in code
- Validation rules (title length, ID formats, state transitions) MUST be documented clearly
- Business logic MUST be separated from presentation/interface concerns
- Task management rules MUST be specified such that they work across CLI, future web UI, or API
- Contracts between components (agents, services) MUST be explicit and documented

**Rationale**: Clear domain rules enable reuse, testing, and consistent behavior across interfaces.

### V. Deterministic and Predictable Behavior

**Every system behavior MUST be deterministic—same inputs produce same outputs, with zero ambiguity.**

- All operations MUST return predictable, structured responses (success/failure, message, data)
- Error messages MUST be specific, actionable, and consistent
- State transitions MUST be well-defined (task creation → update → completion → deletion)
- No randomness, no timestamps (unless required by spec), no environment-dependent behavior
- All test cases MUST produce identical results across runs and environments

**Rationale**: Deterministic behavior enables reliable testing, debugging, and user trust.

### VI. Test-Driven Development (MANDATORY)

**Tests MUST be written first, MUST fail, then implementation makes them pass.**

- Red-Green-Refactor cycle is strictly enforced:
  1. **Red**: Write test(s) for a feature, verify they FAIL
  2. **Green**: Write minimal code to make tests PASS
  3. **Refactor**: Clean up while keeping tests passing
- Tests MUST cover:
  - Happy path scenarios (valid inputs, expected outputs)
  - Edge cases (boundary values, empty inputs, maximum lengths)
  - Error cases (invalid inputs, non-existent IDs, constraint violations)
- Test descriptions MUST be clear, specific, and map to specification requirements
- No implementation without corresponding tests approved by user

**Rationale**: TDD ensures code correctness, prevents regressions, and validates that specifications are testable.

## Technical Constraints

### Language and Platform

- **Language**: Python 3.13 or higher REQUIRED
- **Interface**: Command-line (CLI) only—no GUI, no web interface
- **Platform**: Cross-platform (Windows, macOS, Linux) via standard Python CLI

### Storage and Persistence

- **Storage**: In-memory data structures ONLY (lists, dictionaries, Python objects)
- **Persistence**: PROHIBITED—data is lost when program exits
- **Databases**: PROHIBITED (PostgreSQL, SQLite, Redis, etc.)
- **Files**: PROHIBITED for data storage (JSON, CSV, text files, etc.)
- Configuration files for application settings are PROHIBITED in Phase 1

### Dependencies and Frameworks

- **Standard Library**: Python 3.13+ standard library is ALLOWED
- **External Dependencies**: PROHIBITED unless explicitly required by specification
- **Web Frameworks**: PROHIBITED (Flask, FastAPI, Django, etc.)
- **ORMs**: PROHIBITED (SQLAlchemy, Django ORM, etc.)
- **Authentication Libraries**: PROHIBITED (no user accounts in Phase 1)

### Prohibited Technologies

- **AI/ML**: No runtime AI, agents, embeddings, NLP, or automation libraries
- **APIs**: No REST APIs, GraphQL, gRPC, or any network communication
- **Async/Concurrency**: Not required for Phase 1; synchronous code is sufficient
- **Background Jobs**: No task queues, schedulers, or background processing

### Tooling

- **Specification**: Spec-Kit Plus framework for documentation
- **Development**: Claude Code for spec-driven implementation
- **Testing**: Python's built-in `unittest` or `pytest` (if needed for TDD)
- **Linting**: Optional—use `ruff` or `pylint` if code quality checks needed

## Development Workflow

### Specification Phase

1. **Create Feature Spec**: Use `/sp.specify` to create `specs/[feature]/spec.md`
   - Define user scenarios with acceptance criteria
   - Document functional requirements (FR-XXX)
   - Define success criteria and edge cases
2. **Clarify Ambiguities**: Use `/sp.clarify` to resolve unclear requirements
3. **User Approval**: Feature spec MUST be approved before planning

### Planning Phase

4. **Create Implementation Plan**: Use `/sp.plan` to create `specs/[feature]/plan.md`
   - Define technical approach (Python modules, data structures)
   - Document project structure (`src/`, `tests/`)
   - Run Constitution Check—verify no violations
5. **Complexity Justification**: If Constitution Check fails, document violations and simpler alternatives rejected
6. **User Approval**: Implementation plan MUST be approved before tasking

### Task Breakdown Phase

7. **Generate Tasks**: Use `/sp.tasks` to create `specs/[feature]/tasks.md`
   - Break plan into atomic, testable tasks
   - Mark parallel tasks with `[P]`
   - Define dependencies and execution order
8. **User Approval**: Task list MUST be approved before implementation

### Implementation Phase

9. **Test-First**: Write tests for each task FIRST, verify they FAIL
10. **Implement**: Write minimal code to make tests PASS
11. **Refactor**: Clean up code while keeping tests passing
12. **Validate**: Run all tests, ensure Phase 1 scope compliance
13. **Commit**: Use `/sp.git.commit_pr` to commit with standardized messages

### Quality Gates

- **Constitution Check**: Every plan MUST pass or justify violations
- **Phase Compliance**: Every feature MUST be within Phase 1 scope
- **Test Coverage**: Every feature MUST have passing tests
- **Simplicity Review**: Every implementation MUST be simplest solution
- **Specification Alignment**: Code MUST match specification exactly

### Review and Approval

- Human approval REQUIRED at: Spec, Plan, Tasks, Implementation
- No code proceeds to next phase without explicit approval
- Violations or scope creep trigger immediate halt and clarification

## Governance

### Authority and Compliance

- **This constitution supersedes all other practices, patterns, and preferences**
- All pull requests MUST verify constitution compliance before merge
- Any violation MUST be documented, justified, and approved
- Complexity beyond simplest solution MUST have written rationale in plan.md
- Phase violations (out-of-scope features) are grounds for rejection

### Amendment Process

- Constitution changes REQUIRE:
  1. Written proposal with rationale
  2. Impact analysis on existing specs and code
  3. User/stakeholder approval
  4. Version bump following semantic versioning
  5. Update to all dependent templates and documentation
- Amendments MUST be documented in Sync Impact Report at top of this file

### Versioning Policy

- **Version Format**: MAJOR.MINOR.PATCH (semantic versioning)
- **MAJOR**: Backward-incompatible governance changes, principle removals/redefinitions
- **MINOR**: New principles added, material expansions to existing guidance
- **PATCH**: Clarifications, wording improvements, typo fixes, non-semantic refinements

### Runtime Guidance

- For agent-specific guidance, refer to `CLAUDE.md` in repository root
- For skill development, see `.claude/skills/` directory
- For agent definitions, see `.claude/agents/` directory
- For command workflows, see `.claude/commands/` directory

### Success Criteria for Phase 1

This constitution is successful when:

- ✅ A complete, unambiguous feature specification exists for all Phase 1 operations
- ✅ All five Phase 1 features (add, update, delete, list, toggle) work as specified
- ✅ Code strictly follows written specs with zero deviation or interpretation
- ✅ Application runs without errors in local CLI environment (Python 3.13+)
- ✅ All tests pass and cover happy paths, edge cases, and error conditions
- ✅ No Phase 1 scope violations exist (persistence, auth, web UI, etc.)
- ✅ No over-engineering detected (simplest solution is used throughout)
- ✅ Domain rules are clearly documented and reusable

**Version**: 1.0.0 | **Ratified**: 2025-12-28 | **Last Amended**: 2025-12-28
