---
name: experiment-design
description: Design rigorous experiments (A/B tests, multivariate tests, bandit experiments) to validate hypotheses, optimize ML models, and drive data-informed decisions.
---

# experiment-design

## 1. Skill name
Experiment Design

## 2. One-line purpose
Design rigorous experiments (A/B tests, multivariate tests, bandit experiments) to validate hypotheses, optimize ML models, and drive data-informed decisions.

## 3. When to use this skill
- When deciding whether a new feature, model, or product change improves outcomes
- When optimizing ML models through hyperparameter tuning or feature selection
- When testing multiple treatment variants against a control
- When the cost of a wrong decision is high enough to justify the experiment cost
- When stakeholders disagree on the best approach and data is needed to decide
- When validating that a new ML model outperforms the current one in production

## 4. When not to use this skill
- When the expected effect size is too small to detect with available traffic
- When the experiment would take too long to run given the decision timeline
- When the cost of running the experiment exceeds the expected benefit
- When a qualitative decision (e.g., user feedback, expert review) is sufficient
- When the change is clearly beneficial (fixing a bug, improving security)

## 5. Core principles
- **An experiment tests a hypothesis, not a hunch**: Before running, define the null hypothesis (no effect) and the alternative hypothesis (there is an effect). Both should be specific and measurable (MLDP Ch.5, DMLS Ch.9).
- **A good experiment has an intervention, a control, and a metric**: Without a control group and a pre-defined metric, you cannot interpret the result (MLDP Ch.5, LS Ch.7).
- **Randomization is the foundation**: Random assignment to control and treatment groups ensures that observed differences are caused by the treatment, not by pre-existing differences (MLDP Ch.5).
- **Statistical significance ≠ practical significance**: A p-value < 0.05 tells you the effect is real. It doesn't tell you the effect is big enough to matter. Focus on effect size and practical significance (MLDP Ch.5, DMLS Ch.9).
- **Multiple testing requires correction**: Running 20 metrics and picking the only significant one is p-hacking. Use Bonferroni, Holm-Bonferroni, or FDR correction when testing multiple hypotheses (MLDP Ch.5).
- **The Build-Measure-Learn loop is the experiment cycle**: Build the experiment (variant), measure the results, learn whether to adopt, iterate, or kill (LS Ch.7).
- **Systems thinking prevents unintended consequences**: Before running the experiment, think about what else might change in the system. A local improvement might cause a global degradation (TIS Ch.3, Ch.6).
- **Start with the simplest experiment**: A/B test is the gold standard, but sometimes a pre/post analysis or a phased rollout is sufficient. Match the rigor to the decision (MLDP Ch.5, DMLS Ch.9).
- **Interference between treatment and control (network effects) invalidates results**: If treatment affects control users (e.g., marketplace, social network), use cluster-randomized experiments or switchback experiments (MLDP Ch.5).
- **Pre-register your experiment**: Write down the design, hypothesis, metrics, and analysis plan before running. This prevents p-hacking and confirmation bias (MLDP Ch.5, LS Ch.7).

## 6. Step-by-step method

### Step 1: Define the hypothesis
- State the null hypothesis (H0): "The change has no effect on [metric]"
- State the alternative hypothesis (H1): "The change has a statistically significant effect on [metric]"
- Specify the direction: one-tailed (improvement only) or two-tailed (any change)
- Identify the primary metric: the one metric that will determine the decision (MLDP Ch.5, DMLS Ch.9)
- Identify secondary metrics: other metrics that could be affected (guardrail metrics)
- Guardrail metrics: metrics that must NOT degrade even if the primary metric improves (e.g., latency, error rate)

### Step 2: Design the experiment
- Choose the experiment type (MLDP Ch.5):
  - *A/B test*: one control, one treatment, simple comparison
  - *A/B/n test*: one control, multiple treatments
  - *Multivariate test*: test multiple factors simultaneously with interactions
  - *Switchback*: switch between control and treatment over time (for marketplace, network effects)
  - *Interleaved*: show both control and treatment to the same user (ranking experiments)
  - *Multi-armed bandit*: dynamically allocate traffic to winning variants
- Define the randomization unit: user, session, event, cluster, or time period
- Define the sample size: use power analysis to determine the minimum sample size needed to detect the minimum effect size of interest
- Define the experiment duration: long enough to capture the full effect (primacy, novelty, seasonality)

### Step 3: Calculate sample size
- Determine the minimum effect size worth detecting (MDE): the smallest improvement that would justify the change (MLDP Ch.5)
- Choose the statistical power (usually 80%): probability of detecting the effect if it exists
- Choose the significance level (usually 5%): probability of false positive
- Use the formula or a sample size calculator: larger effects require fewer samples; smaller effects require more
- If the required sample size exceeds available traffic, either lower the effect size expectation or accept a longer experiment

### Step 4: Implement the experiment
- Randomly assign units to control and treatment (DMLS Ch.9)
- Ensure the assignment is stable: a unit should see the same variant consistently
- Implement guardrails: system health monitoring (latency, errors, memory) during the experiment
- Implement logging: log every exposure and every outcome event
- Use feature flags to toggle variants without redeployment

### Step 5: Monitor during the experiment
- Check for sample ratio mismatch (SRM): the expected ratio of control/treatment vs. actual ratio. If they differ, something is wrong (MLDP Ch.5)
- Monitor guardrail metrics: if a guardrail is breached, consider stopping the experiment
- Do NOT peek at the primary metric repeatedly: peeking inflates false positive rates
- If you must monitor, use sequential testing methods that account for continuous monitoring

