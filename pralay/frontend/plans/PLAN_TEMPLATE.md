# [FEATURE_NAME] — Implementation Plan

| | |
|---|---|
| **Status** | PENDING / IN_PROGRESS / BLOCKED / COMPLETED |
| **Phase** | 1 – Foundation / 2 – ML Validation / 3 – Field Pilot / 4 – Scaling |
| **Priority** | P0 / P1 / P2 |
| **Depends On** | _List any plan, PR, or backend endpoint this depends on_ |
| **Author** | _Team / Role_ |
| **Created** | _YYYY-MM-DD_ |

## 1. Context & Problem Statement

_Describe the feature, why it is needed, and the user/stakeholder outcome it delivers._

## 2. Goals & Non-Goals

**Goals**
- _
- _

**Non-Goals**
- _Explicitly out of scope for this plan_

## 3. Current State Analysis

_Summarize the existing code, types, routes, stores, and API endpoints this feature touches. Always reference exact file paths._

## 4. Technical Approach

_Design decisions: libraries, patterns, state management, data flow. Note the stack constraints (React+TS+Vite, FastAPI v1 router, WebSocket, PostGIS, etc.)._

## 5. API Contract

| Method | Endpoint | Request | Response | Status When Down |
|---|---|---|---|---|
| GET | `/api/v1/...` | _params_ | _schema_ | _fallback behavior_ |

## 6. Implementation Steps

> Actionable checkboxes with exact file paths. Complete each step before marking it.

- [ ] **Step 1 — <Title>**
  - [ ] Create `src/.../file.ts`
    - _what to implement_
  - [ ] Create `src/.../file.tsx`
    - _what to implement_

## 7. Testing & Verification

- [ ] `npm run lint`
- [ ] `npm run build` (runs `tsc && vite build`)
- [ ] Manual: `npm run dev` → URL, expected behavior
- [ ] Backend tests: `pytest` (if backend changed)

## 8. Risks & Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| _Sensor failure / data gap_ |  | _Show sensor_health_status & data_sources_available; degrade gracefully_ |
| _Network loss / API down_ |  | _Mock fallback data; cache last-good payload_ |
| _Alert fatigue_ |  | _Dedupe/cooldown; severity-ranked UI_ |
| _Govt-cloud compliance_ |  | _No PII; aggregated village-level data only_ |

## 9. Acceptance Criteria

- [ ] _

## 10. Rollback Plan

_How to revert if this feature regresses (remove route, restore component, revert commit)._