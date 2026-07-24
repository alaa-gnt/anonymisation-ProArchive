---
name: architecture-analysis
description: Evaluate a system architecture against reliability, scalability, maintainability, and simplicity criteria to identify risks and improvement opportunities.
---

# architecture-analysis

## 1. Skill name
Architecture Analysis

## 2. One-line purpose
Evaluate a system architecture against reliability, scalability, maintainability, and simplicity criteria to identify risks and improvement opportunities.

## 3. When to use this skill
- Before building a new system or major feature
- When reviewing an existing system that has reliability, scalability, or performance problems
- During an architecture review or design review meeting
- When assessing tradeoffs between different technical approaches
- Before writing an RFC or architecture decision record (ADR)

## 4. When not to use this skill
- For trivial, single-module changes where the architecture is already well-understood
- When the team needs rapid prototyping or exploratory coding, not analysis
- When the system is already fully documented and no decisions are pending

## 5. Core principles
- **Reliability first**: The system must do what it is supposed to do, even when faults occur (DDIA Ch.1). Faults are not the same as failures; a fault-tolerant system can anticipate and handle faults.
- **Scalability is about coping with load**: Describe load with load parameters (e.g., requests/sec, read/write ratio, fan-out). Describe performance with percentiles (p50, p95, p99, p999). Tail latency matters more than averages (DDIA Ch.1).
- **Maintainability is three concerns**: Operability (easy for ops teams), Simplicity (low complexity), Evolvability (easy to change) (DDIA Ch.1, POSD Ch.2).
- **Complexity is accidental, not inherent**: Deep modules are good, shallow modules are bad. Complexity comes from dependencies and obscurity (POSD Ch.2, Ch.4).
- **Good architecture enables incremental change**: The system should allow you to change one part without affecting others (DDIA Ch.12, POSD).
- **Bounded contexts keep models clean**: Separate domains with explicit boundaries and translation layers (DDD Ch.14).
- **Use the right storage for the right job**: Not every system needs a relational database; match storage to access patterns (DDIA Ch.2, Ch.3, Ch.6).
- **Everything is a tradeoff**: Consistency vs. performance, latency vs. throughput, strong vs. eventual consistency. Document the tradeoff and the rationale (DDIA Ch.5, Ch.7, Ch.9, WSSE).
- **Design for operation**: Observability (metrics, logs, traces) is not optional (DDIA Ch.1, WSSE Ch.7).

## 6. Step-by-step method

### Step 1: Gather context
- Identify the system boundaries and stakeholders
- Collect existing diagrams, docs, ADRs, and runbooks
- Define the primary load parameters (requests/sec, data volume, read/write ratio, fan-out)
- Collect current performance metrics (response time percentiles, error rates, resource utilization)

### Step 2: Decompose the system
- Identify bounded contexts (DDD)
- Draw component boundaries and their responsibilities
- List all data stores, message queues, caches, and external services
- Document data flow between components (requests, responses, events)

### Step 3: Analyze each component for reliability
- Identify single points of failure
- Check replication strategy (leader/follower, multi-leader, leaderless) (DDIA Ch.5)
- Check partition strategy (key range vs. hash partitioning, skew, hot spots) (DDIA Ch.6)
- Review retry and timeout logic (circuit breakers, exponential backoff) (DDIA Ch.8)
- Check for cascading failures (e.g., retry storms)
- Review backup and restore procedures

### Step 4: Analyze scalability
- For each component, identify which load parameters affect it
- For each load parameter, determine whether the system scales horizontally or vertically
- Check for bottlenecks: single-writer, shared state, contention on locks
- Review caching strategy (cache hit rates, invalidation, write-through vs. write-back)
- Verify that partitioning distributes load evenly (hot spot detection)

### Step 5: Analyze consistency and data flow
- Identify the consistency guarantees needed for each operation (DDIA Ch.7, Ch.9)
- Check for read-after-write, monotonic reads, consistent prefix reads requirements
- Verify that the system handles replication lag
- Review transaction boundaries and isolation levels
- Check for potential write conflicts and how they are resolved

### Step 6: Evaluate maintainability
- Assess module depth: do modules hide complexity or expose it? (POSD Ch.4)
- Check for information leakage between layers
- Review error handling: are errors propagated or swallowed?
- Check for tactical programming (shortcuts that will cause long-term pain) (POSD Ch.3)
- Review testing strategy at each level

