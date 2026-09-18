import { FC } from 'react';
import { Users, Mountain, Shield } from 'lucide-react';
import { initialAssessments } from '../data/mockAssessments';

export const Regions: FC = () => {
  return (
    <div className="p-6 max-w-[1600px] mx-auto space-y-6">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 bg-slate-900 border border-slate-800 p-5 rounded-2xl shadow-lg">
        <div>
          <span className="text-xs font-black tracking-widest text-emerald-400 uppercase bg-emerald-950/60 border border-emerald-800/80 px-2.5 py-1 rounded-full">
            Pilot Sectors & Demographics &bull; PRD §3
          </span>
          <h1 className="text-2xl font-black text-white mt-2">
            Target Pilot Catchments & Vulnerability Profiles
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Chamoli & Rudraprayag upper catchment river valleys, elevation gradients, and vulnerable demographic footprints
          </p>
        </div>

        <div className="flex items-center gap-2 bg-slate-800 border border-slate-700 px-3 py-1.5 rounded-xl text-xs text-slate-300">
          <Shield className="w-4 h-4 text-blue-400" />
          <span>5 Priority Pilot Villages Instrumented</span>
        </div>
      </div>

      {/* Villages Card Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {initialAssessments.map((village) => (
          <div
            key={village.village_id}
            className="bg-slate-900 border border-slate-800 hover:border-slate-700 rounded-2xl p-5 shadow-lg flex flex-col justify-between"
          >
            <div>
              <div className="flex items-center justify-between">
                <span className="text-xs font-mono text-slate-400">{village.district}, {village.state}</span>
                <span
                  className={`text-[10px] font-black px-2 py-0.5 rounded-full ${
                    village.risk_level === 'RED'
                      ? 'bg-red-600 text-white'
                      : village.risk_level === 'ORANGE'
                      ? 'bg-amber-600 text-white'
                      : village.risk_level === 'YELLOW'
                      ? 'bg-yellow-500 text-slate-950'
                      : 'bg-emerald-600 text-white'
                  }`}
                >
                  {village.risk_level} STATUS
                </span>
              </div>

              <h3 className="text-xl font-black text-white mt-2">
                {village.village_name}
              </h3>
              <p className="text-xs text-slate-400">
                Lat {village.latitude.toFixed(4)}, Lon {village.longitude.toFixed(4)}
              </p>

              <div className="mt-4 space-y-2 text-xs bg-slate-950/60 p-3 rounded-xl border border-slate-800">
                <div className="flex justify-between py-1 border-b border-slate-800/80 text-slate-300">
                  <span className="flex items-center gap-1.5">
                    <Users className="w-3.5 h-3.5 text-blue-400" />
                    <span>Population at Risk</span>
                  </span>
                  <span className="font-bold text-white">{village.population_at_risk.toLocaleString()}</span>
                </div>

                <div className="flex justify-between py-1 border-b border-slate-800/80 text-slate-300">
                  <span className="flex items-center gap-1.5">
                    <Mountain className="w-3.5 h-3.5 text-amber-400" />
                    <span>Terrain Slope</span>
                  </span>
                  <span className="font-bold text-white">{village.slope_degrees}&deg;</span>
                </div>

                <div className="flex justify-between py-1 text-slate-300">
                  <span className="flex items-center gap-1.5">
                    <Shield className="w-3.5 h-3.5 text-emerald-400" />
                    <span>Safe Shelter</span>
                  </span>
                  <span className="font-semibold text-slate-200 text-right truncate max-w-[150px]">
                    {village.action.nearest_shelter_name}
                  </span>
                </div>
              </div>
            </div>

            <div className="mt-4 pt-3 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
              <span>Evac Route: <strong className="text-sky-300">{village.action.evacuation_route_id}</strong></span>
              <span className="text-slate-500">{village.action.shelter_distance_km} km</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Regions;
