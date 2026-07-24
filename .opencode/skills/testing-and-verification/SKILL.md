---
name: testing-and-verification
description: Create a testing strategy that catches defects early, documents correct behavior, and enables safe refactoring without wasting effort.
---

# testing-and-verification

## 1. Skill name
Testing and Verification

## 2. One-line purpose
Create a testing strategy that catches defects early, documents correct behavior, and enables safe refactoring without wasting effort.

## 3. When to use this skill
- When starting a new project (establish the testing approach)
- When writing test cases for new or existing code
- When reviewing test coverage and effectiveness
- When a bug escapes to production (improve the testing gap)
- When refactoring or changing existing code (safety net)

## 4. When not to use this skill
- For throwaway prototypes or proof-of-concept code
- When the cost of testing exceeds the cost of failure
- For systems with no deterministic behavior (e.g., some ML systems—use evaluation plans instead)

## 5. Core principles
- **Testing reduces risk, it does not eliminate it**: Even exhaustive testing cannot prove the absence of defects. The goal is to reduce the probability of failure to an acceptable level (CC Ch.20).
- **A good test is one that finds a defect**: Test cases that have never failed are less valuable than those that have (CC Ch.20).
- **Test at different levels of the testing pyramid**: Unit tests (many, fast, isolated), Integration tests (fewer, test interactions), System tests (few, test end-to-end), Acceptance tests (validate requirements) (CC Ch.20, TPP Ch.7).
- **Tests must be reliable**: A flaky test (sometimes passes, sometimes fails) is worse than no test. It erodes trust in the test suite (CC Ch.20).
- **Tests should be maintainable**: When the code changes, the tests should change minimally. Brittle tests that break for every change are a liability (Refactoring Ch.2, CC Ch.20).
- **Write tests before code (TDD)**: Decide what behavior is needed, write a test that fails, then implement the behavior. This ensures testability and focuses the design (TPP Ch.7, Refactoring Ch.2).
- **Test one thing per test case**: Each test should verify one specific behavior. This makes failures easy to diagnose (CC Ch.20).
- **Boundary conditions are the most error-prone**: Test off-by-one, empty, null, max/min, and edge cases explicitly (CC Ch.20, TPP Ch.7).
- **Error handling paths must be tested**: The happy path is well-tested; the failure paths are where bugs hide. Test each error handler (CC Ch.8, Ch.20).
- **Testing is part of the development process, not a separate phase**: Continuous testing with every build reduces feedback time (TPP Ch.7, Refactoring Ch.2).

## 6. Step-by-step method

### Step 1: Define the testing strategy
- Determine the testing levels needed (unit, integration, system, acceptance) (CC Ch.20)
- Set quality goals: what level of coverage is required? (Heuristic: 80% branch coverage for critical code, lower for UI/glue code)
- Decide on testing frameworks and tools
- Establish CI requirements: tests must pass before merge

### Step 2: Design unit tests
- Identify the smallest testable units (functions, methods, classes) (CC Ch.20)
- For each unit:
  - List the inputs and expected outputs
  - Identify equivalence classes (partition the input space)
  - Identify boundary conditions (max, min, empty, null, off-by-one)
  - Identify error conditions and exceptions
- Write one test per behavior (not per method):
  - `test_method_whenCondition_expectedBehavior` naming
- Each test should be independent: no shared state, no order dependencies
- Mock external dependencies (databases, APIs, filesystems) (CC Ch.20, TPP Ch.7)

### Step 3: Design integration tests
- Identify the boundaries where units interact (e.g., data access, service calls) (CC Ch.20)
- Test the interaction between real components (database queries, API calls)
- Use realistic data (not just nulls and empty strings)
- Test failure modes: what happens when the database is down? When the API returns an error?
- Integration tests are slower; keep the number manageable (heuristic: 20% of test suite)

### Step 4: Design system and acceptance tests
- System tests: test the complete system end-to-end (CC Ch.20)
- Acceptance tests: verify the system meets business requirements
- Use scenarios that reflect real user workflows
- Test deployment configurations, not just development environments
- Smoke tests: quick checks that the system is running after deployment

### Step 5: Test error handling and edge cases
- For each error path (try/catch, error return, exception), write a test that triggers it (CC Ch.8)
- Test with invalid, malformed, and out-of-range inputs
- Test with missing dependencies (files, services, network)
- Test concurrent access (race conditions, deadlocks) (DDIA Ch.7)
- Test resource limits (memory, disk space, connections)

### Step 6: Review and refactor tests
- Remove duplicate tests: if two tests cover the same behavior, keep one
- Remove tests that never fail: they provide no value (CC Ch.20)
- Refactor tests when the production code changes: tests should mirror the structure
- Check test coverage metrics (line, branch, condition) (CC Ch.20)
- Ensure tests are fast enough to run on every commit (heuristic: unit tests < 1 min, integration < 10 min)

