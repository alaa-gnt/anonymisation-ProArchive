---
name: roadmap-drafting
description: Draft a product roadmap that aligns with strategy, prioritizes outcomes over output, communicates what will be built (and what won't), and adapts as learning happens.
---

# roadmap-drafting

## 1. Work skill name
Roadmap Drafting

## 2. Job to be done
Draft a product roadmap that aligns with strategy, prioritizes outcomes over output, communicates what will be built (and what won't), and adapts as learning happens.

## 3. Trigger or use case
- A new product or quarter needs a roadmap
- The team is deciding what to work on next
- Stakeholders want visibility into upcoming work
- The current roadmap is unrealistic or unfocused
- The team needs to say "no" to feature requests and needs a framework

## 4. Required inputs
- Product vision and strategy (Inspired Ch.2, GSBS Ch.1)
- Customer discovery findings (TMT Ch.1-2)
- Business goals and OKRs
- Current product performance data
- Team capacity and constraints
- Known technical debt or infrastructure needs

## 5. Step-by-step workflow

### Step 1: Review the strategy
- Review the product vision: where are we going? (Inspired Ch.2)
- Review the strategy: what is our diagnosis, guiding policy, and coherent actions? (GSBS Ch.1)
- Review the business goals: what outcomes are we trying to achieve this quarter? (Inspired Ch.5)
- If the strategy is unclear, clarify it before drafting the roadmap. The roadmap is downstream of strategy.

### Step 2: Gather inputs
- Customer feedback (support tickets, interviews, surveys)
- Product analytics (usage data, retention, conversion, feature adoption)
- Competitive landscape changes
- Technical constraints and dependencies
- Team capacity (how many engineers, for how long?)

### Step 3: Identify the key outcomes for the period
- What are the most important business outcomes for the next quarter? (Inspired Ch.5)
- What problems must be solved to achieve those outcomes?
- What is the single most important thing to accomplish? (GSBS Ch.6)
- Rank outcomes by: impact (on business goals), confidence (how sure are we?), effort (how hard is it?)

### Step 4: Map outcomes to candidate solutions
- For each outcome, brainstorm possible solutions (features, improvements, experiments)
- Do NOT commit to solutions yet—this is ideation (Inspired Ch.4)
- For each solution, estimate effort (T-shirt sizes: S, M, L, XL)
- For each solution, estimate confidence (C = clear evidence, M = medium, W = weak)
- Prioritize: high impact + high confidence = do first. High impact + low confidence = test first.

### Step 5: Define the roadmap themes
- Group solutions into themes (not a list of features) (Inspired Ch.10)
- Each theme is a problem area or outcome, not a feature: "Improve onboarding" not "Add social login"
- For each theme, define:
  - The outcome it serves
  - The key results (metrics)
  - The timeframe (this quarter, next quarter, future)
  - The level of uncertainty (known vs. needs discovery)

### Step 6: Define NOW, NEXT, LATER
- **NOW**: What we are working on right now (high confidence, high impact, well-understood) (Inspired Ch.10)
- **NEXT**: What we plan to work on after NOW (some confidence, needs more discovery)
- **LATER**: What we are considering but not committing to (exploratory, needs validation)
- This structure communicates priorities without over-committing to future features (GSBS Ch.6)

### Step 7: Review and validate the roadmap
- Is the roadmap aligned with the strategy? (If not, revise)
- Is the roadmap realistic given team capacity? (If NOW is too full, cut)
- Is the roadmap focused? (If there are more than 3 themes in NOW, it's not focused)
- Does the roadmap include discovery work for uncertain items? (If it's all delivery, you're not learning) (Inspired Ch.6)
- Share the roadmap with stakeholders and get feedback

### Step 8: Maintain the roadmap as a living document
- Review the roadmap at the end of each sprint or month
- Move items from NEXT to NOW as they become ready
- Move items from NOW to DONE or DROPPED based on learning
- Update when the strategy changes
- The roadmap is a communication tool, not a contract

## 6. Output deliverable
A product roadmap with: vision and strategy summary, quarterly themes (NOW/NEXT/LATER), outcomes and key results for each theme, discovery vs. delivery split, and capacity allocation.

## 7. Quality checklist
- [ ] Roadmap is aligned with strategy (downstream of strategy, not upstream)
- [ ] Outcomes are prioritized, not features (what we want to achieve, not what we'll build)
- [ ] NOW/NEXT/LATER structure is used
- [ ] NOW contains no more than 3 themes (focused)
- [ ] Discovery items are included alongside delivery items
- [ ] Team capacity is realistically accounted for
- [ ] Each theme has a measurable outcome
- [ ] Roadmap is shared and understood by stakeholders
- [ ] Roadmap is treated as a living document (reviewed monthly)
- [ ] Items that were dropped or postponed are acknowledged

## 8. Common failure modes
- Mistaking the roadmap for the strategy. The roadmap is an output of the strategy, not the strategy itself (Inspired Ch.2, GSBS Ch.1)
- Over-committing: filling NOW with more than the team can deliver (Inspired Ch.10)
- Making the roadmap a wishlist with no prioritization (everything is P0) (GSBS Ch.6)
- Focusing on features instead of outcomes (Inspired Ch.5)
- Not including discovery work: the roadmap should include time for validation and experimentation (Inspired Ch.6)
- Treating the roadmap as a fixed contract: it should evolve as learning happens (LS Ch.7)
- Ignoring technical debt and infrastructure (the roadmap is only features)
- Not communicating what is NOT on the roadmap (stakeholders assume everything will get built)

## 9. Dependencies on framework skills
- Strategy Assessment (to align roadmap with strategy)
- Product Discovery (for customer insights and validation)
- Startup Validation (for testing assumptions on the roadmap)

## 10. Source books used
- Primary: Inspired (Cagan)
- Support: Good Strategy Bad Strategy (Rumelt), The Lean Startup (Ries), Thinking in Systems (Meadows)

## 11. Example of a good final output structure
```
# Product Roadmap: Q3 202X

## Vision
Become the default platform for remote team task management

## Strategy (Q3 Focus)
Increase team activation rate from 40% to 60% by improving first-week user experience

---

## NOW (This Quarter)

### Theme 1: Onboarding Redesign
- Outcome: 60% of new teams create their first task within 24h (currently 35%)
- Approach: Streamlined signup, template-based first project, guided tour
- Delivery: New onboarding flow (S), Template selection (S)
- Discovery: Test "invite team" flow friction (2 user research sessions)

### Theme 2: Team Invite Improvement
- Outcome: Reduce time from signup to team member joining from 2h to 5min
- Approach: Better invite UX, email notifications, magic link
- Delivery: Magic link signup (M), Email notification redesign (S)

---

## NEXT (Next Quarter)

### Theme 3: Notification System
- Outcome: Increase weekly active users by 20%
- Approach: Smart notifications, digest emails, push notifications
- Discovery needed: What notification frequency do users prefer?

### Theme 4: Mobile App v1
- Outcome: Enable task management on mobile (expand TAM)
- Discovery needed: Mobile-specific user research (very uncertain)

---

## LATER (Future)

- Integrations (Slack, Jira, GitHub)
- Premium tier with analytics
- API for third-party developers
```
