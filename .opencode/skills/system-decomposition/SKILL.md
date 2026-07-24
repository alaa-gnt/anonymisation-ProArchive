---
name: system-decomposition
description: Split a software system into well-defined modules or services with clean boundaries, minimal coupling, and high cohesion.
---

# system-decomposition

## 1. Skill name
System Decomposition

## 2. One-line purpose
Split a software system into well-defined modules or services with clean boundaries, minimal coupling, and high cohesion.

## 3. When to use this skill
- At the start of a new project when deciding module/service boundaries
- When refactoring a monolithic system into services or packages
- When the codebase has become hard to change because of tangled dependencies
- During architecture reviews to assess module boundaries
- When on-boarding new teams to a large system

## 4. When not to use this skill
- For trivial scripts or one-off tools that won't evolve
- When the system is already cleanly decomposed and no boundary issues exist
- When the primary problem is performance, not structure

## 5. Core principles
- **Deep modules are better than shallow modules**: A deep module has a simple interface but lots of implementation behind it. A shallow module has a complex interface relative to the functionality it provides (POSD Ch.4).
- **Complexity comes from dependencies and obscurity**: Dependencies make it hard to change one module without changing another. Obscurity means you can't understand what a module does without reading its implementation (POSD Ch.2).
- **Information hiding is the key abstraction tool**: A module should hide implementation details behind a clean interface (POSD Ch.4).
- **Bounded contexts define the domain boundaries**: Each bounded context has its own ubiquitous language and model, and explicit translation happens at the boundaries (DDD Ch.14).
- **Focus on the domain, not the technology**: Decompose along domain lines, not technical layers (DDD).
- **Conway's Law**: System structure mirrors communication structure of the organization. Design for team boundaries (DDIA Ch.12, POSD).
- **The wrong decomposition creates a distributed monolith**: If services are tightly coupled and must be deployed together, the decomposition has failed (DDIA Ch.4, POSD Ch.9).
- **Modules should have one reason to change**: The Single Responsibility Principle applied at the module level (POSD Ch.4).
- **Define service boundaries by data ownership**: A service should own its data and expose operations on it, not expose raw data access (DDIA Ch.6, DDD).
- **Composability matters**: Modules should be composable like Unix pipes—small, focused tools that can be combined (TPP Ch.7, DDIA Ch.10).

## 6. Step-by-step method

### Step 1: Identify the domain and bounded contexts
- List all business capabilities the system must support
- Group capabilities into bounded contexts using DDD event-storming or domain analysis
- For each bounded context, define the ubiquitous language
- Identify the relationships between contexts (partnership, shared kernel, customer-supplier, conformist, anticorruption layer, open-host service, published language) (DDD Ch.14)

### Step 2: Define module responsibilities
- For each bounded context, define what it is responsible for and what it is NOT responsible for
- Write a single-paragraph mission statement for each module
- Identify the data that belongs to each module (data ownership)
- Define the operations each module exposes

### Step 3: Design the interfaces
- For each module, define its public API (functions, services, events, messages)
- The interface should be narrower than the implementation (deep module rule)
- Each interface should tell you what it does, not how it does it
- Aim for interfaces that are stable: changes to implementation should rarely require interface changes (POSD Ch.4, Ch.6)

### Step 4: Identify dependencies
- Map which modules depend on which
- A dependency should be toward stable, well-understood modules
- Avoid circular dependencies (A depends on B, B depends on A)
- Use dependency injection or service interfaces to invert dependencies where needed (TPP Ch.3)
- Count the dependencies: if module A depends on modules B, C, D, E, F, it may be too coupled

### Step 5: Assess coupling and cohesion
- **Cohesion**: Elements within a module should be strongly related. If a module contains unrelated functionality, split it.
- **Coupling**: Dependencies between modules should be minimal and explicit.
- Use the following heuristics:
  - If changing module A always requires changing module B, they are too coupled
  - If you cannot test module A without module B, they are too coupled
  - If module A accesses internal data of module B, the boundary is wrong

