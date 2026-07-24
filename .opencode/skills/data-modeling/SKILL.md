---
name: data-modeling
description: Design data models that match access patterns, maintain consistency guarantees, and evolve gracefully over time.
---

# data-modeling

## 1. Skill name
Data Modeling

## 2. One-line purpose
Design data models that match access patterns, maintain consistency guarantees, and evolve gracefully over time.

## 3. When to use this skill
- When designing a new database schema (relational, document, graph, or key-value)
- When choosing between data model approaches (relational vs. document vs. graph)
- When migrating from one data model to another
- When defining schemas for event streams or message queues
- When modeling entities and relationships for an API

## 4. When not to use this skill
- For ephemeral data that has no schema requirements (e.g., temporary caches, logs)
- When a simple file or blob store suffices
- When the data model is already fixed by a third-party system

## 5. Core principles
- **A data model is the most critical part of a system**: How the data is represented affects everything else (queryability, performance, maintainability) (DDIA Ch.2).
- **Match the data model to the application's access patterns**: Document model works well for one-to-many relationships; relational model works well for many-to-many; graph model works well for highly interconnected data (DDIA Ch.2).
- **Normalize to reduce duplication, but denormalize for read performance**: The relational model uses normalization to reduce redundancy. Denormalization is a valid optimization when reads dominate writes (DDIA Ch.2, FDE Ch.5).
- **Schema-on-read is flexible but risky**: Document databases use schema-on-read (no enforced schema), which can lead to inconsistent data. Schema-on-write (enforced schema) provides stronger guarantees (DDIA Ch.2).
- **Data model evolution is inevitable**: Use techniques like schema versioning, migration scripts, or dual-writing to handle changes over time (DDIA Ch.4).
- **The domain model should drive the data model**: Don't let the database technology dictate the domain model (DDD Ch.3, Ch.4).
- **Entities have identity, value objects do not**: Entities have a lifecycle and identity (e.g., a User). Value objects are defined by their attributes (e.g., an Address) (DDD Ch.5).
- **Aggregates define consistency boundaries**: Load and save aggregate roots as a unit. This determines transactional boundaries (DDD Ch.6).
- **Design for read patterns first**: Start with the questions you need to answer, then design the schema to make those reads efficient (FDE Ch.5, DWA Ch.5).
- **Consider polyglot persistence**: Different data within the same system may benefit from different storage technologies (DDIA Ch.2, FDE Ch.5).

## 6. Step-by-step method

### Step 1: Understand the domain
- Work with domain experts to understand the business entities and their relationships
- Identify entities (with identity), value objects (without identity), and aggregates (DDD)
- Define the ubiquitous language for all data concepts
- List all the questions the system must answer (access patterns)

### Step 2: Identify access patterns
- For each entity, list all operations: create, read, update, delete, list, search
- For each read operation, specify: parameters, frequency, required response time, data volume
- For each write operation, specify: frequency, data volume, consistency requirements
- Identify which entities are read together (this suggests how to structure the model)

### Step 3: Choose the data model approach
- **Relational**: Good for structured data with well-defined relationships, need for joins, ad-hoc queries, ACID transactions (DDIA Ch.2)
- **Document**: Good for data that is mostly self-contained (one-to-many within a document), flexible schema, rapid iteration (DDIA Ch.2)
- **Graph**: Good for highly interconnected data, traversals, recursive relationships (DDIA Ch.2)
- **Key-Value**: Good for simple lookups by primary key, high throughput, caching (DDIA Ch.2)
- **Column-family**: Good for wide-column data, analytics, time-series (DDIA Ch.2, FDE Ch.5)
- **Time-series**: Good for event data with time-based queries (FDE Ch.5)
- Choose based on access patterns, not popularity

### Step 4: Design the schema
- For relational: Define tables, columns, primary keys, foreign keys, indexes, constraints, normalization level
- For document: Define document structure, nesting vs. references, schema validation rules
- For graph: Define node types, edge types, properties, indexes
- Apply DDD tactical patterns: entities, value objects, aggregates, repositories, domain events (DDD Ch.5-7)
- Define the aggregate boundaries: aggregate root, consistency boundaries, loading strategy

### Step 5: Define key and index strategy
- For each entity, define the natural key or surrogate key
- For each access pattern, define the index needed (primary index, secondary index, composite index, covering index) (DDIA Ch.3)
- Consider: B-tree vs. LSM-tree tradeoffs (read-heavy favors B-trees, write-heavy favors LSM-trees) (DDIA Ch.3)
- Consider: hash index vs. range index based on query patterns
- For partitioned data: choose partitioning key to avoid hot spots (DDIA Ch.6)

