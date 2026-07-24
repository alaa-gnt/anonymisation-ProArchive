---
name: systems-thinking
description: Understand complex systems by mapping stocks, flows, feedback loops, and delays to identify leverage points and avoid unintended consequences.
---

# systems-thinking

## 1. Skill name
Systems Thinking

## 2. One-line purpose
Understand complex systems by mapping stocks, flows, feedback loops, and delays to identify leverage points and avoid unintended consequences.

## 3. When to use this skill
- When analyzing a problem that persists despite repeated attempts to fix it
- When designing policies, incentives, or interventions that affect a complex system
- When the same problem keeps recurring in different forms
- When the team cannot agree on the root cause of a problem
- When planning a major change that will affect multiple parts of the system

## 4. When not to use this skill
- For simple, linear problems with clear cause and effect (e.g., a bug in code)
- When immediate action is required and the analysis would delay response
- For problems that are well-understood and have straightforward solutions

## 5. Core principles
- **The system produces its own behavior**: When you see a problem, resist the urge to blame individuals. Look at the system structure that produced the behavior (TIS Ch.3).
- **Stocks are the foundation**: Stocks are accumulations (money, inventory, trust, team morale). They change slowly and buffer the system. Understanding stocks is the first step (TIS Ch.1).
- **Flows change stocks over time**: Inflows increase stocks; outflows decrease them. The behavior of a system is determined by the pattern of flows (TIS Ch.1).
- **Feedback loops drive dynamics**: Reinforcing loops amplify change (growth, collapse). Balancing loops resist change and maintain stability (TIS Ch.1).
- **Delays create oscillation**: When there is a significant delay between action and response, the system will overshoot and correct, producing cycles (TIS Ch.2).
- **Non-linearity is everywhere**: Doubling the input rarely doubles the output. There are thresholds, tipping points, and diminishing returns (TIS Ch.2).
- **Leverage points are counter-intuitive**: The most effective intervention is often the least obvious. Pushing harder usually doesn't work (TIS Ch.6).
- **The goal of analysis is not prediction, but insight**: You cannot predict complex systems. The goal is to understand the structure so you can anticipate behavior (TIS Ch.1).
- **Bounded rationality**: People act based on the information available to them, which is always incomplete. If the system creates bad information, it creates bad decisions (TIS Ch.4).
- **Strategy must account for system dynamics**: A good strategy identifies the feedback loops and leverage points that determine whether the strategy will succeed (GSBS Ch.1, TIS Ch.6).
- **Experimentation is the only way to learn in complex systems**: You cannot model everything. Run small experiments, observe the results, and adjust (LS Ch.7, TIS Ch.6).

## 6. Step-by-step method

