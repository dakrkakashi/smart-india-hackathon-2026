import { FC } from 'react';
import { MapPin, Users, Activity, Mountain } from 'lucide-react';
import { RiskAssessment } from '../../types/risk';

interface Props {
  assessments: RiskAssessment[];
  selectedVillageId: number;
  onSelectVillage: (villageId: number) => void;
}

export const VillageCatchmentList: FC<Props> = ({
  assessments,
  selectedVillageId,
  onSelectVillage
}) => {
  const getBadgeStyle = (lvl: string) => {
    switch (lvl) {
      case 'RED': return 'bg-red-600 text-white';
      case 'ORANGE': return 'bg-amber-600 text-white';
      case 'YELLOW': return 'bg-yellow-500 text-slate-950';
      default: return 'bg-emerald-600 text-white';
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3 mb-4">
        <div>
          <h3 className="text-base font-bold text-white flex items-center space-x-2">
            <MapPin className="w-4 h-4 text-blue-400" />
            <span>Pilot Catchment Villages (Chamoli & Rudraprayag)</span>
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Click any village to view real-time localized compound assessment
          </p>
        </div>
        <span className="text-xs font-semibold text-slate-400 bg-slate-800 px-2.5 py-1 rounded-full">
          {assessments.length} Active Pilot Sectors
        </span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
        {assessments.map((village) => {
          const isSelected = village.village_id === selectedVillageId;
          return (
            <button
              key={village.village_id}
              onClick={() => onSelectVillage(village.village_id)}
              className={`p-4 rounded-xl text-left transition-all border ${
                isSelected
                  ? 'bg-blue-950/40 border-blue-500 ring-2 ring-blue-500/40'
                  : 'bg-slate-800/60 border-slate-700/60 hover:border-slate-600 hover:bg-slate-800'
              }`}
            >
              <div className="flex items-center justify-between">
                <span className="text-xs font-mono text-slate-400">{village.district}</span>
                <span className={`text-[10px] font-black px-2 py-0.5 rounded-full ${getBadgeStyle(village.risk_level)}`}>
                  {village.risk_level}
                </span>
              </div>

              <h4 className="text-base font-bold text-white mt-1.5">{village.village_name}</h4>

              <div className="mt-2.5 space-y-1 text-xs text-slate-400">
                <div className="flex items-center justify-between">
                  <span className="flex items-center space-x-1">
                    <Activity className="w-3 h-3 text-slate-400" />
                    <span>Risk:</span>
                  </span>
                  <span className="font-bold text-white">{village.compound_risk_score}/100</span>
                </div>

                <div className="flex items-center justify-between">
                  <span className="flex items-center space-x-1">
                    <Users className="w-3 h-3 text-slate-400" />
                    <span>Pop:</span>
                  </span>
                  <span className="font-semibold text-slate-300">{village.population_at_risk}</span>
                </div>

                <div className="flex items-center justify-between">
                  <span className="flex items-center space-x-1">
                    <Mountain className="w-3 h-3 text-slate-400" />
                    <span>Slope:</span>
                  </span>
                  <span className="font-semibold text-slate-300">{village.slope_degrees}°</span>
                </div>
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
};
