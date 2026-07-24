---
name: api-design
description: Design APIs that are consistent, intuitive, evolvable, and aligned with the domain model and system architecture.
---

# api-design

## 1. Skill name
API Design

## 2. One-line purpose
Design APIs that are consistent, intuitive, evolvable, and aligned with the domain model and system architecture.

## 3. When to use this skill
- When designing a new API (REST, GraphQL, or RPC) for a service
- When reviewing an existing API for consistency, usability, and evolvability
- When defining the contract between frontend and backend
- When versioning or evolving an existing API
- When designing APIs for external consumers (public APIs)

## 4. When not to use this skill
- For internal, ephemeral scripts with no consumers
- When the API is already well-defined and meets all requirements
- For simple CRUD apps where the API mirrors the database schema directly

## 5. Core principles
- **Design the API before implementing it**: The API is the contract; it should be designed from the consumer's perspective (DWA Ch.1, Ch.2).
- **Consistency is king**: Use consistent naming conventions, error formats, pagination patterns, and authentication methods across all endpoints (DWA Ch.3, Ch.4).
- **Use resource-oriented design**: Model the API around resources (nouns), not actions (verbs). Use HTTP methods to define actions on resources (DWA Ch.2).
- **Design for evolvability**: Use versioning, backward-compatible changes, and extension points. Never remove or change a field without a deprecation period (DWA Ch.9, DDIA Ch.4).
- **Error responses must be actionable**: Every error should tell the consumer what went wrong and what to do about it (DWA Ch.4).
- **APIs should align with bounded contexts**: Each API should correspond to a bounded context, exposing the ubiquitous language (DWA Ch.2, DDD Ch.14).
- **The API is the language of the domain**: Use the domain's terminology, not technical jargon. The API should tell a story about the domain (DWA Ch.2, DDD Ch.2).
- **Design for performance and scalability**: Support pagination, partial responses, caching, and bulk operations where needed (DWA Ch.5, WSSE Ch.2, DDIA Ch.5).
- **Prefer standard conventions over custom solutions**: Use standard HTTP status codes, standard media types, standard authentication schemes (DWA Ch.3, Ch.4).
- **APIs are products**: Treat internal APIs with as much care as external ones. Versioning, documentation, and support apply to both (DWA Ch.1, TPP Ch.2).

## 6. Step-by-step method

### Step 1: Understand the domain and consumers
- Identify who will use the API (frontend team, partner, external developer)
- Understand the domain from the consumer's perspective using the ubiquitous language (DDD, DWA)
- List all use cases the API must support
- Define the resource model: what resources exist and how they relate

### Step 2: Design the resource model
- Identify resources (nouns): Users, Orders, Products, etc.
- Define relationships between resources (one-to-one, one-to-many, many-to-many)
- For each resource, define: identifier, attributes, sub-resources
- Use URL hierarchy to express resource relationships: `/users/{id}/orders`
- Keep URL depth shallow (max 3 levels) (DWA Ch.2)

### Step 3: Define operations for each resource
- Standard CRUD operations map to HTTP methods:
  - GET /resources — List
  - POST /resources — Create
  - GET /resources/{id} — Read
  - PUT /resources/{id} — Replace (full update)
  - PATCH /resources/{id} — Partial update
  - DELETE /resources/{id} — Delete
- Use POST for operations that don't fit CRUD (actions, computations)
- Use query parameters for filtering, sorting, pagination
- Use request bodies for complex parameters (DWA Ch.2, Ch.3)

### Step 4: Design the request and response formats
- Use JSON by default, with consistent naming (camelCase or snake_case, pick one) (DWA Ch.3)
- For each endpoint, define: request format, response format, error format
- Use standard envelope structure for paginated responses (DWA Ch.5)
- Use standard error format with a unique error code, human-readable message, and details field (DWA Ch.4)
- Consider compound documents or GraphQL for related data to reduce N+1 (DDIA Ch.2)
- Use ISO 8601 for dates and timestamps (DWA Ch.3)

### Step 5: Design for evolvability
- Use URL versioning (`/v1/users`) or header-based versioning (DWA Ch.9, DDIA Ch.4)
- Follow Postel's Law: be conservative in what you send, liberal in what you accept
- Add fields to responses as optional by default
- Use `deprecated` annotations for fields being phased out
- Never remove a field without a deprecation period and migration guide
- For fields that may change type, use a `type` discriminator field (DDIA Ch.4)
- Plan for extension: use maps/dictionaries for extensible attributes

### Step 6: Design for performance
- Support pagination for list endpoints (cursor-based vs. page-based) (DWA Ch.5, WSSE Ch.2)
- Support partial responses (fields parameter) (DWA Ch.5)
- Support bulk operations for batch processing (DWA Ch.5)
- Use caching headers (ETag, Last-Modified) for read endpoints (DDIA Ch.5)
- Design for idempotency key support for critical operations (DWA Ch.6)
- Rate limiting strategy: tokens, requests/sec, quotas per consumer