### Step 1: Define the system boundary
- What is the system you are analyzing? (A company, a market, a product, a team, a data pipeline)
- What is the problem you are trying to solve? Be specific: "Inventory is always too high or too low" not "operations are broken"
- What is the time horizon? (Days, months, years? Different dynamics emerge at different time scales)
- What is outside the system boundary? (External factors you won't model but should acknowledge)

### Step 2: Identify the stocks and flows
- **Stocks** are quantities that accumulate over time:
  - Tangible: cash, inventory, users, servers, bugs
  - Intangible: trust, morale, brand, expertise, technical debt
- **Flows** change stocks over time:
  - Inflows: revenue, new users, new features, new hires
  - Outflows: expenses, churned users, deprecated features, departures
- Draw a stock-and-flow diagram: boxes for stocks, arrows for flows, faucets/taps to control flows

### Step 3: Identify feedback loops
- **Reinforcing loops (R)**: Drive growth or collapse (TIS Ch.1)
  - Example: More users → more content → more value → more users
  - Example: Less trust → less communication → more mistakes → less trust
  - Label as R and describe the direction (R1: viral growth, R2: trust erosion)
- **Balancing loops (B)**: Resist change and maintain equilibrium (TIS Ch.1)
  - Example: Temperature rises → thermostat turns on cooling → temperature drops
  - Example: Inventory too high → reduce ordering → inventory normalizes
  - Label as B and describe the goal (B1: inventory target, B2: quality standard)
- For each loop, identify: what stock is changing, what drives the change, what resists the change

### Step 4: Identify delays
- Where is there a delay between an action and its effect? (TIS Ch.2)
- Common delays in software/startup contexts:
  - Development delay: build → ship → user feedback (weeks to months)
  - Hiring delay: post → interview → hire → productive (months)
  - Technical debt delay: shortcut → complexity → slowdown (months to years)
  - Market response delay: price change → customer response (weeks to months)
- For each delay, estimate the duration and describe what happens during the delay

### Step 5: Map the system dynamics
- Combine stocks, flows, loops, and delays into a causal loop diagram
- Identify the dominant loop at any given time (which loop is driving behavior right now?)
- Identify potential shifts in dominance (when does the balancing loop take over from the reinforcing loop?)
- Example: A startup grows via a reinforcing loop (more users → more referrals → more users) until the market saturates, then a balancing loop dominates (no new users → growth stops)

### Step 6: Identify leverage points
- Rank the interventions from least to most effective (TIS Ch.6):
  1. Change numbers/parameters (e.g., lower interest rates, increase ad spend) — least effective
  2. Change the size of buffers (e.g., increase inventory)
  3. Change the structure of stocks and flows (e.g., add a new pipeline)
  4. Change the length of delays (e.g., reduce cycle time)
  5. Change the strength of feedback loops (e.g., amplify reinforcing loop)
  6. Change the rules of the system (e.g., change pricing, incentives)
  7. Change the structure of information flows (e.g., provide real-time metrics)
  8. Change the goals of the system (e.g., shift from growth to profitability)
  9. Change the paradigm / mindset — most effective
- For each potential intervention, ask: "What will happen next?" (anticipate unintended consequences)

### Step 7: Design interventions
- Choose interventions at higher leverage points (paradigm, goals, information flows) over lower ones (parameters, buffers)
- Design small experiments to test your understanding of the system (LS Ch.7)
- Monitor for unintended consequences: when you push on a system, it pushes back
- Be prepared to adjust: you will never understand the system completely

## 7. Decision rules
- **If a problem persists despite repeated efforts to fix it, there is a systemic cause. Look for feedback loops that are maintaining the problem** (TIS Ch.3).
- **If there is a significant delay between action and outcome, the system will oscillate. Do not over-correct during the delay** (TIS Ch.2).
- **If you cannot find the leverage point, you probably haven't mapped the system thoroughly enough** (TIS Ch.6).
- **If the intervention is at a low leverage point (changing numbers, parameters), expect small, temporary effects** (TIS Ch.6).
- **If the intervention is at a high leverage point (goals, paradigms), expect resistance from the system** (TIS Ch.6).
- **If the system is producing undesirable behavior, first check the information flows: are people acting on incomplete or incorrect information?** (TIS Ch.4).
- **If you are pushing harder on a balancing loop, stop. You are fighting the system. Change the loop instead** (TIS Ch.3).
- **If the strategy ignores system dynamics, the strategy will fail in execution** (GSBS Ch.1, TIS Ch.3).
- **If you need to change behavior, change the structure, not the people. The structure determines behavior** (TIS Ch.3).

## 8. Common mistakes
- Blaming individuals for failures caused by system structure (TIS Ch.3).
- Pushing harder on a balancing loop (e.g., demanding more output when the system is already at capacity) (TIS Ch.3).
- Ignoring delays and over-correcting: raising prices when demand is temporarily low, then lowering them when demand recovers (TIS Ch.2).
- Choosing low-leverage interventions because they are easy (e.g., adding more people to a late project) (TIS Ch.6, GSBS Ch.6).
- Focusing on events (what happened) instead of patterns and system structure (why it keeps happening) (TIS Ch.1).
- Assuming linear relationships: doubling inputs does not double outputs (TIS Ch.2).
- Not defining the system boundary: analyzing too broadly (paralysis) or too narrowly (missing key dynamics) (TIS Ch.1).
- Creating a model and believing it is reality: all models are wrong; some are useful (TIS Ch.1).
- Forgetting that the system includes people with bounded rationality (TIS Ch.4).
- Expecting the system to behave the same way tomorrow as it does today (TIS Ch.1).

## 9. Output format
```
## Systems Analysis: [Problem/System Name]

### System Boundary
- What is included:
- What is excluded:
- Time horizon:
- The problem:

### Stock and Flow Diagram
[Diagram: boxes for stocks, arrows for flows, labels for rates]

### Stock Inventory
| Stock | Current Level | Inflow(s) | Outflow(s) | Notes |
|-------|--------------|------------|------------|-------|

### Feedback Loops
| Loop ID | Type (R/B) | Description | Dominant? |
|---------|------------|-------------|-----------|

### Delays
| Delay | Between | Duration | Effect |
|-------|---------|----------|--------|

### Leverage Points
| Point | Intervention | Leverage (1-10) | Effort (1-10) | Recommendation |
|-------|-------------|------------------|---------------|----------------|

### Intervention Plan
| Action | Expected Effect | Risk of Unintended Consequence | Experiment |
|--------|----------------|-------------------------------|------------|
```

## 10. Quality checklist
- [ ] System boundary is defined (what's in, what's out)
- [ ] Stocks and flows are identified and mapped
- [ ] Feedback loops (reinforcing and balancing) are identified
- [ ] Delays are identified with estimated duration
- [ ] Dominant loop at current time is identified
- [ ] Leverage points are ranked by effectiveness
- [ ] Interventions target higher leverage points
- [ ] Unintended consequences are considered
- [ ] Intervention is designed as an experiment with monitoring
- [ ] Analysis avoids blaming individuals for system-caused problems

## 11. Source books used
- Primary: Thinking in Systems (Meadows)
- Support: Good Strategy Bad Strategy (Rumelt), The Lean Startup (Ries)

## 12. Notes on how the books complement each other
TIS provides the foundational framework for understanding complex systems: stocks, flows, feedback loops, delays, leverage points, bounded rationality. It equips the analyst to see the structure behind recurrent problems. GSBS adds the strategy layer: how to translate systems analysis into a coherent strategy with diagnosis, policy, and actions. The GSBS emphasis on identifying the critical challenge aligns with TIS's leverage point analysis. LS adds the experimental methodology: since we cannot fully understand complex systems, we must learn through iterative experimentation. Together they form a complete approach: understand the system, design a strategy, test it through experiments, and adapt.