### Step 7: Automate and integrate
- Run unit tests on every commit (pre-commit or CI)
- Run integration tests on every merge to main branch
- Run system and acceptance tests on every release candidate
- Review test failures immediately: a red build is a broken build
- Track test health: flaky tests, skipped tests, coverage trends

## 7. Decision rules
- **If a bug escapes to production, write a test that reproduces it before fixing** (regression test) (CC Ch.20, TPP Ch.7).
- **If a test is flaky (sometimes fails for reasons unrelated to the code), fix or remove it immediately** (CC Ch.20).
- **If a test takes more than 100ms, it's not a unit test—it's an integration test** (CC Ch.20).
- **If you cannot write a test for a method without extensive mocking, the method may have too many dependencies** (POSD Ch.4, CC Ch.20).
- **If branch coverage is below 80%, identify untested branches and add tests** (CC Ch.20).
- **If there is no test for the error handling path, assume it is broken** (CC Ch.8).
- **If changing a feature requires changing 50 tests, the tests are too brittle** (Refactoring Ch.2).
- **If a test shares mutable state with other tests, fix it. Tests must be independent** (CC Ch.20).
- **If the test suite takes more than 5 minutes to run, optimize it or split it into fast/slow suites** (CC Ch.20).
- **If the code is too hard to test, the design is wrong** (TPP Ch.7, POSD Ch.11).

## 8. Common mistakes
- Testing the trivial things but not the edge cases (testing getters/setters but not boundary conditions) (CC Ch.20).
- Writing tests that pass even when the code is broken (e.g., testing the mock, not the real object).
- Testing implementation details instead of behavior: tests break when you refactor (Refactoring Ch.2).
- Relying only on unit tests and skipping integration tests (the pyramid needs all levels) (CC Ch.20).
- Using code coverage as a goal rather than a metric. 100% coverage does not mean bug-free (CC Ch.20).
- Writing tests that depend on the execution order of other tests (non-deterministic test suites).
- Ignoring flaky tests. A flaky test erodes trust in the entire suite (CC Ch.20).
- Testing error handling with mocks that never fail: if the mock always succeeds, the error path is not tested.
- Failing to test the integration between services in a microservices architecture.
- Writing acceptance tests that are too verbose and hard to maintain (CC Ch.20).

## 9. Output format
```
## Testing Plan: [Module/System Name]

### Strategy Summary
- Test levels: [unit, integration, system, acceptance]
- Coverage target: [e.g., 80% branch coverage]
- CI requirements: [e.g., all tests pass before merge]

### Unit Tests
| Module | Test Name | Input | Expected Output | Coverage |
|--------|-----------|-------|-----------------|----------|

### Integration Tests
| Scenario | Components Involved | Data Setup | Expected Behavior |
|----------|-------------------|------------|-------------------|

### System/Acceptance Tests
| Scenario | Workflow Steps | Expected Outcome |
|----------|---------------|------------------|

### Error Handling Tests
| Error Scenario | Trigger | Expected Handling |
|----------------|---------|-------------------|

### Edge Cases
| Case | Reason for Risk | Test |
|------|----------------|------|

### Regression Tests (Bugs Found in Production)
| Bug ID | Root Cause | Regression Test |
|--------|------------|-----------------|
```

## 10. Quality checklist
- [ ] Unit tests cover boundary conditions, equivalence classes, and error paths
- [ ] Integration tests cover component interactions and failure modes
- [ ] Acceptance tests validate business requirements
- [ ] No flaky tests exist in the suite
- [ ] Tests are independent and can run in any order
- [ ] Branch coverage is at least 80% for critical code
- [ ] Error handling paths are tested (not just happy paths)
- [ ] Regression tests exist for all production bugs
- [ ] Tests run on every commit (CI)
- [ ] Test suite is fast enough for the development cycle

## 11. Source books used
- Primary: Code Complete (McConnell)
- Support: The Pragmatic Programmer (Hunt & Thomas), Refactoring (Fowler), A Philosophy of Software Design (Ousterhout)

## 12. Notes on how the books complement each other
CC provides the comprehensive testing framework: test levels, coverage measurement, test design techniques (equivalence partitioning, boundary analysis), and the relationship between testing and quality. TPP adds the TDD methodology, the testing pyramid, and the assertion that hard-to-test code is poorly designed. Refactoring adds the crucial insight that tests are the safety net for all code changes. POSD adds the design perspective: how deep modules with clean interfaces are easier to test. Together they form a complete testing methodology from individual test case design to the overall testing strategy.