### Step 7: Define security and authentication
- Use standard authentication (OAuth 2.0, API keys, JWT) (DWA Ch.6)
- Define authorization model: what each consumer can access
- Use HTTPS only
- Document authentication flow clearly with examples

### Step 8: Document the API
- Provide a complete reference for every endpoint
- Include request and response examples
- Describe error conditions with examples
- Document rate limits and authentication
- Keep documentation up-to-date with the implementation (DWA Ch.7)
- Use OpenAPI/Swagger as the source of truth (DWA Ch.7)

## 7. Decision rules
- **If you have a resource with more than 20 attributes, consider splitting it into related resources** (DWA Ch.2).
- **If you have a URL path with more than 3 levels of nesting, reconsider the hierarchy** (DWA Ch.2).
- **If a client needs to make more than 2 API calls to get data for a single view, consider compound documents, includes, or GraphQL** (DWA Ch.5, DDIA Ch.2).
- **If an endpoint returns very large lists, require pagination by default** (DWA Ch.5).
- **For write operations that may take more than 30 seconds, use asynchronous processing (return 202 Accepted with a status endpoint)** (DWA Ch.5).
- **If a request can be safely retried, support idempotency keys** (DWA Ch.6, DDIA Ch.8).
- **If two operations must be atomic, consider whether they should be a single API call or use a transaction-like pattern** (DDIA Ch.7).
- **If the API consumer is external, be more conservative: deprecation periods should be longer, changes should be additive only** (DWA Ch.9).
- **If the API is for internal use only, still document it properly; the next team that maintains it will need the docs** (DWA Ch.7, TPP Ch.2).

## 8. Common mistakes
- Designing the API to mirror the internal database schema (DWA Ch.2).
- Using verbs in URLs (`/createUser`, `/deleteOrder`) instead of HTTP methods (DWA Ch.2).
- Ignoring error response design, returning 500 for everything (DWA Ch.4).
- Not versioning the API from the start, leading to breaking changes (DWA Ch.9).
- Mixing camelCase and snake_case across different endpoints (DWA Ch.3).
- Returning more data than the client needs, causing performance issues (DWA Ch.5, WSSE Ch.2).
- Not supporting pagination for list endpoints, then adding it as a breaking change (DWA Ch.5).
- Using nested resources where flat resources would suffice (`/users/{id}/orders/{orderId}/items/{itemId}`).
- Failing to document error conditions, leaving clients guessing (DWA Ch.4).
- Not planning for expansion: adding fields as required from day one, forcing breaking changes later (DWA Ch.9, DDIA Ch.4).
- Exposing IDs that reveal internal information (sequential IDs, database IDs) (DWA Ch.6).

## 9. Output format
```
## API Design: [API Name]
Version:      [e.g., v1]
Last Updated: YYYY-MM-DD

### 1. Resource Model
[Diagram or list of resources and relationships]

### 2. Endpoints
| Method | Path | Description | Auth Required | Pagination |
|--------|------|-------------|---------------|------------|

### 3. Request/Response Formats
[For each endpoint, show request structure, response structure, and example]

### 4. Error Format
```
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message",
    "details": { ... }
  }
}
```

### 5. Pagination
- Default page size:
- Maximum page size:
- Pagination method (cursor/page):

### 6. Versioning Strategy
- Location (URL/header):
- Deprecation policy:

### 7. Rate Limiting
- Per consumer limit:
- Window:
- Headers returned:

### 8. Authentication
- Method:
- Scopes/permissions:
```

## 10. Quality checklist
- [ ] Resource model aligns with domain model (not database schema)
- [ ] Naming is consistent across all endpoints
- [ ] Error format is standardized and actionable
- [ ] Pagination is supported for all list endpoints
- [ ] Versioning strategy is defined and documented
- [ ] Authentication and authorization are specified
- [ ] Every endpoint has a request and response example
- [ ] Backward compatibility strategy exists
- [ ] Rate limiting is defined
- [ ] Performance considerations (caching, partial responses, bulk) are addressed

## 11. Source books used
- Primary: Designing Web APIs (Ames, O'Hara, etc.)
- Support: Designing Data-Intensive Applications (Kleppmann), Domain-Driven Design (Evans), The Pragmatic Programmer (Hunt & Thomas), Web Scalability for Startup Engineers (Artasanchez & Bhalerao)

## 12. Notes on how the books complement each other
DWA provides the comprehensive API design methodology: resource modeling, naming conventions, error design, versioning, documentation. DDIA adds the distributed systems perspective: data encoding, schema evolution (Avro, Protobuf), and how API contracts relate to data flow. DDD provides the domain language that should drive the resource model. TPP adds practical developer principles (DRY, the DRY principle applied to API docs, ETC). WSSE adds scalability concerns: pagination, rate limiting, caching, load balancing as they relate to API design. Together they form a complete API design methodology from domain analysis to production deployment.
