---
name: ml-system-design
description: Design machine learning systems that are reliable, scalable, maintainable, and aligned with business objectives throughout the ML lifecycle.
---

# ml-system-design

## 1. Skill name
ML System Design

## 2. One-line purpose
Design machine learning systems that are reliable, scalable, maintainable, and aligned with business objectives throughout the ML lifecycle.

## 3. When to use this skill
- When designing a new ML-powered feature or product
- When evaluating whether ML is the right approach for a problem
- When reviewing an existing ML system for production readiness
- When planning the data infrastructure needed for ML
- When estimating the full cost of an ML project (data, compute, people, maintenance)

## 4. When not to use this skill
- For simple rule-based problems that don't need ML
- For one-time analytics or research with no production deployment
- When the cost of ML (data collection, labeling, infra, monitoring) exceeds the benefit
- When heuristic or rules-based solutions would work equally well

## 5. Core principles
- **ML is not magic, it's software engineering with uncertainty**: ML systems have the same reliability, scalability, and maintainability requirements as traditional systems, plus additional concerns around data management and model behavior (DMLS Ch.1).
- **Start with a simple baseline**: Before building a complex ML model, establish a simple heuristic or linear baseline. If the baseline is good enough, you don't need ML. If it's not, the baseline provides a comparison point (DMLS Ch.3, MLDP Ch.1).
- **Data is the most important component**: The ML system is only as good as the data feeding it. Invest in data quality, data infrastructure, and data lineage before optimizing models (DMLS Ch.2, Ch.4, FDE Ch.5).
- **The ML lifecycle is iterative, not linear**: You will go back and forth between data collection, feature engineering, model training, deployment, and monitoring many times (DMLS Ch.1).
- **Feature engineering is the hardest part**: Features encode domain knowledge. Good features make simple models work; bad features make complex models fail (DMLS Ch.4, MLDP Ch.4).
- **Model performance ≠ business impact**: A model with 99% accuracy is useless if it doesn't drive the desired business outcome. Define business metrics first, then map them to model metrics (DMLS Ch.9).
- **Training-serving skew is the most common failure mode**: The data used during training must match the data seen during serving. Detect and monitor for skew (DMLS Ch.6, MLDP Ch.10).
- **Monitor everything, not just the model**: Monitor data quality, feature distributions, prediction distributions, model performance, and system health. Any of these can degrade silently (DMLS Ch.7, Ch.8).
- **Reproducibility is critical**: Track data versions, code versions, model parameters, and training environment. Without reproducibility, you cannot debug production issues (DMLS Ch.1, Ch.7).
- **ML infrastructure is a data engineering problem**: The data pipeline is as important as the model. Invest in data engineering (FDE Ch.1, Ch.3, DMLS Ch.2).
- **Design patterns encode best practices**: Use proven patterns like transformation, repeatable splitting, explainable predictions, and cascade models where appropriate (MLDP Ch.1-4).

## 6. Step-by-step method

### Step 1: Frame the ML problem
- Define the business objective: what outcome are we trying to improve? (DMLS Ch.1)
- Define the ML objective: what will the model predict? (classification, regression, ranking, recommendation, etc.)
- Map the ML objective to the business objective: how will improving the model metric improve the business metric?
- Define success criteria for both business and ML metrics
- If the ML objective cannot be clearly mapped to the business objective, reconsider whether ML is the right approach

### Step 2: Establish a baseline
- Implement a simple heuristic rule (most common class, average value, business rule) (DMLS Ch.3)
- Implement a simple linear model (logistic regression, linear regression)
- If the baseline meets the success criteria, ship the baseline and skip ML
- If the baseline doesn't meet the criteria, use it as a comparison point for ML models

### Step 3: Assess data availability and quality
- Do we have the data to solve this problem? (DMLS Ch.2)
- What data sources are available? (internal databases, logs, third-party APIs, user-generated data)
- Do we need labeled data? If so, how will we get labels? (manual labeling, natural labels, weak supervision) (DMLS Ch.3)
- Assess data quality: missing values, inconsistencies, outliers, label noise, sampling bias (DMLS Ch.4, FDE Ch.5)
- Estimate the data volume and velocity needed
- If data is insufficient, plan data collection before model development

