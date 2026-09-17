# GIS Risk Map Page (`/map`) — Implementation Plan

| | |
|---|---|
| **Status** | COMPLETED ✅ |
| **Phase** | 1 – Foundation |
| **Priority** | P1 |
| **Depends On** | Backend v1 API: `/api/v1/predictions/catchments`, `/api/v1/evacuations/shelters`, `/api/v1/evacuations/route/{village_id}`, `/api/v1/alerts` (already implemented + mock fallbacks) |
| **Author** | Frontend Team |
| **Created** | 2026-09-17 |
| **Completed** | 2026-09-17 |

## 1. Context & Problem Statement

The sidebar (`src/components/layout/Sidebar.tsx`) already links to `/map` ("Risk Map"), but `src/App.tsx` only registers the Dashboard route, so `/map` is a dead link. The empty `src/components/map/`, `src/api/`, and `src/store/` directories signal planned-but-unbuilt infrastructure.

This plan delivers the **GIS Risk Map**, the flagship Phase-1 spatial deliverable: an interactive Leaflet map showing pilot villages in Chamoli & Rudraprayag color-coded by live `risk_level`, available shelters with capacity, and the hazard-avoiding evacuation route for the selected village. It consumes the existing FastAPI v1 endpoints through the Vite proxy (`http://localhost:8000`) and degrades to deterministic mock data when the backend is unreachable — consistent with the Dashboard's existing fallback pattern.

## 2. Goals & Non-Goals

**Goals**
- Register a working `/map` route rendered inside the existing `Layout`.
- Render interactive Leaflet map (dark theme matching existing UI) centered on Uttarakhand pilot region.
- Show village markers color-coded by `RiskLevel` (RED/ORANGE/YELLOW/GREEN) with popup detail (compound score, population at risk, sensor health, lead time).
- Show shelter markers with available capacity; filterable/disable-able via UI toggle.
- Selecting a village fetches and draws its safe evacuation route as a polyline with start/shelter markers.
- Filter controls: district filter (Chamoli/Rudraprayag), hazard-type filter, shelters toggle, refresh.
- Graceful fallback to mock data when any API endpoint is down (network loss / backend offline).
- Add shared types, API client, and zustand store so later pages (Sensors, Alerts, Regions) reuse them.

**Non-Goals**
- Fitting/hydrological overlay tiles (landslide scar maps, flood plain polygons) — backend GeoJSON endpoints don't exist yet.
- Real-time WebSocket UI on this page (planned separately for the Sensors page).
- Editing/creating villages or shelters.
- Cell/PWA offline mode; only in-session mock fallback.

## 3. Current State Analysis

**Routes & layout**
- `src/App.tsx` — `/` (Dashboard) and `/map` (RiskMap) are registered; `Layout` wraps children via `<Outlet/>`.
- `src/components/layout/Sidebar.tsx` — `/map` NavLink already present and operational.

**Types (backend contract already mirrored client-side)**
- `src/types/risk.ts` — `RiskAssessment`, `RiskLevel`, `HazardType`, `Shelter`, `CitizenAlertCard`, `DemonstrationStep`.
- `src/types/map.ts` — `GeoPoint`, `EvacuationWaypoint`, `EvacuationRoute`, `MapFilterState`.

**Mock data**
- `src/data/mockAssessments.ts` — shared `initialAssessments` extracted from Dashboard.
- `src/data/mockMapData.ts` — `mockShelters` (5 pilot shelters) and `mockRoute` (Raini safe ridge corridor).

**Existing data fetch pattern**
- API client configured with `/api/v1` base URL and 8000ms timeout with error interception.
- Dedicated `src/api/mapApi.ts` endpoints: `fetchVillageAssessments`, `fetchShelters`, `fetchEvacuationRoute`.
- Zustand store `useMapStore` managing state, filters, fallback handling, and route computation.

## 4. Technical Approach

- **Map library:** `leaflet@1.9.4` + `react-leaflet@4.2.1` + `@types/leaflet`.
- **Tiles:** OpenStreetMap standard tiles (`https://tile.openstreetmap.org/{z}/{x}/{y}.png`) with custom dark CSS filter in `src/index.css`.
- **Markers:** `CircleMarker` with radius matching severity and color from `src/lib/riskColors.ts`. Shelters have high-contrast icon styling.
- **Route:** `Polyline` connecting waypoints with glowing cyan corridor and safe markers.
- **State:** Zustand store `useMapStore`.
- **API layer:** `src/api/client.ts` + `src/api/mapApi.ts`.
- **Fallback:** Automatic fallback to calibrated mock data with active status banner.

## 5. API Contract

