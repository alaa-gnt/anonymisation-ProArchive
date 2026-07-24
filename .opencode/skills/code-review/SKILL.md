---
name: code-review
description: Review code changes for correctness, maintainability, safety, and adherence to standards, providing actionable feedback that improves both the code and the team.
---

# code-review

## 1. Work skill name
Code Review

## 2. Job to be done
Review code changes for correctness, maintainability, safety, and adherence to standards, providing actionable feedback that improves both the code and the team.

## 3. Trigger or use case
- A pull request or merge request is opened
- A significant code change needs review before integration
- A junior developer submits code that needs mentoring
- A cross-team change needs a domain expert's review

## 4. Required inputs
- The diff (changed lines of code)
- The pull request description and context
- Related requirements, acceptance criteria, or user stories
- Existing code in the changed module
- Coding standards and conventions

## 5. Step-by-step workflow

### Step 1: Understand the change
- Read the PR description and any linked issues
- Understand what the change is supposed to do
- Identify the scope: is this a small bug fix or a large feature?
- Check if tests are included

### Step 2: Review the high-level design
- Is the approach correct for the problem? (CC Ch.4)
- Does the change fit with the existing architecture?
- Are the right patterns being used? (not over-engineering, not under-engineering)
- Does the change belong in this module or should it be elsewhere?
- Check for tactical programming: quick hacks that will cause long-term pain (POSD Ch.3)

### Step 3: Review for correctness
- Does the code do what the requirements say? (CC Ch.20)
- Are all edge cases handled? (empty, null, max, out-of-range)
- Are error paths handled properly? (CC Ch.8)
- Is there any dead code or unreachable paths?
- Are concurrency/thread-safety issues handled? (DDIA Ch.7)
- Check for off-by-one errors, type mismatches, unsafe casts

### Step 4: Review for maintainability
- Is the code easy to read and understand?
- Are the names meaningful? (method names, variable names, class names) (POSD Ch.4, Refactoring Ch.6)
- Are functions/methods short enough? (heuristic: <10 lines is ideal for a single responsibility)
- Is the module deep or shallow? (POSD Ch.4)
- Is there duplicated code that should be extracted? (Refactoring Ch.3)
- Are there commented-out code blocks? (remove them, don't merge them)

### Step 5: Review for safety and security
- Are inputs validated and sanitized?
- Is authentication and authorization handled correctly?
- Are secrets (passwords, tokens) handled securely? (never log secrets)
- Is there risk of injection (SQL, XSS, command injection)?
- Are rate limits handled?

### Step 6: Review tests
- Do the tests cover the happy path? (CC Ch.20)
- Do the tests cover edge cases and error paths?
- Are the tests readable and maintainable?
- Do the tests actually fail when the code is broken? (no tautological tests)
- Is coverage sufficient for the change?

### Step 7: Review performance
- Could the code cause performance issues? (N+1 queries, large allocations, blocking calls)
- Are database queries using indexes?
- Is there unnecessary work in hot paths?
- Are caching opportunities missed?

### Step 8: Provide feedback
- Be specific: "Line 42: this function can throw null" not "this is buggy" (TPP Ch.7)
- Be constructive: suggest alternatives, not just problems
- Prioritize: blockers (must fix before merge), warnings (should fix), nits (nice to have)
- Explain the why, not just the what: "This pattern is fragile because..."
- Ask questions, don't dictate: "What happens if X is null?" instead of "Check for null here"

## 6. Output deliverable
A code review with categorized feedback: blockers (must fix before merge), warnings (should fix), nits (optional improvements), and questions (clarifications needed).

## 7. Quality checklist
- [ ] Change is understood (read the PR description)
- [ ] Design approach is appropriate
- [ ] Edge cases and error paths are handled
- [ ] Security concerns are addressed
- [ ] Tests exist and are meaningful
- [ ] No tactical programming / technical debt shortcuts
- [ ] Code follows project conventions
- [ ] No duplicated code
- [ ] Performance implications are considered
- [ ] Feedback is specific, constructive, and prioritized

## 8. Common failure modes
- Nitpicking style issues instead of focusing on correctness (CC Ch.26)
- Not reading the full context, only the diff (miss integration issues)
- Being too harsh or too passive (both damage team culture)
- Reviewing too late after the code is already "done" (TPP Ch.7)
- Assuming tests are adequate without checking them (CC Ch.20)
- Not considering edge cases (CC Ch.20)
- Rubber-stamping: approving without actually reviewing (CC Ch.26)
- Focusing on the implementation but ignoring whether it solves the right problem (TPP Ch.7)

## 9. Dependencies on framework skills
- Refactoring (to identify code smells and suggest improvements)
- Testing and Verification (to evaluate test quality)
- System Decomposition (to check module boundaries)

## 10. Source books used
- Primary: Code Complete (McConnell)
- Support: Refactoring (Fowler), The Pragmatic Programmer (Hunt & Thomas), A Philosophy of Software Design (Ousterhout)

## 11. Example of a good final output structure
```
## Code Review: feat/add-order-cancellation

### Blocker (must fix)
- Line 87: NullPointerException when `order.payment` is null. Add null check before calling .refund()
- Line 120: SQL injection risk. Use parameterized query instead of string interpolation

### Warning (should fix)
- Lines 150-180: Duplicate validation logic between createOrder() and cancelOrder(). Extract to OrderValidator class
- No test for concurrent cancellation (two requests cancel same order)

### Nit (optional)
- Line 45: Consider renaming `process()` to `cancelOrder()` for clarity

### Questions
- What happens if the payment service is down? Do we retry or fail immediately?
```