### Step 4: Design the feature engineering pipeline
- Identify raw data sources and plan feature extraction (DMLS Ch.4, MLDP Ch.4)
- Apply feature engineering patterns: embedding, cross-features, feature crossing, feature hashing, feature selection (MLDP Ch.4)
- Design the feature computation pipeline: batch vs. streaming features, feature store considerations (DMLS Ch.4, FDE Ch.5)
- Plan for feature validation: schema checks, distribution checks, drift detection (DMLS Ch.7)
- Use feature stores to share features across models and ensure consistency between training and serving (MLDP Ch.9)

### Step 5: Design the model architecture
- Select the model type based on the problem: linear models for interpretability, tree-based for tabular data, neural networks for unstructured data (DMLS Ch.5)
- Use ML design patterns where applicable (MLDP):
  - *Cascading*: chain models where one model's output is another's input (MLDP Ch.6)
  - *Ensemble*: combine multiple models for better performance (MLDP Ch.6)
  - *Neural Architecture Search*: automate architecture selection (MLDP Ch.2)
  - *Explainable Predictions*: ensure the model can explain its outputs (MLDP Ch.3)
  - *Reusable Transformations*: keep transformations in a shared pipeline (MLDP Ch.1)
- Plan for model training: distributed training, hyperparameter tuning, experiment tracking (DMLS Ch.5)

### Step 6: Design the data pipeline and infrastructure
- Plan the data pipeline: batch or stream (or both) (FDE Ch.3, DDIA Ch.10-11)
- Design the data storage: data lake, data warehouse, feature store (FDE Ch.5)
- Plan for data versioning and lineage: track where each training dataset came from (DMLS Ch.2)
- Design the model training pipeline: orchestration, compute resources, experiment tracking (DMLS Ch.5)
- Plan the deployment infrastructure: model serving, prediction caching, load balancing (DMLS Ch.6)

### Step 7: Plan deployment and monitoring
- Choose the deployment strategy: online (real-time), batch, edge, or hybrid (DMLS Ch.6)
- Plan for canary deployment and rollback: never deploy a new model to 100% of traffic
- Design monitoring:
  - Data quality: nulls, out-of-range, schema violations (DMLS Ch.7)
  - Feature drift: distribution change over time (DMLS Ch.8)
  - Prediction drift: model output distribution change (DMLS Ch.8)
  - Model performance: accuracy, precision, recall (computed when labels are available) (DMLS Ch.9)
  - System health: latency, throughput, error rate, resource utilization (DMLS Ch.7)
- Define alert thresholds and escalation paths for each monitoring signal

### Step 8: Plan for iteration and improvement
- Establish a model retraining cycle: continuous, periodic, or on-demand (DMLS Ch.8)
- Plan for A/B testing: compare model versions in production (DMLS Ch.9)
- Plan for model debugging: if performance degrades, how will you diagnose the root cause?
- Document the system: architecture diagram, data lineage, model card, known limitations

## 7. Decision rules
- **If a simple baseline matches the current best approach, ship the baseline. Don't over-engineer** (DMLS Ch.3).
- **If the data is not available or its quality is unknown, invest in data before models** (DMLS Ch.2).
- **If the training data distribution does not match the production distribution, the model will fail. Measure and fix distribution mismatch first** (DMLS Ch.6, Ch.8).
- **If the feature pipeline differs between training and serving (training-serving skew), the model will fail silently. Make the pipelines identical** (DMLS Ch.6).
- **If the model cannot be monitored in production (no labels, no predictions logged), it should not be deployed** (DMLS Ch.7, Ch.9).
- **If the model needs to explain its predictions (regulated industry, customer-facing), use interpretable models or add explainability layers** (MLDP Ch.3).
- **If the business metric does not improve when the model metric improves, the ML objective is wrong. Re-frame the problem** (DMLS Ch.9).
- **If the cost of acquiring and labeling data exceeds the expected benefit of the model, ML is not the right solution** (DMLS Ch.2).
- **If the infrastructure cost (compute, storage, serving) exceeds the value generated, scale down the model complexity** (DMLS Ch.5).
- **If the team cannot reproduce a model from 3 months ago, the experiment tracking and versioning are insufficient** (DMLS Ch.1, Ch.5).

