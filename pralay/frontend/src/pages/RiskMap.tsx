import { useEffect, useMemo } from 'react';
import { useMapStore } from '../store/useMapStore';
import { RiskMapView } from '../components/map/RiskMapView';
import { MapFilters } from '../components/map/MapFilters';
import { getRiskHex, RISK_BADGE_CLASSES } from '../lib/riskColors';
import { MapPin, Navigation, Clock, Home, AlertTriangle, Radio } from 'lucide-react';

export default function RiskMap() {
  const {
    assessments,
    shelters,
    selectedVillageId,
    route,
    filters,
    loading,
    isUsingFallback,
    loadMapData,
    selectVillage,
    setFilters,
    refresh,
  } = useMapStore();

  useEffect(() => {
    loadMapData();
  }, [loadMapData]);

  // Filter assessments based on active filters
  const filteredAssessments = useMemo(() => {
    return assessments.filter((village) => {
      if (filters.district !== 'ALL' && village.district.toLowerCase() !== filters.district.toLowerCase()) {
        return false;
      }
      if (filters.hazard !== 'ALL' && village.primary_hazard !== filters.hazard) {
        return false;
      }
      return true;
    });
  }, [assessments, filters]);

  const selectedVillage =
    assessments.find((v) => v.village_id === selectedVillageId) || assessments[0];

  return (
    <div className="p-6 max-w-[1600px] mx-auto space-y-6">
      {/* Page Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 bg-slate-900 border border-slate-800 p-5 rounded-2xl shadow-lg">
        <div>
          <span className="text-xs font-black tracking-widest text-sky-400 uppercase bg-sky-950/60 border border-sky-800/80 px-2.5 py-1 rounded-full">
            GIS Risk & Evacuation Engine &bull; PS 26192
          </span>
          <h1 className="text-2xl font-black text-white mt-2">
            Geospatial Hazard & Safe Evacuation Map
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Real-Time Village Catchment Heatmap, Relief Shelters & Ridge Bypass Routing
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 bg-slate-800 border border-slate-700 px-3 py-1.5 rounded-xl text-xs">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            <span className="text-slate-300 font-medium">GIS Engine Active</span>
          </div>
        </div>
      </div>

      {/* Offline/Fallback Banner */}
      {isUsingFallback && (
        <div className="bg-amber-950/40 border border-amber-800/80 text-amber-200 text-xs px-4 py-2.5 rounded-xl flex items-center justify-between shadow-md">
          <div className="flex items-center gap-2">
            <Radio className="w-4 h-4 text-amber-400 animate-pulse" />
            <span>
              <strong>Local Deterministic Mode:</strong> Live API unreachable, rendering calibrated
              pilot catchment data for Chamoli &amp; Rudraprayag.
            </span>
          </div>
          <button
            onClick={refresh}
            className="text-[11px] underline font-bold hover:text-white"
          >
            Retry Connection
          </button>
        </div>
      )}

      {/* Map Filter Controls */}
      <MapFilters
        filters={filters}
        onFilterChange={setFilters}
        onRefresh={refresh}
        loading={loading}
        totalVillages={assessments.length}
        filteredVillages={filteredAssessments.length}
      />

      {/* Interactive Leaflet Map */}
      <RiskMapView
        assessments={filteredAssessments}
        shelters={shelters}
        selectedVillageId={selectedVillageId}
        route={route}
        showShelters={filters.showShelters}
        onSelectVillage={selectVillage}
      />

      {/* Selected Village & Active Evacuation Corridor Summary */}
      {selectedVillage && (
        <div className="bg-slate-900 border border-slate-800 p-5 rounded-2xl shadow-lg space-y-4">
          <div className="flex flex-wrap items-center justify-between border-b border-slate-800 pb-3 gap-3">
            <div className="flex items-center gap-3">
              <div
                className="w-10 h-10 rounded-xl flex items-center justify-center font-bold text-white shadow-md"
                style={{ backgroundColor: getRiskHex(selectedVillage.risk_level) }}
              >
                <MapPin className="w-5 h-5" />
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <h3 className="text-lg font-bold text-white">{selectedVillage.village_name}</h3>
                  <span
                    className={`text-xs px-2.5 py-0.5 rounded-full font-bold ${
                      RISK_BADGE_CLASSES[selectedVillage.risk_level]
                    }`}
                  >
                    {selectedVillage.risk_level} RISK ({selectedVillage.compound_risk_score.toFixed(1)}/100)
                  </span>
                </div>
                <p className="text-xs text-slate-400">
                  {selectedVillage.district} District, {selectedVillage.state} &bull; Population at Risk:{' '}
                  <strong className="text-slate-200">{selectedVillage.population_at_risk}</strong>
                </p>
              </div>
            </div>

            <div className="flex items-center gap-4 text-xs">
              <div className="bg-slate-800/80 px-3 py-2 rounded-xl border border-slate-700">
                <span className="text-slate-400 block text-[10px] uppercase font-bold">
                  Estimated Lead Time
                </span>
                <span className="text-amber-400 font-extrabold flex items-center gap-1 text-sm mt-0.5">
                  <Clock className="w-3.5 h-3.5" />
                  {selectedVillage.lead_time.minutes
                    ? `${selectedVillage.lead_time.minutes} Mins`
                    : 'Monitoring Status'}
                </span>
              </div>

              <div className="bg-slate-800/80 px-3 py-2 rounded-xl border border-slate-700">
                <span className="text-slate-400 block text-[10px] uppercase font-bold">
                  Rainfall (1h / 24h)
                </span>
                <span className="text-blue-300 font-bold text-sm mt-0.5">
                  {selectedVillage.rainfall_1h_mm} mm / {selectedVillage.rainfall_24h_mm} mm
                </span>
              </div>
            </div>
          </div>

          {/* Safe Evacuation Route Card */}
          {route && (
            <div className="bg-slate-950/70 border border-sky-900/50 p-4 rounded-xl space-y-3">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <div className="flex items-center gap-2 text-sky-400 font-bold text-xs">
                  <Navigation className="w-4 h-4" />
                  <span>Assigned Safe Route: {route.route_id}</span>
                </div>
                <div className="flex items-center gap-3 text-xs text-slate-300">
                  <span>
                    Distance: <strong className="text-white">{route.total_distance_km} km</strong>
                  </span>
                  <span>
                    Transit Time: <strong className="text-sky-300">~{route.estimated_transit_minutes} mins</strong>
                  </span>
                </div>
              </div>

              <p className="text-xs text-slate-200 leading-relaxed bg-slate-900/90 p-3 rounded-lg border border-slate-800">
                {route.instructions}
              </p>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs pt-1">
                <div className="flex items-start gap-2 bg-slate-900/60 p-2.5 rounded-lg border border-slate-800">
                  <Home className="w-4 h-4 text-emerald-400 mt-0.5 shrink-0" />
                  <div>
                    <span className="text-slate-400 block text-[10px] uppercase">Destination Shelter</span>
                    <span className="font-semibold text-white">{route.destination_shelter_name}</span>
                  </div>
                </div>

                {route.avoid_sectors && route.avoid_sectors.length > 0 && (
                  <div className="flex items-start gap-2 bg-red-950/30 p-2.5 rounded-lg border border-red-900/40">
                    <AlertTriangle className="w-4 h-4 text-red-400 mt-0.5 shrink-0" />
                    <div>
                      <span className="text-red-400 block text-[10px] uppercase font-bold">Avoid Valley Sectors</span>
                      <span className="text-red-200 text-[11px]">{route.avoid_sectors.join(', ')}</span>
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