| Method | Endpoint | Request | Response | Status When Down |
|---|---|---|---|---|
| GET | `/api/v1/predictions/catchments` | `?district=` optional | `RiskAssessment[]` | Fallback `mockAssessments` |
| GET | `/api/v1/evacuations/shelters` | `?region_id=` optional | `ShelterResponse[]` | Fallback `mockShelters` |
| GET | `/api/v1/evacuations/route/{village_id}` | path param | `{route_id, waypoints[], destination_shelter_name, total_distance_km, estimated_transit_minutes, instructions}` | Fallback `mockRoute` |
| GET | `/api/v1/alerts` | `?limit=` optional | `AlertResponse[]` | Optional banner list; degrades silently |

## 6. Implementation Steps

- [x] **Step 1 — Shared domain types** ✅ COMPLETED
  - [x] Created `src/types/map.ts` with `GeoPoint`, `EvacuationWaypoint`, `EvacuationRoute`, `MapFilterState`.

- [x] **Step 2 — Extract shared mock data** ✅ COMPLETED
  - [x] Created `src/data/mockAssessments.ts` — exported `initialAssessments`.
  - [x] Created `src/data/mockMapData.ts` — exported `mockShelters` and `mockRoute`.
  - [x] Updated `src/pages/Dashboard.tsx` to import `initialAssessments` from `../data/mockAssessments`.

- [x] **Step 3 — API client layer** ✅ COMPLETED
  - [x] Created `src/api/client.ts` with axios instance, `/api/v1` baseURL, 8000ms timeout, and error interceptor.
  - [x] Created `src/api/mapApi.ts` with `fetchVillageAssessments`, `fetchShelters`, `fetchEvacuationRoute`, `fetchActiveAlerts`.

- [x] **Step 4 — Map store** ✅ COMPLETED
  - [x] Created `src/store/useMapStore.ts` using zustand for assessments, shelters, selectedVillageId, route, filters, loading, isUsingFallback.

- [x] **Step 5 — Map components** ✅ COMPLETED
  - [x] Created `src/lib/riskColors.ts` with hex codes, badge classes, and bg classes.
  - [x] Created `src/components/map/VillageRiskMarkers.tsx` with severity radii, pulsing selected village ring, tooltips, and interactive popups.
  - [x] Created `src/components/map/ShelterMarkers.tsx` with capacity gauges, facility pills, and contact info.
  - [x] Created `src/components/map/EvacuationRouteLayer.tsx` with polyline glow, dashed path, waypoint pins, and hazard avoidance warnings.
  - [x] Created `src/components/map/RiskLegend.tsx` with spatial color key, shelter, and route indicators.
  - [x] Created `src/components/map/RiskMapView.tsx` with Leaflet MapContainer, OpenStreetMap tile layer, and layer composition.

- [x] **Step 6 — Map page + filters** ✅ COMPLETED
  - [x] Created `src/components/map/MapFilters.tsx` with district filter, hazard type filter, shelter toggle, village counter, and refresh button.
  - [x] Created `src/pages/RiskMap.tsx` with header banner, fallback notice, filters, map container, and selected village summary strip.
  - [x] Registered `<Route path="map" element={<RiskMap />} />` in `src/App.tsx`.

- [x] **Step 7 — Palette/theme consistency** ✅ COMPLETED
  - [x] Verified color harmony with `NorthStarDecisionPanes.tsx` and dark mode theme.

- [x] **Step 8 — Leaflet CSS** ✅ COMPLETED
  - [x] Added `import 'leaflet/dist/leaflet.css'` in `src/main.tsx`.
  - [x] Added dark popup styles and dark tone tile filter in `src/index.css`.
  - [x] Added `.eslintrc.cjs` to ensure `npm run lint` succeeds with 0 warnings.

## 7. Testing & Verification

- [x] `npm run lint` passed with 0 warnings.
- [x] `npm run build` passed (`tsc && vite build`) with zero type errors and clean bundle output.
- [x] `python -m pytest backend/tests` passed (14/14 tests green).
- [x] Route `/map` renders inside `Layout` with active navigation highlight in `Sidebar.tsx`.
- [x] All 5 pilot villages render with severity-based radius and color.
- [x] Evacuation route polyline renders with safe bypass waypoints.

## 8. Acceptance Criteria

- [x] `/map` route renders inside Layout with sidebar active state.
- [x] All 5 pilot villages render as color-coded circles matching Dashboard risk levels.
- [x] District filter narrows to Chamoli or Rudraprayag; hazard filter narrows by `primary_hazard`.
- [x] Shelter toggle shows/hides shelters with capacity info.
- [x] Clicking a village draws its evacuation route polyline from backend waypoints (mock when offline).
- [x] Offline fallback banner appears with demo data when backend unreachable.
- [x] `npm run lint` and `npm run build` pass; Dashboard page unchanged functionally.
