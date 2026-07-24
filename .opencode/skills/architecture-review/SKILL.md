---
name: architecture-review
description: Evaluate a system architecture design to identify risks, validate tradeoffs, and ensure alignment with reliability, scalability, maintainability, and security requirements before implementation begins.
---

# architecture-review

## 1. Work skill name
Architecture Review

## 2. Job to be done
Evaluate a system architecture design to identify risks, validate tradeoffs, and ensure alignment with reliability, scalability, maintainability, and security requirements before implementation begins.

## 3. Trigger or use case
- A team has produced an architecture design document and needs a review before implementation starts
- A system is experiencing incidents and the root cause may be architectural
- The team is planning a major refactoring or migration
- A new team member or stakeholder wants to understand the architecture
- Before a major investment decision (build vs. buy, new platform, cloud migration)

## 4. Required inputs
- Architecture design document or RFC (required)
- Current system diagrams (if reviewing an existing system)
- Load parameters (expected traffic, data volume, growth projections)
- Existing ADRs or design decisions
- Runbooks or operational docs (if available)
- Previous incident post-mortems (if any)

## 5. Step-by-step workflow

### Step 1: Pre-read the design document
- Read the entire architecture document before the review meeting
- Identify the key design decisions and tradeoffs
- List questions and concerns
- Verify the document has: context, constraints, system boundaries, component diagram, data flow, key decisions, tradeoffs, operational considerations

### Step 2: Verify scope and requirements
- Check that the design addresses the stated requirements (functional and non-functional)
- Check that the load parameters are defined and quantified
- Check that the constraints (budget, timeline, team skills, compliance) are known and accounted for

### Step 3: Analyze reliability (DDIA Ch.1, Ch.5-9)
- Identify single points of failure
- Review replication strategy (leader/follower, multi-leader, leaderless)
- Review partition strategy
- Check backup and restore plans
- Review error handling and retry logic
- Check for cascading failure scenarios

### Step 4: Analyze scalability (DDIA Ch.1, Ch.6, WSSE Ch.2-4)
- For each component, identify the limiting factor under load
- Review caching strategy (what, where, invalidation)
- Review partitioning strategy (hot spots, skew)
- Review database indexing strategy
- Review async processing for heavy operations

### Step 5: Analyze maintainability (POSD Ch.4, Ch.6)
- Review module boundaries
- Assess information hiding
- Check for tactical programming
- Review API design (DWA Ch.2-5)

### Step 6: Analyze security and compliance
- Authentication and authorization
- Data encryption (at rest, in transit)
- Audit logging
- Compliance requirements (GDPR, SOC2, etc.)

### Step 7: Document findings and recommendations
- For each finding: describe the risk, severity (critical/major/minor), and recommendation
- For each tradeoff: describe both options, why the chosen option was preferred, and what was given up
- Prioritize: critical issues must be resolved before implementation; major issues should be resolved; minor issues can be tracked

### Step 8: Present and discuss
- Present findings to the design team
- Focus on critical and major issues
- Discuss alternatives and tradeoffs
- Reach consensus on next steps

## 6. Output deliverable
An architecture review document with sections for: scope review, reliability assessment, scalability assessment, maintainability assessment, security review, finding register with severity, recommendations, and tradeoff analysis.

## 7. Quality checklist
- [ ] Load parameters are quantified (not just "high traffic")
- [ ] Single points of failure are identified
- [ ] Replication and partitioning strategies are reviewed
- [ ] Caching strategy is reviewed (hit rate, invalidation)
- [ ] Error handling and retry logic are reviewed
- [ ] Module boundaries and information hiding are assessed
- [ ] API design follows consistent conventions
- [ ] Security and compliance requirements are addressed
- [ ] Tradeoff decisions are documented with rationale
- [ ] Findings are prioritized by severity

## 8. Common failure modes
- Reviewing without load parameters (cannot assess scalability)
- Focusing only on the happy path (ignoring failure modes)
- Not distinguishing between critical and minor issues (everything is a "concern")
- Reviewing too late (after implementation has started)
- Reviewing without domain context (the domain model drives the architecture)
- Ignoring operations (no runbook, no monitoring plan)
- Overlooking data flow (how data moves between components)

## 9. Dependencies on framework skills
- Architecture Analysis (primary framework for the review)
- System Decomposition (for module boundary assessment)
- Data Modeling (for reviewing the data model and storage choices)
- API Design (for reviewing API contracts)

## 10. Source books used
- Primary: Designing Data-Intensive Applications (Kleppmann)
- Support: A Philosophy of Software Design (Ousterhout), Domain-Driven Design (Evans), Designing Web APIs (Ames, O'Hara, etc.), Web Scalability for Startup Engineers (Artasanchez & Bhalerao), Fundamentals of Data Engineering (Reis & Housley)

## 11. Example of a good final output structure
```
# Architecture Review: Order Management System

## Scope
- System boundaries: Order Service, Payment Service, Inventory Service
- Load parameters: 1000 orders/sec peak, 10:1 read:write ratio
- Constraints: SOC2 compliance, AWS, Node.js/Python

## Reliability Review
| Component | Risk | Severity | Recommendation |
|-----------|------|----------|----------------|
| Order DB (single primary) | If primary fails, writes blocked until failover | Critical | Add read replicas + automatic failover |
| Payment retry logic | No exponential backoff, could cause retry storm | Major | Add exponential backoff + jitter |

## Scalability Review
| Component | Limiting Factor | Recommendation |
|-----------|--------------------------------|
| Order service | DB connection pool (100) | Scale read replicas horizontally |
| Inventory cache | TTL-based invalidation may serve stale data | Add write-through cache invalidation |

## Maintainability Review
- Order service has a single class with 12 responsibilities → split into bounded contexts
- API uses verbs in URLs (/createOrder) → use HTTP methods

## Tradeoffs
| Decision | Options | Chosen | Rationale |
|----------|---------|--------|-----------|
| Consistency model | Strong vs. eventual | Eventual for order status | Accept stale reads for lower latency |

## Risk Register
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Payment provider outage | Low | High | Retry with backoff + dead-letter queue |
```
