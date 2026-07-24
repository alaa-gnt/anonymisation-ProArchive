---
name: product-discovery
description: Identify and validate what product to build by understanding customer problems, testing riskiest assumptions, and aligning with business strategy.
---

# product-discovery

## 1. Skill name
Product Discovery

## 2. One-line purpose
Identify and validate what product to build by understanding customer problems, testing riskiest assumptions, and aligning with business strategy.

## 3. When to use this skill
- Before starting a new product or feature development
- When the team is unsure what to build next
- When there are multiple competing ideas and no clear winner
- When you need to reduce risk before committing engineering resources
- When customer feedback contradicts internal assumptions

## 4. When not to use this skill
- When the problem and solution are already well-understood (optimization phase)
- When the team is in delivery mode on a validated product
- When the decision is purely technical with no customer impact

## 5. Core principles
- **Discovery is separate from delivery**: Discovery explores what to build; delivery builds it. Both are needed, but they have different rhythms and methods (Inspired Ch.6).
- **The goal is to reduce risks, not to confirm ideas**: The four risks are value risk (will they buy?), usability risk (can they use it?), feasibility risk (can we build it?), and business viability risk (does it work for the business?) (Inspired Ch.6).
- **Customer problems, not solutions**: Stay in the problem space until the problem is well-understood. Premature solutioning is the most common mistake (Inspired Ch.4, TMT Ch.1).
- **Test the riskiest assumption first**: Identify which assumption, if wrong, kills the idea. Test that one first (Inspired Ch.7).
- **Don't ask, observe**: Customers don't always know what they want. Observe their actual behavior. What they do is more reliable than what they say (TMT Ch.1, Inspired Ch.4).
- **The Mom Test applies to all customer conversations**: Don't pitch, don't ask hypotheticals, ask about past behavior, look for commitment signals (TMT Ch.1).
- **Outcomes over output**: The goal is to achieve a desired outcome (customer behavior change), not to ship features (Inspired Ch.5, LS Ch.3).
- **Discovery is continuous, not a phase**: Even after launch, you should continuously discover new opportunities and validate assumptions (Inspired Ch.6, LS Ch.7).
- **Customer segments and jobs-to-be-done**: Different segments hire products to do different jobs. Understand the job before designing the product (Inspired Ch.3).
- **Prototypes are the language of discovery**: Low-fidelity prototypes (sketches, wireframes, clickable mockups) let you test usability and value without building the product (Inspired Ch.8).

## 6. Step-by-step method

### Step 1: Identify the problem
- Start with the product vision or business objective
- Identify the customer segment and the job-to-be-done (Inspired Ch.3)
- Conduct problem interviews (not solution interviews) using The Mom Test techniques (TMT Ch.1-2):
  - Ask about current behavior: "How do you handle X today?"
  - Ask about history: "When was the last time you encountered X?"
  - Ask about frequency: "How often does X happen?"
  - Ask about impact: "What does it cost you (time, money, frustration) when X happens?"