### Step 6: Plan for evolution
- Design for forward and backward compatibility: new code should read old data, old code should read new data (DDIA Ch.4)
- Choose schema evolution mechanisms: optional fields, default values, version fields, migration scripts
- Plan the migration strategy: one-shot migration vs. gradual migration vs. dual-writing
- Use schema registries for message schemas (DDIA Ch.4)
- Consider event sourcing for domains where audit history matters (DDIA Ch.11)

### Step 7: Validate the model
- Walk through the primary access patterns and verify the schema supports them
- Estimate data volume and verify the approach scales
- Check for N+1 query problems (especially in ORMs and graph APIs)
- Check that aggregate boundaries match consistency requirements
- Test the model with real data examples

## 7. Decision rules
- **If the data has clear, stable relationships with joins, use a relational model** (DDIA Ch.2).
- **If the data is mostly self-contained and accessed as a unit (e.g., a blog post with comments), use a document model** (DDIA Ch.2).
- **If the data is a graph of highly interconnected nodes with recursive traversals (e.g., social network, recommendation engine), use a graph model** (DDIA Ch.2).
- **If the access pattern is exclusively primary-key lookup (e.g., user session, cache), use a key-value store** (DDIA Ch.2).
- **If query patterns are unknown or changing rapidly, use schema-on-read and enforce validation in the application** (DDIA Ch.2).
- **If consistency guarantees are critical (e.g., financial data), choose a database with strong consistency and ACID transactions** (DDIA Ch.7, Ch.9).
- **If the main requirement is high write throughput and analytics (e.g., event logs), choose column-family or time-series storage** (DDIA Ch.3, FDE Ch.5).
- **If the aggregate is larger than a few hundred fields or deeply nested, consider splitting it** (DDD Ch.6).
- **If an entity's data changes over time and you need full history, consider event sourcing** (DDIA Ch.11).
- **If two aggregates need to be updated atomically, consider whether they should be part of the same aggregate** (DDD Ch.6).

## 8. Common mistakes
- Modeling based on the API output rather than the domain model (DDD Ch.4, DWA Ch.5).
- Choosing a NoSQL database "because it's modern" without understanding the access patterns (DDIA Ch.2).
- Making aggregates too large (performance problems) or too small (consistency problems) (DDD Ch.6).
- Using the same data model for OLTP and OLAP without considering the different requirements (DDIA Ch.3, FDE Ch.5).
- Ignoring schema evolution: assuming the schema will never change (DDIA Ch.4).
- Under-indexing (slow queries) or over-indexing (slow writes, large storage) (DDIA Ch.3).
- Using secondary indexes without understanding their partitioning implications (DDIA Ch.6).
- Storing denormalized data without a plan for keeping it in sync (DDIA Ch.2, FDE Ch.5).
- Not planning for hot keys in partitioned systems (DDIA Ch.6).
- Modeling value objects as entities and vice versa (DDD Ch.5).
- Creating an anemic domain model where entities are just data containers with no behavior (DDD Ch.4).

## 9. Output format
```
## Data Model: [Domain/System Name]

### Domain Overview
- Entities:
- Value objects:
- Aggregates:
- Ubiquitous language terms:

### Storage Technology
- Primary database:
- Justification:
- Polyglot persistence decisions:

### Schema Design
[For each entity/aggregate]
- Type (Entity/ValueObject/Aggregate):
- Fields:
  - [name]: [type] [constraints]
- Relationships:
- Indexes:
- Consistency requirements:

### Access Pattern Mapping
| Access Pattern | Query | Index Used | Expected Latency |

### Evolution Plan
- Schema versioning strategy:
- Migration strategy:
- Compatibility strategy:

### Model Validation
- N+1 check:
- Volume estimate:
- Consistency boundary check:
```

## 10. Quality checklist
- [ ] Domain entities and value objects are correctly identified
- [ ] Aggregate boundaries match consistency requirements
- [ ] Storage technology matches access patterns
- [ ] Primary access patterns are mapped to queries
- [ ] Indexes are designed for all read patterns
- [ ] Key partitioning avoids hot spots
- [ ] Schema evolution plan exists
- [ ] N+1 query problems are identified and mitigated
- [ ] Consistency guarantees are explicit
- [ ] Data volume estimates support the choice

## 11. Source books used
- Primary: Designing Data-Intensive Applications (Kleppmann)
- Support: Fundamentals of Data Engineering (Reis & Housley), Domain-Driven Design (Evans), Designing Web APIs (Ames, O'Hara, etc.)

## 12. Notes on how the books complement each other
DDIA provides the deep foundation: data model comparison (relational, document, graph), storage internals (B-trees, LSM-trees, column-oriented storage), and consistency models. FDE adds the data engineering perspective: storage systems classification, batch vs. stream, schema design for analytics. DDD provides the domain-driven approach: entities, value objects, aggregates as the building blocks of the model. DWA adds the API perspective: how data models translate to API contracts. Together they cover the full cycle from domain modeling to storage implementation to API exposure.
