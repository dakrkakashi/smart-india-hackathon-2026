import React from 'react';

export const RiskLegend: React.FC = () => {
  return (
    <div className="absolute bottom-5 left-5 z-[1000] bg-slate-900/90 backdrop-blur-md border border-slate-700/80 p-3 rounded-xl shadow-2xl text-xs text-slate-200 max-w-[220px] pointer-events-auto">
      <div className="font-bold text-white text-[11px] uppercase tracking-wider mb-2 border-b border-slate-700 pb-1">
        Spatial Risk & Evac Legend
      </div>

      <div className="space-y-1.5 text-[11px]">
        <div className="flex items-center gap-2">
          <span className="w-3 h-3 rounded-full bg-red-600 border border-white shrink-0" />
          <span>RED &bull; Critical (Evacuate)</span>
        </div>

        <div className="flex items-center gap-2">
          <span className="w-3 h-3 rounded-full bg-amber-500 border border-white shrink-0" />
          <span>ORANGE &bull; High (Prepare)</span>
        </div>

        <div className="flex items-center gap-2">
          <span className="w-3 h-3 rounded-full bg-yellow-400 border border-slate-900 shrink-0" />
          <span>YELLOW &bull; Moderate (Watch)</span>
        </div>

        <div className="flex items-center gap-2">
          <span className="w-3 h-3 rounded-full bg-emerald-600 border border-white shrink-0" />
          <span>GREEN &bull; Low (Monitoring)</span>
        </div>

        <div className="border-t border-slate-700/80 pt-1.5 mt-1.5 space-y-1.5">
          <div className="flex items-center gap-2">
            <span className="w-3 h-3 rounded-full bg-sky-600 border border-white flex items-center justify-center text-[7px] shrink-0">
              🏠
            </span>
            <span className="text-sky-300">Relief Shelter</span>
          </div>

          <div className="flex items-center gap-2">
            <div className="w-4 h-0.5 border-t-2 border-dashed border-sky-400 shrink-0" />
            <span className="text-sky-300">Safe Evacuation Route</span>
          </div>
        </div>
      </div>
    </div>
  );
};
