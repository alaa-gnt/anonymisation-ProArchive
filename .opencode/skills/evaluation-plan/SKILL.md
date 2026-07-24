---
name: evaluation-plan
description: Design a plan to evaluate an ML model's performance both offline (before deployment) and online (in production), covering metrics, validation strategy, and monitoring.
---

# evaluation-plan

## 1. Work skill name
Evaluation Plan

## 2. Job to be done
Design a plan to evaluate an ML model's performance both offline (before deployment) and online (in production), covering metrics, validation strategy, and monitoring.

## 3. Trigger or use case
- An ML model is being developed and needs to be evaluated before deployment
- A model in production needs its performance assessed for potential degradation
- A new model version needs to be compared against the current production model
- A model's business impact needs to be measured (does the model actually improve the business outcome?)

## 4. Required inputs
- Model objectives: what the model predicts, what business outcome it serves
- Training data: source, distribution, labels
- Evaluation data: holdout set, validation set, or production data with labels
- Current baseline or production model performance
- Business metrics and success criteria

## 5. Step-by-step workflow

### Step 1: Define the evaluation goals
- What are we trying to measure? (DMLS Ch.9):
  - *Predictive performance*: accuracy, precision, recall, RMSE, etc.
  - *Business impact*: revenue increase, cost reduction, user engagement
  - *Operational performance*: latency, throughput, resource usage
- Define the success criteria: what performance must be met for the model to be deployable?
- Define the minimum bar: below this, the model is not worth deploying

### Step 2: Design offline evaluation
- Split data into training, validation, and holdout test sets (MLDP Ch.5)
- Use appropriate validation strategy:
  - Random split for i.i.d. data
  - Time-based split for time-series data
  - Stratified split for imbalanced data
  - Group split to avoid data leakage (same user in train and test)
- Choose metrics that match the business objective:
  - Classification: precision, recall, F1, AUC-ROC, AUC-PR, confusion matrix
  - Regression: RMSE, MAE, MAPE, R-squared
  - Ranking: NDCG, MAP, MRR
  - Recommendation: precision@k, recall@k, coverage, diversity
- Evaluate on slices: does the model perform well for all customer segments? (DMLS Ch.5)

### Step 3: Check for data leakage
- Ensure no leakage from future into past (time-series)
- Ensure no leakage between train and test (proper splits)
- Ensure no feature leakage (features that won't be available at prediction time)
- Document all potential leakage sources and how they were prevented (MLDP Ch.5)

### Step 4: Compare against baselines
- Compare against: heuristic baseline, previous model version, simple linear model (DMLS Ch.3)
- Use statistical significance tests (t-test, McNemar's test, permutation test) (MLDP Ch.5)
- Report confidence intervals, not just point estimates
- If the new model is not statistically significantly better than the baseline, don't deploy it

### Step 5: Design online evaluation (A/B test)
- Design the A/B test (see Experiment Design skill): control = current model, treatment = new model
- Define the primary online metric (business metric, not just model metric) (DMLS Ch.9)
- Define guardrail metrics: what must NOT degrade (latency, error rate, other model metrics)
- Calculate required sample size and duration
- Plan for canary deployment: 1% → 10% → 50% → 100% (DMLS Ch.6)

### Step 6: Plan monitoring for drift and degradation
- Define drift detection for:
  - *Feature drift*: distribution change in input features (DMLS Ch.8)
  - *Label drift*: distribution change in ground truth labels
  - *Prediction drift*: distribution change in model outputs
- Set alert thresholds for each drift metric
- Plan for ground truth collection: how will we get labels in production?
- Plan for performance monitoring: when labels arrive, compute model metrics vs. ground truth (DMLS Ch.9)

### Step 7: Document the evaluation results
- For offline evaluation: metrics on holdout set, sliced analysis, comparison to baseline, limitations
- For online evaluation: A/B test results, business impact, guardrail metrics, statistical significance
- Decision: deploy, reject, or iterate

## 6. Output deliverable
An evaluation plan document with: offline evaluation metrics and results, baseline comparison, A/B test design, drift monitoring plan, and deployment decision.

## 7. Quality checklist
- [ ] Evaluation metrics match the business objective
- [ ] Data split strategy prevents leakage
- [ ] Baselines are established (heuristic and/or current model)
- [ ] Statistical significance is reported (not just point estimates)
- [ ] Sliced analysis checks for disparate performance
- [ ] A/B test design includes guardrail metrics
- [ ] Drift monitoring is planned (feature, label, prediction)
- [ ] Ground truth collection plan exists for production monitoring
- [ ] Success criteria are defined before evaluation starts
- [ ] Deployment decision criteria are pre-defined

## 8. Common failure modes
- Optimizing for the wrong metric (model metric improves but business metric doesn't) (DMLS Ch.9)
- Data leakage in train/test split (model looks great offline, fails in production) (MLDP Ch.5)
- Not comparing against a simple baseline (DMLS Ch.3)
- Not slicing the evaluation (model works for majority but fails for minority segment) (DMLS Ch.5)
- A/B test is underpowered (cannot detect the effect size of interest) (MLDP Ch.5)
- No drift monitoring (model degrades silently after deployment) (DMLS Ch.8)
- Confusing offline metrics with online impact (99% accuracy offline doesn't mean 99% user satisfaction) (DMLS Ch.9)
- Not testing the evaluation pipeline (the metrics computation has bugs)

## 9. Dependencies on framework skills
- Experiment Design (for A/B test methodology)
- ML System Design (for deployment and monitoring infrastructure)
- Systems Thinking (for understanding feedback loops)

## 10. Source books used
- Primary: Designing Machine Learning Systems (Huyen)
- Support: Machine Learning Design Patterns (Lakshmanan et al.), Thinking in Systems (Meadows), The Lean Startup (Ries)

## 11. Example of a good final output structure
```
# Evaluation Plan: Fraud Detection Model v2

## Offline Evaluation
- Test set: 100K transactions (time-based split: last 2 weeks of training data)
- Metrics: Precision (target: >90%), Recall (target: >80%), F1 (target: >85%)
- Baseline (v1): Precision 85%, Recall 72%, F1 78%
- v2 result: Precision 91%, Recall 83%, F1 87% (p<0.01, McNemar's test)
- Sliced analysis: performance is similar across all transaction amount segments

## A/B Test Design
- Control: v1 model (100% traffic)
- Treatment: v2 model (ramp: 1% -> 10% -> 50%)
- Primary metric: fraud detection rate (increase)
- Guardrail: false positive rate (must not increase), latency (+ < 50ms)
- Duration: 2 weeks at 50% traffic

## Drift Monitoring
- Feature drift: daily KS-test on feature distributions, alert if p<0.01
- Prediction drift: weekly comparison of prediction distribution
- Label drift: monthly comparison of ground truth labels

## Deployment Decision
- Go: if A/B test shows statistically significant improvement at 50% with no guardrail violations
- No-go: if no improvement or guardrails breached
```