## 8. Common mistakes
- Building a complex model before a simple baseline is established (DMLS Ch.3).
- Training-serving skew: processing features differently during training and serving (DMLS Ch.6).
- Ignoring data quality: garbage in, garbage out applies doubly to ML (DMLS Ch.4).
- Not monitoring for drift: data distributions change over time, silently degrading performance (DMLS Ch.8).
- Optimizing for model metrics instead of business outcome (DMLS Ch.9).
- Building a model without a plan to deploy and maintain it (DMLS Ch.6).
- Treating ML as a one-time project instead of an ongoing system (DMLS Ch.1).
- Not tracking experiments: no one knows which combination of data/features/hyperparameters produced the best model (DMLS Ch.5).
- Assuming more data always helps: noisy, biased, or irrelevant data can hurt performance (DMLS Ch.2).
- Ignoring feedback loops: the model's predictions change user behavior, which changes future data (DMLS Ch.9).
- Deploying directly to 100% of traffic without a canary or A/B test (DMLS Ch.6).

## 9. Output format
```
## ML System Design: [System Name]

### Problem Frame
- Business objective:
- ML objective:
- Model type:
- Success criteria (business + ML):

### Baseline
- Heuristic baseline performance:
- Simple model baseline performance:

### Data Assessment
| Data Source | Type | Volume | Quality | Labels Available? |
|-------------|------|--------|---------|------------------|

### Feature Pipeline
- Feature sources:
- Feature transformations:
- Feature store:
- Training-serving consistency:

### Model Architecture
- Model type:
- Training approach:
- Hyperparameter tuning:
- Experiment tracking:

### Data Pipeline
- Batch/stream:
- Orchestration:
- Versioning/lineage:
- Storage:

### Deployment
- Strategy (online/batch/edge):
- Canary/rollback plan:
- Serving infrastructure:

### Monitoring
| Signal | Metric | Threshold | Alert |
|--------|--------|-----------|-------|

### Iteration Plan
- Retraining cycle:
- A/B testing plan:
- Model debugging approach:
```

## 10. Quality checklist
- [ ] Business problem is defined and ML is the right solution
- [ ] Simple baseline is established before complex modeling
- [ ] Data quality and availability are assessed
- [ ] Feature pipeline is consistent between training and serving
- [ ] Training-serving skew is explicitly prevented
- [ ] Model architecture matches the problem type
- [ ] Deployment strategy includes canary and rollback
- [ ] Monitoring covers data quality, drift, performance, and system health
- [ ] Experiment tracking and reproducibility are in place
- [ ] Business metric improvement from ML is measurable

## 11. Source books used
- Primary: Designing Machine Learning Systems (Huyen)
- Support: Machine Learning Design Patterns (Lakshmanan, Robinson, Munn), Fundamentals of Data Engineering (Reis & Housley), Designing Data-Intensive Applications (Kleppmann)

## 12. Notes on how the books complement each other
DMLS provides the comprehensive ML system design methodology: problem framing, data management, feature engineering, model deployment, monitoring, iteration. MLDP adds reusable patterns for common ML challenges (transformation, explainability, cascading, ensembles). FDE provides the data engineering foundation: data infrastructure, batch vs. stream processing, storage systems, data quality. DDIA adds the distributed systems perspective: replication, partitioning, consistency—all relevant when ML systems operate at scale. Together they form a complete ML system design methodology from data engineering through model deployment to production monitoring.