### Step 6: Analyze the results
- Calculate the primary metric for each group
- Calculate the effect size and confidence interval
- Perform the statistical test (t-test, Mann-Whitney, chi-squared, depending on metric type) (MLDP Ch.5)
- Apply multiple testing correction if analyzing multiple metrics (DMLS Ch.9)
- Check for Simpson's paradox: is the overall effect consistent across segments?
- Check for heterogeneous treatment effects: does the treatment work for some segments but not others?

### Step 7: Decide and take action
- If p < significance level AND effect size > minimum detectable effect: adopt the change
- If p < significance level BUT effect size < MDE: the effect is real but too small to matter. Consider cost vs. benefit
- If p >= significance level: the effect is not statistically significant. Cannot conclude the change improves the metric
- If p >= significance level BUT confidence interval includes a large positive effect: you may need more data
- Document the decision: what was tested, what was found, and what was decided
- If adopting: roll out gradually (canary) and continue monitoring (DMLS Ch.6, Ch.9)

## 7. Decision rules
- **If the required sample size exceeds 4 weeks of traffic at current volume, either accept a larger effect size or skip the experiment** (DMLS Ch.9).
- **If the experiment involves network effects (marketplace, social), use cluster-randomized or switchback experiments** (MLDP Ch.5).
- **If the primary metric is a ratio (e.g., conversion rate), use a proportion test; if it's a continuous metric (e.g., revenue), use a t-test**.
- **If more than 5% of units are exposed to both control and treatment (cross-contamination), the experiment is invalid** (MLDP Ch.5).
- **If the sample ratio between control and treatment differs from expected by more than 1%, investigate SRM** (MLDP Ch.5).
- **If multiple metrics show significance but all have small effect sizes, apply multiple testing correction before declaring success** (MLDP Ch.5).
- **If a secondary metric shows significant degradation, even if the primary metric improves, consider not launching** (guardrail rule).
- **If the novelty effect is likely (new feature seems interesting at first but use declines), extend the experiment duration to capture the steady-state effect**.
- **If the experiment shows no effect but the confidence interval is very wide, the experiment was underpowered. Run a longer experiment or accept the uncertainty**.
- **If the ML model improvement is within the confidence interval of the baseline model, there is no evidence the new model is better** (DMLS Ch.9).

## 8. Common mistakes
- Running the experiment without a clear hypothesis (p-hacking by testing everything) (MLDP Ch.5).
- Stopping the experiment early because the result is "significant" (peeking) (MLDP Ch.5).
- Running multiple tests and reporting only the significant ones (publication bias).
- Ignoring sample ratio mismatch (SRM) which indicates implementation issues (MLDP Ch.5).
- Using the wrong randomization unit (user-level treatment but session-level metrics).
- Assuming the effect is linear over time (seasonality, weekday effects).
- Not logging exposures, so you cannot exclude noisy sessions or analyze non-responses.
- Running an experiment without guardrail metrics (launch kills latency → users leave → metric improves due to selection bias).
- Confusing statistical significance with practical significance (p < 0.05 but effect is tiny) (MLDP Ch.5).
- Not considering interference between control and treatment groups (network effects) (MLDP Ch.5).
- Ignoring system dynamics: an experiment that improves one metric might degrade another (TIS Ch.3).

## 9. Output format
```
## Experiment Design: [Experiment Name]

### Hypothesis
- Null hypothesis (H0):
- Alternative hypothesis (H1):
- Primary metric:
- Guardrail metrics:

### Design
- Experiment type:
- Randomization unit:
- Sample size (required):
- Duration:

### Implementation
- Treatment description:
- Control description:
- Feature flag:
- Logging plan:

### Analysis Plan
- Statistical test:
- Significance level:
- Multiple testing correction:
- Segment analysis:

### Decision Criteria
- Adopt if:
- Reject if:
- Inconclusive if:
```

## 10. Quality checklist
- [ ] Hypothesis is specific, falsifiable, and pre-registered
- [ ] Primary metric is defined (not asking "did something change?")
- [ ] Guardrail metrics are defined (what must NOT degrade)
- [ ] Sample size is calculated (power analysis)
- [ ] Randomization unit matches the treatment scope
- [ ] Experiment duration accounts for novelty and seasonality
- [ ] Multiple testing correction is planned
- [ ] Sample ratio mismatch (SRM) is checked
- [ ] Decision criteria are defined before results are known
- [ ] Analysis plan is pre-registered (no p-hacking)

## 11. Source books used
- Primary: Machine Learning Design Patterns (Lakshmanan, Robinson, Munn)
- Support: Designing Machine Learning Systems (Huyen), The Lean Startup (Ries), Thinking in Systems (Meadows)

## 12. Notes on how the books complement each other
MLDP provides the rigorous experimental design framework: hypothesis testing, sample size calculation, SRM detection, multiple testing correction, and network effects handling. DMLS adds the ML-specific considerations: A/B testing for model comparison, evaluating offline metrics vs. online metrics, and deployment strategies. LS provides the Build-Measure-Learn cycle and the concept of validated learning—the broader business context for experiments. TIS adds the systems perspective: anticipating unintended consequences and understanding that a local improvement may create global problems. Together they form a complete experiment methodology from hypothesis through design, execution, analysis, and decision.
