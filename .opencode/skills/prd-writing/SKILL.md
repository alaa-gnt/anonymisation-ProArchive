---
name: prd-writing
description: Write a Product Requirements Document that clearly defines the problem, target users, desired outcomes, features, and success criteria so that engineering can build the right thing.
---

# prd-writing

## 1. Work skill name
PRD Writing

## 2. Job to be done
Write a Product Requirements Document that clearly defines the problem, target users, desired outcomes, features, and success criteria so that engineering can build the right thing.

## 3. Trigger or use case
- A new product or major feature is about to enter development
- The team needs a shared understanding of what to build and why
- The product team needs to communicate requirements to engineering and design
- The product is entering a new phase and needs a defined scope

## 4. Required inputs
- Product vision and strategy (Inspired Ch.2, GSBS Ch.1)
- Customer discovery findings: problem validation, customer segments, jobs-to-be-done (TMT Ch.1-2)
- Competitive analysis (what alternatives exist)
- Business context: revenue model, success metrics, constraints
- User research: personas, user journeys, pain points

## 5. Step-by-step workflow

### Step 1: Define the problem
- Write a clear problem statement: who is the customer, what is the problem, why is it worth solving (Inspired Ch.4)
- Include evidence: customer quotes, data, research findings
- Describe the current alternative: how does the customer solve this today? (TMT Ch.2)
- If the problem is not validated by customer conversations, state that this is an assumption that needs testing (Inspired Ch.7)

### Step 2: Define the target users
- Define the primary customer segment (Inspired Ch.3)
- Include personas if applicable: demographics, goals, pain points, current behavior
- Define secondary users (admins, managers, partners)
- Define who is explicitly NOT a target user (to avoid scope creep)

### Step 3: Define the desired outcome
- What business outcome should this product/feature achieve? (Inspired Ch.5)
- Define success metrics: North Star metric, leading indicators, lagging indicators
- Define counter-metrics (what should NOT degrade)
- Example: "Increase activation rate from 40% to 60% in 3 months"
- The outcome should be measurable and time-bound

### Step 4: Describe the solution (features)
- List the features required to achieve the outcome
- For each feature, describe the user-facing behavior, not the implementation
- Prioritize features: P0 (must have for launch), P1 (should have), P2 (nice to have)
- Include user flows or wireframes if available
- Include acceptance criteria for each feature
- Explicitly state what is NOT in scope (GSBS Ch.6)

### Step 5: Define the release criteria
- What must be true to ship? (minimum quality bar, performance targets, test coverage)
- Define the rollout plan: phased rollout, feature flags, A/B testing (DMLS Ch.6, Ch.9)
- Define the monitoring plan: what metrics will be tracked post-launch?
- Define the rollback plan

### Step 6: Define the post-launch learning plan
- What hypotheses are being tested with this release? (LS Ch.7)
- How will we measure success? (metrics dashboard)
- What will trigger a pivot or iteration?
- What is the next set of features if this succeeds?

## 6. Output deliverable
A Product Requirements Document covering: problem statement, target users, desired outcomes, feature list with priorities, acceptance criteria, release criteria, and success metrics.

## 7. Quality checklist
- [ ] Problem is validated (not an assumption—if it is, state it as such)
- [ ] Target users are specific (not "everyone")
- [ ] Desired outcome is measurable and time-bound
- [ ] Features are prioritized (P0/P1/P2)
- [ ] Each feature has acceptance criteria
- [ ] Exclusions are explicitly documented (what is NOT in scope)
- [ ] Release criteria are defined (quality bar)
- [ ] Rollout and rollback plans are defined
- [ ] Success metrics are defined (not just "users like it")
- [ ] Post-launch learning plan is defined
- [ ] PRD is reviewed with engineering and design before development starts

## 8. Common failure modes
- Writing the PRD before validating the problem (Inspired Ch.4, TMT Ch.1)
- Specifying implementation details instead of user-facing behavior (TPP Ch.2)
- Including too many P0 features (scope creep disguised as prioritization)
- Not defining success metrics (no way to know if the product succeeded) (Inspired Ch.5)
- Writing the PRD in isolation without engineering or design input (Inspired Ch.6)
- Not defining what is out of scope (everyone has different expectations) (GSBS Ch.6)
- Specifying features that don't tie back to the desired outcome
- Writing too much detail for P2 features that will never be built
- Not updating the PRD as learning happens (treating it as a static document) (LS Ch.7)

## 9. Dependencies on framework skills
- Product Discovery (for problem validation and customer insights)
- Strategy Assessment (to align with business strategy)
- Startup Validation (to test assumptions)

## 10. Source books used
- Primary: Inspired (Cagan)
- Support: The Mom Test (Fitzpatrick), The Lean Startup (Ries), Good Strategy Bad Strategy (Rumelt)

## 11. Example of a good final output structure
```
# PRD: Order Cancellation

## Problem Statement
Customers currently cannot cancel orders after placement. If they change their mind, they must contact support. This creates 500 support tickets/month and 3-day resolution times. Customer interviews confirm that self-service cancellation is the #1 requested feature (TMT validation: 15/20 customers told specific stories about needing to cancel).

## Target Users
Primary: Online shoppers who place orders and change their mind within 30 minutes
Secondary: Customer support agents who currently handle cancellations manually

## Desired Outcome
Reduce support tickets related to order cancellation by 80% within 3 months

## Features
P0: Self-service cancellation within 30 min of order placement
- User can cancel from order confirmation page or order history
- Full refund to original payment method
- Confirmation email sent

P1: Self-service cancellation within 24 hours
- Same as P0 but with manual review if order is being processed

P2: Partial cancellation (cancel one item from a multi-item order)

## Success Metrics
- Primary: Self-service cancellation rate > 90% of all cancellations
- Secondary: Support ticket reduction for cancellations by 80%
- Counter-metric: Accidental cancellation rate < 1%

## Out of Scope (v1)
- Partial cancellation
- Cancellation after shipment
- Subscription order cancellation

## Release Criteria
- All P0 features tested and passing
- 95% test coverage for cancellation flow
- Latency: cancellation API responds < 200ms p95
```
