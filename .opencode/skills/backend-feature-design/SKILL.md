---
name: backend-feature-design
description: Design a backend feature from API contract through implementation, including request/response handling, data access, business logic, error handling, and testing strategy.
---

# backend-feature-design

## 1. Work skill name
Backend Feature Design

## 2. Job to be done
Design a backend feature from API contract through implementation, including request/response handling, data access, business logic, error handling, and testing strategy.

## 3. Trigger or use case
- A new feature needs to be implemented in an existing service
- A new API endpoint needs to be designed and built
- A new microservice needs to be created
- An existing feature needs significant rework

## 4. Required inputs
- Feature requirements (user stories, acceptance criteria)
- API specifications (OpenAPI/Swagger if applicable)
- Existing codebase and service architecture
- Data model for the relevant domain
- Existing integration points (other services, databases, queues)

## 5. Step-by-step workflow

### Step 1: Understand the feature requirements
- Read the user stories and acceptance criteria
- Clarify ambiguous requirements with the product owner
- Identify the domain entity or operation involved
- Define the scope: what is in scope and what is explicitly out of scope

### Step 2: Design the API contract (DWA Ch.2-5)
- Define the endpoint (method, path, parameters)
- Define the request structure (body, headers, query params)
- Define the response structure (body, headers, status codes)
- Define error responses for each failure mode
- Follow the existing API conventions in the service

### Step 3: Design the data access layer
- Identify the data needed for the feature
- Choose the appropriate storage mechanism (DB, cache, queue, blob)
- Design the database schema changes (if any)
- Plan the data migration strategy (if schema changes are needed)
- Review indexing for the new access patterns (DDIA Ch.3)

### Step 4: Design the business logic layer
- Implement the domain logic following DDD tactical patterns (entities, value objects, aggregates, domain services) (DDD Ch.5-7)
- Keep business logic separate from infrastructure concerns (DB access, external API calls)
- Handle error cases: validation errors, business rule violations, system errors
- Use appropriate design patterns (strategy, factory, repository) (TPP Ch.3)

### Step 5: Design error handling
- Define all failure modes:
  - Input validation errors (400 Bad Request)
  - Authentication/authorization errors (401/403)
  - Not found (404)
  - Conflict (409) for state conflicts
  - Rate limiting (429)
  - Internal errors (500)
- For each failure mode, define the error response format
- Use consistent error format across all endpoints (DWA Ch.4)

### Step 6: Design for performance and scalability
- Consider caching for read-heavy endpoints
- Consider async processing for long-running operations
- Consider pagination for list endpoints
- Consider bulk endpoints for batch operations (DWA Ch.5, WSSE Ch.2)

### Step 7: Write tests
- Unit tests for business logic (CC Ch.20, TPP Ch.7)
- Integration tests for data access
- Integration tests for the API endpoint
- Edge case tests: null inputs, empty results, concurrent requests
- Error handling tests: each error path should have a test

### Step 8: Document and review
- Update the API documentation (OpenAPI)
- Write or update ADRs for significant design decisions
- Submit the design for review before coding

## 6. Output deliverable
A backend feature design document including: API contract (endpoint, request, response, errors), data access plan, business logic design, error handling strategy, test plan, and ADRs for significant decisions.

## 7. Quality checklist
- [ ] API endpoint follows RESTful conventions (nouns, HTTP methods, consistent naming)
- [ ] Request and response structures are documented
- [ ] Error responses are defined for each failure mode
- [ ] Data access is designed for the access patterns
- [ ] Indexes are planned for new queries
- [ ] Business logic is separated from infrastructure concerns
- [ ] Validation rules are defined
- [ ] Edge cases are handled (empty, null, concurrent requests)
- [ ] Tests cover happy path, error paths, and edge cases
- [ ] Performance considerations are addressed (caching, pagination, async)

## 8. Common failure modes
- Designing the API before understanding the data model (DWA Ch.5)
- Mixing business logic with infrastructure code (DDD Ch.4)
- Not defining error responses, forcing clients to parse 500 errors (DWA Ch.4)
- Forgetting to handle concurrent writes or state conflicts (DDIA Ch.7)
- Writing the API to mirror the database schema (DWA Ch.2)
- Not testing error paths (CC Ch.20)
- Skipping the design phase and going straight to coding
- Ignoring existing conventions in the codebase

## 9. Dependencies on framework skills
- API Design (for API contract design)
- Data Modeling (for data layer design)
- Testing and Verification (for test planning)
- Refactoring (for maintaining code quality)

## 10. Source books used
- Primary: Designing Web APIs (Ames, O'Hara, etc.)
- Support: The Pragmatic Programmer (Hunt & Thomas), Code Complete (McConnell), Domain-Driven Design (Evans), Refactoring (Fowler)

## 11. Example of a good final output structure
```
# Backend Feature: Order Cancellation

## API Contract
- `POST /api/v1/orders/{id}/cancel`
- Request: `{ "reason": "changed_mind", "note": "optional" }`
- Response 200: `{ "status": "cancelled", "cancelled_at": "ISO8601", "refund_id": "ref-123" }`
- Error 404: `{ "error": "order_not_found", "message": "Order ID invalid" }`
- Error 409: `{ "error": "order_already_fulfilled", "message": "Cannot cancel a shipped order" }`

## Business Logic
- Order aggregate: validate status is not shipped/delivered
- Initiate refund via PaymentService
- Update order status to CANCELLED
- Publish OrderCancelled domain event

## Error Handling
| Condition | Status | Error Code |
|-----------|--------|------------|
| Order not found | 404 | order_not_found |
| Order already shipped | 409 | order_already_fulfilled |
| Payment service down | 503 | payment_service_unavailable |

## Tests
- Cancel pending order → status is cancelled, refund initiated
- Cancel shipped order → 409 error
- Cancel non-existent order → 404 error
- Concurrent cancellation → only first request succeeds
```
