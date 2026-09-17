# GIS Risk Map Page (`/map`) — Implementation Plan

| | |
|---|---|
| **Status** | COMPLETED ✅ |
| **Phase** | 1 – Foundation & Interactive Spatial GIS |
| **Priority** | P1 |
| **Depends On** | Backend v1 API: `/api/v1/predictions/catchments`, `/api/v1/evacuations/shelters`, `/api/v1/evacuations/route/{village_id}`, `/api/v1/alerts` (already implemented + mock fallbacks) |
| **Author** | Frontend Team |
| **Created** | 2026-09-17 |
| **Completed** | 2026-09-17 |

## 1. Summary of Execution

The flagship Phase 1 GIS spatial deliverable — the **GIS Risk Map** — has been fully implemented, integrated, and verified at `/map`:
1. **Registered Route**: Added `<Route path="map" element={<RiskMap />} />` in [`src/App.tsx`](file:///D:/Shivam%20Project/SIH%20PROJECT/pralay/frontend/src/App.tsx), activating the existing `Sidebar.tsx` "Risk Map" NavLink.
2. **Interactive Leaflet Engine**: Configured React Leaflet with OpenStreetMap tiles, dark theme filter, zoom controls, and custom dark popups.
3. **Hyperlocal Village Markers**: Color-coded `CircleMarker` with severity radius (RED 14px, ORANGE 12px, YELLOW 10px, GREEN 8px), tooltips, and interactive popups detailing compound risk, population at risk, slope, rainfall, and telemetry health.
4. **Relief Shelters**: Color-coded shelter markers with live capacity status, occupancy bars, elevation data, facility tags (water, power, first-aid), and contact details.
5. **Safe Evacuation Route Polyline**: Glowing cyan polyline with dashed corridor connecting assembly point -> high-elevation ridge bypass -> destination shelter, avoiding riverbed hazard zones.
6. **Filter Controls**: Multi-parameter filter panel for District (Chamoli/Rudraprayag), Primary Hazard, and Shelter toggle.
7. **Resilient Data Layer**: Zustand store `useMapStore` and Axios client with automated fallback to calibrated pilot data when offline.
8. **Verification**: 
   - `npm run lint` — 0 warnings.
   - `npm run build` — Clean production bundle (`dist/index.html`, CSS, JS chunks).
   - `pytest backend/tests` — 14/14 passed.