### Step 6: Evaluate module depth
- For each module, count the number of public methods vs the implementation complexity
- A shallow module has many public methods relative to the implementation size
- A deep module has few public methods relative to the implementation size
- Refactor shallow modules: either combine them with related modules or push complexity into the implementation (POSD Ch.4)

### Step 7: Document the decomposition
- Create a module dependency diagram
- For each module, document: name, mission, owned data, public API, dependencies, key design decisions
- Record any exceptions or known violations (e.g., modules that are still too coupled, with a plan to fix)

## 7. Decision rules
- **If a module has more than 10 public methods, check if any of them could be combined or made more abstract** (POSD Ch.4).
- **If a module depends on more than 5 other modules, look for dependency inversion opportunities**.
- **If two teams must coordinate on every change to their respective modules, the boundary is wrong** (Conway's Law).
- **If a service exposes its database directly (e.g., table access), it has failed to hide information** (DDIA Ch.6, POSD Ch.4).
- **If a module changes for more than one reason (e.g., business logic + serialization + persistence), separate the concerns**.
- **If the system has services that cannot be deployed independently, it is a distributed monolith, not a microservices architecture** (DDIA Ch.4).
- **If a module's test requires extensive mocking of 5+ other modules, the interface is too coupled** (CC Ch.20, TPP Ch.7).

## 8. Common mistakes
- Decomposing by technical layer (controllers, services, repositories) instead of by domain (DDD Ch.14).
- Creating shallow modules that add abstraction without reducing complexity (POSD Ch.4).
- Designing services that are too fine-grained, leading to chatty communication and performance problems (DDIA Ch.4, WSSE Ch.2).
- Designing services that are too coarse-grained, leading to a monolith with no clear boundaries.
- Assuming microservices solve all problems. The cost is high: network latency, consistency challenges, operational complexity (DDIA Ch.5-9).
- Exposing internal data structures through the interface, creating tight coupling (POSD Ch.4, DDD Ch.14).
- Not defining the ubiquitous language per bounded context, leading to confusion across teams (DDD Ch.2).
- Creating an anticorruption layer that adds translation for everything, even for stable, well-understood systems (DDD Ch.14).
- Relying on shared databases between services, which tightly couples them (DDIA Ch.6).
- Using synchronous calls (HTTP/REST) where async messaging would reduce coupling (DDIA Ch.4, Ch.11).

## 9. Output format
```
## System Decomposition: [System Name]

### Bounded Context Map
[Diagram: bounded contexts, relationships, and translation layers]

### Module: [Module Name]
- Mission:
- Owned data:
- Public API:
- Dependencies:
- Key design decisions:

### Module: [Module Name 2]
...

### Dependency Matrix
| Module | Depends On | Dependency Type | Stability |

### Depth Assessment
| Module | Public Methods | Implementation Complexity | Depth Rating |

### Violations and Plan
| Issue | Severity | Plan to Fix |
```

## 10. Quality checklist
- [ ] Bounded contexts are mapped with relationships defined
- [ ] Each module has a mission statement
- [ ] Each module owns its data (no shared databases)
- [ ] Interfaces are narrower than implementations (deep modules)
- [ ] No circular dependencies exist
- [ ] No module depends on more than 5 others
- [ ] Ubiquitous language is defined per bounded context
- [ ] Deployment independence is verified (or explicitly traded off)
- [ ] Module depth is assessed
- [ ] Anticorruption layers are planned for legacy system boundaries

## 11. Source books used
- Primary: A Philosophy of Software Design (Ousterhout)
- Support: Designing Data-Intensive Applications (Kleppmann), Domain-Driven Design (Evans), The Pragmatic Programmer (Hunt & Thomas), Code Complete (McConnell)

## 12. Notes on how the books complement each other
POSD provides the core theory of module design: deep vs shallow modules, information hiding, complexity management. DDD provides the methodology for finding domain boundaries (bounded contexts, ubiquitous language). DDIA adds the distributed systems perspective: what happens when modules become services. TPP provides pragmatic principles (DRY, orthogonality, reversibility). CC adds the construction-level view (routines, coupling, cohesion). Together they form a complete decomposition methodology from code to service to system.