- Look for emotional signals: frustration, excitement, resignation
- Determine if the problem is active (they are actively trying to solve it) or passive (they wish it were solved but aren't doing anything about it)

### Step 2: Map the risks
- List all assumptions underlying the idea (Inspired Ch.7):
  - *Value risk*: Will customers buy or use this?
  - *Usability risk*: Can customers figure out how to use this?
  - *Feasibility risk*: Can our engineers build this?
  - *Business viability risk*: Does this work for our business model?
- Rank the assumptions by two dimensions: how critical they are (if wrong, does the idea die?) and how uncertain they are (how confident are we?)
- Identify the riskiest assumption: the one that is both critical AND uncertain (Inspired Ch.7)

### Step 3: Design discovery experiments
- For the riskiest assumption, design an experiment that tests it with minimal effort (Inspired Ch.8):
  - *Value risk test*: Fake door / smoke test (landing page, "Buy now" button), prototype demo, concierge MVP
  - *Usability risk test*: Clickable prototype with user observation, paper prototype, usability testing
  - *Feasibility risk test*: Technical spike / proof-of-concept
  - *Business viability risk test*: Pricing tests, cost analysis, partnership discussions
- Define the success criteria BEFORE running the experiment
- Use prototypes (low-fi or hi-fi) to test value and usability without building the real product

### Step 4: Run customer discovery conversations
- Find 5-10 target customers (not friends, not the CEO's golf buddies) (TMT Ch.3)
- Use a structured interview guide, but be prepared to follow interesting tangents
- Observe, don't pitch. If you find yourself pitching, stop and ask a question (TMT Ch.1)
- Listen for:
  - Stories about past behavior (the gold)
  - Emotional reactions to the problem (the signal)
  - Commitment signals (time, money, referral) (TMT Ch.2)
  - Bad data signals (compliments, fluff, hypotheticals) (TMT Ch.2)
- After each conversation, write down what you learned and update your assumptions

### Step 5: Synthesize and decide
- After 5-10 conversations, look for patterns:
  - Is the problem real and frequent enough?
  - Is the customer segment willing to pay?
  - Is there a viable business model?
- If the riskiest assumption is invalidated: pivot (change the assumption) or kill the idea
- If the riskiest assumption holds: test the next riskiest assumption
- If multiple critical assumptions hold: proceed to validate with an MVP (LS Ch.7, Ch.8)

### Step 6: Hand off to delivery
- When the critical risks are resolved, create a product opportunity assessment (Inspired Ch.11)
- Define the MVP scope: the smallest thing that delivers the outcome
- Write user stories or PRD based on validated learning, not speculation
- The delivery team takes it from here, but discovery continues on the next set of assumptions

## 7. Decision rules
- **If 5 customer conversations produce no real problem stories, the problem may not exist** (TMT Ch.2).
- **If customers say the problem exists but are not doing anything about it, it's a passive problem. Not worth solving** (TMT Ch.4).
- **If you cannot find 5 customers in your target segment who agree to a conversation, the segment may be too small or unreachable** (TMT Ch.3).
- **If the MVP would take more than 3 months to build, you haven't reduced risk enough. Do more discovery** (Inspired Ch.7).
- **If the team cannot articulate the riskiest assumption, do more analysis before designing experiments** (Inspired Ch.7).
- **If the customer says "I would pay for that" but can't tell you what they currently spend, they won't** (TMT Ch.2).
- **If a discovery experiment costs more than $1000 or takes more than 2 weeks, it's too expensive. Find a cheaper test** (Inspired Ch.8, LS Ch.6).
- **If the business model doesn't work at scale, the idea may still be worth pursuing as a feature, not a product** (Inspired Ch.11).

## 8. Common mistakes
- Skipping discovery and going straight to building (solution-land) (Inspired Ch.4, TMT Ch.1).
- Confusing a customer's interest with validation. Interest is cheap; commitment is real (TMT Ch.2).
- Asking "Would you use this?" (everyone says yes to be polite) (TMT Ch.1).
- Building a prototype that is too polished, making customers afraid to criticize (TMT Ch.1).
- Talking to the wrong people: friends, family, current customers (if the product is for a new segment) (TMT Ch.3).
- Not defining success criteria before the experiment, so results are always "inconclusive" (LS Ch.7).
- Using discovery as a one-time phase rather than a continuous practice (Inspired Ch.6).
- Ignoring the four risks and only testing one (usually value, but feasibility or viability could kill the idea first) (Inspired Ch.6).
- Discovering the problem but not the business model. If it can't make money, it's a hobby (Inspired Ch.11).
- Not writing down the learning. If you don't capture what you learned, you didn't learn (LS Ch.3).

## 9. Output format
```
## Product Discovery: [Product/Idea Name]

### Problem Statement
- Customer segment:
- Job to be done:
- Current behavior/alternative:
- Pain/frustration:

### Risk Matrix
| Risk | Criticality | Uncertainty | Riskiest? | Experiment |
|------|-------------|-------------|-----------|------------|

### Customer Conversation Summary
| Date | Segment | Key Learnings | Bad Data Signals | Commitment Signals |
|------|---------|---------------|------------------|-------------------|

### Risk Test Results
| Experiment | Hypotheses | Result | Success Criteria Met? | Updated Assumption |
|------------|------------|--------|----------------------|-------------------|

### Decision
- [ ] Proceed to MVP
- [ ] Pivot: [change]
- [ ] Kill

### Next Steps
- MVP scope (if proceeding):
- Next risk to test (if continuing discovery):
```

## 10. Quality checklist
- [ ] Problem is validated through customer conversations (not assumptions)
- [ ] Customer segment is specific and reachable
- [ ] Four risks (value, usability, feasibility, viability) are mapped
- [ ] Riskiest assumption is identified
- [ ] Experiment tests the riskiest assumption, not the easiest one
- [ ] Success criteria were defined before the experiment
- [ ] Customer conversations used Mom Test techniques (no pitching, no hypotheticals)
- [ ] Commitment signals were observed (not just interest)
- [ ] Decision is based on evidence, not opinion
- [ ] Next steps are clear and actionable

## 11. Source books used
- Primary: The Mom Test (Fitzpatrick)
- Support: The Lean Startup (Ries), Inspired (Cagan), Good Strategy Bad Strategy (Rumelt)

## 12. Notes on how the books complement each other
TMT provides the conversation methodology for discovering real customer problems. LS provides the experimental framework (Build-Measure-Learn, MVP, validated learning). Inspired adds the product manager's toolkit: the four risks, the discovery-delivery split, prototypes, and the product opportunity assessment. GSBS adds the strategic lens: making sure the product is aligned with a coherent strategy, not just building features. Together they form a complete product discovery methodology: talk to customers, test assumptions, align with strategy, and then build.
