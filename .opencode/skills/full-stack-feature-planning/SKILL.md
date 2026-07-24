---
name: full-stack-feature-planning
description: Plan a feature end-to-end from the API contract through backend, frontend, data, and deployment, ensuring all layers work together coherently.
---

# full-stack-feature-planning

## 1. Work skill name
Full-Stack Feature Planning

## 2. Job to be done
Plan a feature end-to-end from the API contract through backend, frontend, data, and deployment, ensuring all layers work together coherently.

## 3. Trigger or use case
- A new feature spans frontend and backend and needs coordinated planning
- A new API endpoint needs both frontend and backend changes
- A feature requires data schema changes affecting multiple services
- Multiple teams need to coordinate on a shared feature

## 4. Required inputs
- Feature requirements (user stories, acceptance criteria, designs/mockups)
- Existing API specifications and frontend components
- Data model and database schema
- Service architecture diagram
- Deployment and release process

## 5. Step-by-step workflow

### Step 1: Decompose the feature into layers
- Define the API contract first (DWA Ch.2-5)
- Define the data model changes (DDIA Ch.2, FDE Ch.5)
- Define the backend service changes
- Define the frontend changes
- Identify integration points between layers
- For each change, estimate effort

### Step 2: Design the API contract (DWA Ch.2-5)
- Define the endpoints and their request/response formats
- Ensure the API supports the frontend's data needs (avoid N+1 round-trips)
- Define error responses
- If existing endpoints need changes, plan backward-compatible evolution (DWA Ch.9, DDIA Ch.4)

### Step 3: Design the data layer changes (DDIA Ch.2-3, FDE Ch.5)
- Plan database schema changes (new tables, columns, indexes)
- Plan the data migration strategy (zero-downtime if needed)
- Identify cache invalidations needed
- Plan for new data pipelines if the feature requires data processing

### Step 4: Design the backend changes
- Implement new API endpoints or modify existing ones
- Add business logic
- Handle new error cases
- Add observability (metrics, logs, traces for the new feature)

### Step 5: Design the frontend changes
- New components or modifications to existing ones
- State management for the new feature
- Error handling and loading states
- Mobile responsiveness considerations
- Accessibility requirements

### Step 6: Plan testing across layers
- Unit tests for each layer
- Integration tests for API endpoints
- End-to-end tests for the full feature flow (CC Ch.20)
- Manual testing checklist for UI/UX

### Step 7: Plan deployment and release
- Feature flags for safe rollout (DMLS Ch.6)
- Deployment order: backend first, then frontend
- Backward compatibility during deployment
- Rollback plan
- A/B test plan if the feature is experimental (MLDP Ch.5, DMLS Ch.9)

## 6. Output deliverable
A feature planning document covering: API contract, data layer changes, backend changes, frontend changes, testing strategy, deployment plan, and rollback plan.

## 7. Quality checklist
- [ ] API contract supports frontend data needs
- [ ] API evolution is backward compatible
- [ ] Data migration plan is zero-downtime (if needed)
- [ ] Error handling is defined at every layer (backend errors → frontend messaging)
- [ ] Loading states and empty states are planned
- [ ] Tests cover all layers (unit, integration, E2E)
- [ ] Feature flag is used for safe rollout
- [ ] Deployment order is defined (backend first, then frontend)
- [ ] Rollback plan exists
- [ ] Observability is added for the new feature

## 8. Common failure modes
- Designing the API without consulting the frontend team (API doesn't meet UI needs)
- Not accounting for backward compatibility during deployment
- Missing error states in the frontend (no error messaging for users)
- Data migration that requires downtime
- Forgetting to invalidate caches after data changes
- Frontend and backend deployed in the wrong order
- Not testing the full flow before merging

## 9. Dependencies on framework skills
- API Design (for API contract)
- Data Modeling (for data layer)
- Refactoring (for maintaining code quality)
- Testing and Verification (for test strategy)

## 10. Source books used
- Primary: Designing Web APIs (Ames, O'Hara, etc.)
- Support: The Pragmatic Programmer (Hunt & Thomas), Code Complete (McConnell), Web Scalability for Startup Engineers (Artasanchez & Bhalerao), Refactoring (Fowler)

## 11. Example of a good final output structure
```
# Feature Plan: User Profile Page

## API Contract
- `GET /v1/users/{id}/profile` → user profile response
- `PUT /v1/users/{id}/profile` → update profile

## Data Changes
- Add `avatar_url`, `bio`, `location` columns to `users` table
- Migration: add columns as nullable, backfill from event log

## Backend Changes
- ProfileService: get/update profile + avatar upload to S3
- Cache: invalidate user profile cache on update

## Frontend Changes
- ProfilePage component with editable fields
- Avatar upload widget
- Error state: "Failed to load profile" banner
- Loading state: skeleton loader

## Tests
- Unit: ProfileService business logic
- Integration: PUT /profile endpoint with S3 upload
- E2E: full profile edit flow

## Deployment
- Backend API changes first (backward compatible)
- Frontend next (feature-flagged)
- Rollback: revert frontend flag, revert backend if needed
```
