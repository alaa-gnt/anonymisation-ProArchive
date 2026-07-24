---
name: mvp-definition
description: Define the Minimum Viable Product scope: the smallest set of features that can be shipped to start the Build-Measure-Learn cycle and validate the riskiest assumptions.
---

# mvp-definition

## 1. Work skill name
MVP Definition

## 2. Job to be done
Define the Minimum Viable Product scope: the smallest set of features that can be shipped to start the Build-Measure-Learn cycle and validate the riskiest assumptions.

## 3. Trigger or use case
- A new product idea has been validated through customer conversations and needs its first release scope
- The team has a long list of features and needs to prioritize the first release
- The team is spending too long building before shipping anything
- Stakeholders keep adding features to the first release, delaying it

## 4. Required inputs
- Validated problem statement (customer segment, job-to-be-done, pain level)
- Customer conversation summaries (The Mom Test results)
- Risk matrix: which assumptions are the riskiest?
- List of all desired features (brainstormed)
- Constraints: timeline, budget, team size, technology

## 5. Step-by-step workflow

### Step 1: Restate the problem and assumptions
- Review the validated problem: who is the customer, what is the job-to-be-done, what is the pain? (TMT Ch.1-2, Inspired Ch.3)
- List the leap-of-faith assumptions: what must be true for this product to succeed? (LS Ch.5)
- Identify the riskiest assumption: the one that, if wrong, kills the idea (Inspired Ch.7)
- The MVP tests the riskiest assumption, not all of them

### Step 2: List all possible features
- Brainstorm every feature the product could have (no filtering yet)
- Group features into categories: core functionality, nice-to-have, polish
- For each feature, estimate: effort (small/medium/large) and risk reduction (how much does it help validate the riskiest assumption?)

### Step 3: Apply the MVP filter
- For each feature, ask: "Is this essential for testing our riskiest assumption?" (LS Ch.6)
- If "no", the feature is candidate for post-MVP
- If "yes" but there is a simpler way to achieve the same learning (e.g., manual process, prototype, smoke test), use the simpler way (Inspired Ch.8)
- The MVP is the intersection of: required for learning + minimum possible effort

### Step 4: Define the MVP scope
- List the features that passed the filter
- Define what each feature does at minimum (no frills, no edge cases, no optimizations)
- Define what is explicitly NOT in scope (this is as important as what is in scope) (GSBS Ch.6)
- Define the success criteria: what metrics will tell us whether to pivot or persevere? (LS Ch.7)
- Set a hard deadline: the MVP ships on [date] or features are cut

### Step 5: Validate the MVP scope
- Ask: "If we ship this and the riskiest assumption is wrong, will we know?" If not, the MVP is too small
- Ask: "Is there anything in the MVP that does not help test the riskiest assumption?" If yes, cut it
- Ask: "Is the MVP still shippable?" If the MVP is embarrassing or unusable, it's too small
- Ask: "Could we learn the same thing without building anything?" (smoke test, concierge, Wizard of Oz)

### Step 6: Plan post-MVP learning
- Define what will be tested after the MVP
- List the next set of assumptions to validate
- Define how customer feedback will be collected

## 6. Output deliverable
An MVP definition document with: the core hypothesis being tested, MVP feature list (and explicit exclusions), MVP success criteria, timeline, post-MVP learning plan, and a list of deferred features.

## 7. Quality checklist
- [ ] MVP scope is defined by the riskiest assumption, not by stakeholder wishlist
- [ ] Every feature in the MVP directly helps test the riskiest assumption
- [ ] Exclusions are explicitly documented (what is NOT in the MVP)
- [ ] A simpler test (smoke test, concierge, prototype) is not possible instead of building the MVP
- [ ] Success criteria are defined before shipping
- [ ] MVP is shippable without embarrassment (it solves the core problem for real customers)
- [ ] MVP has a hard deadline; scope is cut to meet it
- [ ] Team agrees on what "done" means for the MVP
- [ ] Post-MVP assumptions are identified for the next cycle
- [ ] Stakeholders agree that post-MVP features are not MVP blockers

## 8. Common failure modes
- Building a "minimum viable product" that is actually a "minimum viable feature set" (it has every feature, but nothing works well) (LS Ch.6)
- Including too many features because "we'll need them eventually" (scope creep) (GSBS Ch.6)
- Including too few features that the product is unusable (MVP is useless) (LS Ch.6)
- Not defining success criteria, so the MVP's results are always "inconclusive" (LS Ch.7)
- Building the MVP without validating the problem first (LS Ch.5, TMT Ch.2)
- Letting stakeholders add features to the MVP without cutting other features (scope creep)
- Treating the MVP as the final product instead of a learning experiment (LS Ch.7)
- Building the MVP for the wrong customer segment (TMT Ch.3)
- Not setting a hard deadline (the MVP takes 6+ months to build) (LS Ch.6)
- Confusing an MVP with a prototype: an MVP is a real product for real customers, not a demo

## 9. Dependencies on framework skills
- Startup Validation (to identify the riskiest assumption)
- Product Discovery (to validate the problem before defining the MVP)
- Strategy Assessment (to ensure MVP aligns with strategy)

## 10. Source books used
- Primary: The Mom Test (Fitzpatrick)
- Support: The Lean Startup (Ries), Inspired (Cagan), Good Strategy Bad Strategy (Rumelt)

## 11. Example of a good final output structure
```
# MVP Definition: Task Manager for Remote Teams

## Core Hypothesis
Remote teams struggle to track task progress across time zones. If we build a simple shared task list with status updates, teams will use it daily.

## Riskiest Assumption
Teams will adopt a new tool for task tracking even though they already use Slack/email/Jira.

## MVP Scope (shippable in 4 weeks)
- Create a shared task list (title, status: todo/doing/done, assignee)
- Add and update tasks in real-time
- View tasks by status column

## Explicitly NOT in MVP
- Attachments, comments, due dates, notifications, integrations, mobile app
- User roles and permissions (all users are admins)
- Search, filters, reporting

## Success Criteria
- 10 teams sign up within 2 weeks of launch
- 5 teams have created >20 tasks within 2 weeks
- 3 teams return to use the app in week 3

## Deferred Features
- Attachments (post-MVP, if teams request it)
- Notifications (post-MVP, if retention is an issue)
- Integration with Slack (post-MVP, if adoption is slow)
```