### Step 7: Identify risks and tradeoffs
- List each risk with severity and likelihood
- For each risk, propose at least two mitigation strategies
- For each tradeoff, document both sides and the chosen direction
- Record the analysis as an ADR or architecture review doc

## 7. Decision rules
- **If a component has no redundant replica, flag it as a single point of failure.**
- **If p99 latency is >10x p50, flag tail latency amplification** and investigate queuing, GC pauses, or head-of-line blocking (DDIA Ch.1).
- **If the system uses eventual consistency, flag all operations that require strong consistency** and verify they have a fallback or confirmation step (DDIA Ch.9).
- **If the system has no circuit breakers or retry limits for external calls, flag cascading failure risk** (DDIA Ch.8).
- **If a module has more than 7 public methods with complex interdependencies, flag it as a shallow module that should be split** (POSD Ch.4).
- **If there is no runbook or operational documentation, flag operability risk** (DDIA Ch.1).

## 8. Common mistakes
- Confusing faults with failures. Fault-tolerant systems handle faults; failure is when the system as a whole stops serving (DDIA Ch.1).
- Designing for the peak load that happens 0.1% of the time without a cost analysis. Instead, plan to scale during peaks (DDIA Ch.1, WSSE Ch.4).
- Assuming the network is reliable. In distributed systems, the network is unreliable, clocks are unreliable, and processes can pause (DDIA Ch.8).
- Choosing strong consistency everywhere when weaker guarantees would suffice, adding unnecessary cost and latency (DDIA Ch.9).
- Ignoring human error. Most outages are caused by humans, not hardware. Design for operability (DDIA Ch.1).
- Oversimplifying the domain model. The model must be rich enough to capture business invariants (DDD Ch.1, Ch.2).
- Reviewing architecture without load parameters. Scalability cannot be assessed without knowing the load (DDIA Ch.1).
- Treating the API as an afterthought. The API is the contract; it must be designed before implementation (DWA Ch.1, Ch.2).

## 9. Output format
```
## Architecture Analysis: [System Name]
Date:           YYYY-MM-DD
Reviewer:       [Name]
Version:        [Version]

### 1. Context and Scope
- System boundaries:
- Primary load parameters:
- Stakeholders:

### 2. Component Map
[ASCII or reference to diagram showing components, data flows, and stores]

### 3. Reliability Assessment
| Component | Risk | Severity | Mitigation |
|-----------|------|----------|------------|

### 4. Scalability Assessment
| Component | Limiting Factor | Scaling Mechanism | Bottleneck? |

### 5. Consistency and Data Flow
- Consistency model per operation:
- Replication lag tolerance:
- Conflict resolution:

### 6. Maintainability Assessment
- Module depth:
- Error handling:
- Operational readiness:

### 7. Tradeoffs and Decisions
| Decision | Options Considered | Chosen | Rationale |

### 8. Risk Register
| Risk | Likelihood | Impact | Mitigation |
```

## 10. Quality checklist
- [ ] Load parameters are identified and quantified
- [ ] Every component is evaluated for single points of failure
- [ ] Replication and partitioning strategies are documented
- [ ] Consistency guarantees are explicit for each critical operation
- [ ] Tail latency and percentiles are measured, not just averages
- [ ] Error handling and retry logic is reviewed
- [ ] Module depth is assessed (deep vs shallow modules)
- [ ] Tradeoffs are documented with rationale
- [ ] Runbook or operational docs exist (or gap is noted)
- [ ] Bounded contexts and domain models are defined

## 11. Source books used
- Primary: Designing Data-Intensive Applications (Kleppmann)
- Support: A Philosophy of Software Design (Ousterhout), Domain-Driven Design (Evans), Designing Web APIs (Ames, O'Hara, etc.), Web Scalability for Startup Engineers (Artasanchez & Bhalerao)

## 12. Notes on how the books complement each other
DDIA provides the rigorous foundation for distributed systems analysis (replication, partitioning, transactions, consistency). POSD provides the criteria for evaluating code-level design (module depth, complexity). DDD provides the language for decomposing systems into bounded contexts. DWA focuses on API contracts as the interface between components. WSSE adds the startup-engineering perspective: practical tradeoffs under resource constraints. Together they cover the full stack from code to distributed data to operations.
