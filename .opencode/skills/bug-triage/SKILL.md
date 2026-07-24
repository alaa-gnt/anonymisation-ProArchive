---
name: bug-triage
description: Triage a bug report to determine its severity, root cause category, and required fix priority, then route it to the right engineer for resolution.
---

# bug-triage

## 1. Work skill name
Bug Triage

## 2. Job to be done
Triage a bug report to determine its severity, root cause category, and required fix priority, then route it to the right engineer for resolution.

## 3. Trigger or use case
- A bug is reported (by user, QA, monitoring, or automated test)
- An incident is detected in production
- A regression is found during development
- A bug backlog needs prioritization

## 4. Required inputs
- Bug report: description, steps to reproduce, expected vs. actual behavior, environment, frequency, impact
- Logs, error messages, stack traces (if available)
- Recent code changes that might be related
- System metrics (latency, error rate, CPU/memory usage) around the time of the bug

## 5. Step-by-step workflow

### Step 1: Reproduce the bug
- Try to reproduce the bug using the steps provided
- If reproduction steps are missing, ask for them or try to infer from the description
- If the bug is intermittent, collect additional data (logs, metrics, traces)
- Determine: is it reproducible? What is the exact trigger?
- If not reproducible, classify as "no repro" and add monitoring to catch it next time (CC Ch.20)

### Step 2: Classify the root cause category
- **Logic error**: Race condition, off-by-one, missing null check, wrong conditional (CC Ch.20, Ch.22)
- **Data issue**: Missing data, wrong data, data corruption, failed migration (DDIA Ch.4, FDE Ch.5)
- **State/consistency**: Replication lag, stale cache, concurrent modification (DDIA Ch.7, Ch.9)
- **Integration error**: API contract mismatch, timeout, retry exhaustion (DWA Ch.4, DDIA Ch.8)
- **Environment/deployment**: Wrong config, missing env var, wrong version (TPP Ch.7)
- **Performance**: Slow query, memory leak, resource exhaustion (DDIA Ch.1, CC Ch.25)
- **User error**: Misunderstanding of intended behavior (documentation or UX improvement)

### Step 3: Determine severity
- **Critical (P0)**: Data loss, security breach, complete system unavailability
- **High (P1)**: Major feature broken for all users, significant revenue impact
- **Medium (P2)**: Feature broken for some users, workaround exists
- **Low (P3)**: Minor issue, cosmetic, edge case, no workaround needed
- **Wishlist (P4)**: Improvement, enhancement request

### Step 4: Determine priority based on severity and frequency
- Critical + frequent → fix immediately (drop everything)
- Critical + rare → fix within the current sprint
- High + frequent → fix within the current sprint
- High + rare → schedule for next sprint
- Medium → schedule per triage
- Low → add to backlog

### Step 5: Add context for the engineer
- Add reproduction steps
- Add relevant logs and stack traces
- Add the root cause category guess
- Add any recent relevant code changes (git blame)
- Add the expected fix direction (if known)
- Tag the component or service owner
- Reference related issues

### Step 6: Follow up on the fix
- Verify the fix is tested: add a regression test that would catch this bug (CC Ch.20, Refactoring Ch.2)
- Verify the fix is deployed to production
- Update the bug status: resolved, verified, closed
- If the fix reveals a deeper pattern (class of bugs), recommend a systemic fix (TIS Ch.3)

## 6. Output deliverable
A triaged bug report with: reproduction steps, root cause category, severity (P0-P4), priority, assigned engineer, related changes, and regression test plan.

## 7. Quality checklist
- [ ] Bug is reproduced or sufficient data is collected for investigation
- [ ] Root cause category is identified (logic, data, state, integration, env, performance)
- [ ] Severity is assigned (P0-P4) based on impact
- [ ] Priority considers both severity and frequency
- [ ] Reproduction steps are clear and complete
- [ ] Relevant logs, stack traces, and metrics are attached
- [ ] Recent related code changes are identified (if applicable)
- [ ] Bug is assigned to the right engineer/team
- [ ] Regression test is planned to prevent recurrence
- [ ] If multiple bugs share the same root cause, they are grouped

## 8. Common failure modes
- Not reproducing the bug before assigning it (wastes the engineer's time)
- Over-escalating (P0 everything → nobody takes P0 seriously)
- Under-escalating (letting a critical bug sit in the backlog)
- Not adding enough context (engineer has to ask for basic info)
- Fixing the symptom but not the root cause (CC Ch.20)
- Not adding a regression test → same bug reappears in 3 months (CC Ch.20)
- Blaming users instead of fixing the underlying UX or system issue (TIS Ch.3)
- Forgetting to check if the same pattern exists elsewhere (systemic fix opportunity)

## 9. Dependencies on framework skills
- Testing and Verification (regression test planning)
- Systems Thinking (identifying systemic vs. isolated bugs)
- Refactoring (fixing code quality issues found during triage)

## 10. Source books used
- Primary: Code Complete (McConnell)
- Support: The Pragmatic Programmer (Hunt & Thomas), Refactoring (Fowler), A Philosophy of Software Design (Ousterhout), Designing Data-Intensive Applications (Kleppmann)

## 11. Example of a good final output structure
```
## Bug Triage: BUG-4521

### Title: Order cancellation returns 500 when payment service is down

### Reproduction Steps
1. Place an order
2. Stop the payment service
3. POST /orders/{id}/cancel
4. Response: 500 Internal Server Error instead of 503 Service Unavailable

### Root Cause Category
Integration error: no timeout or circuit breaker for payment service call

### Severity: P1 (High)
- Affects: all users during payment service outage
- Impact: users cannot cancel orders during payment service degradation
- Frequency: rare (payment service has 99.9% uptime)

### Related Changes
- Commit a1b2c3: added payment service integration
- PR #1234: order cancellation feature

### Assigned To: @backend-team

### Regression Test
- Test: cancel order when payment service returns 503
- Expected: return 503, not 500

### Note
This is a systemic issue: all services that call payment service should handle its downtime gracefully.
```
