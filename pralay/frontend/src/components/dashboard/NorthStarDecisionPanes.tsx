import { FC } from 'react';
import { MapPin, AlertCircle, Clock, ShieldCheck, Home, Navigation, AlertTriangle } from 'lucide-react';
import { RiskAssessment } from '../../types/risk';

interface Props {
  assessment: RiskAssessment | null;
  onOpenCitizenCard: () => void;
}

export const NorthStarDecisionPanes: FC<Props> = ({ assessment, onOpenCitizenCard }) => {
  if (!assessment) {
    return (
      <div className="bg-slate-900 border border-slate-700 rounded-2xl p-8 text-center text-slate-400">
        Loading real-time compound risk assessment...
      </div>
    );
  }

  const getRiskColor = (lvl: string) => {
    switch (lvl) {
      case 'RED': return 'text-red-400 border-red-500/60 bg-red-950/40';
      case 'ORANGE': return 'text-amber-400 border-amber-500/60 bg-amber-950/40';
      case 'YELLOW': return 'text-yellow-300 border-yellow-500/60 bg-yellow-950/40';
      default: return 'text-emerald-400 border-emerald-500/60 bg-emerald-950/40';
    }
  };

  const getRiskBadge = (lvl: string) => {
    switch (lvl) {
      case 'RED': return 'bg-red-600 text-white animate-pulse';
      case 'ORANGE': return 'bg-amber-600 text-white';
      case 'YELLOW': return 'bg-yellow-500 text-slate-950';
      default: return 'bg-emerald-600 text-white';
    }
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-5 mb-6">
      {/* 1. WHERE IS THE RISK? */}
      <div className="bg-slate-900 border border-slate-800 hover:border-slate-700 rounded-2xl p-5 shadow-lg flex flex-col justify-between">
        <div>
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-black uppercase tracking-wider text-blue-400 flex items-center space-x-1.5">
              <MapPin className="w-3.5 h-3.5" />
              <span>1. Where is the Risk?</span>
            </span>
            <span className="text-xs bg-slate-800 text-slate-300 px-2 py-0.5 rounded font-mono">
              {assessment.district}
            </span>
          </div>

          <h3 className="text-2xl font-black text-white mt-3">
            {assessment.village_name}
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            {assessment.state} &bull; Lat {assessment.latitude.toFixed(4)}, Lon {assessment.longitude.toFixed(4)}
          </p>

          <div className="mt-4 space-y-2 text-xs">
            <div className="flex justify-between py-1 border-b border-slate-800 text-slate-300">
              <span>Population at Risk</span>
              <span className="font-bold text-white">{assessment.population_at_risk.toLocaleString()}</span>
            </div>
            <div className="flex justify-between py-1 border-b border-slate-800 text-slate-300">
              <span>Mean Slope Angle</span>
              <span className="font-bold text-white">{assessment.slope_degrees}° (Steep Hill)</span>
            </div>
            <div className="flex justify-between py-1 text-slate-300">
              <span>Sensor Health</span>
              <span className="font-semibold text-emerald-400">● {assessment.sensor_health_status}</span>
            </div>
          </div>
        </div>

        <div className="mt-4 pt-3 border-t border-slate-800 text-[11px] text-slate-500">
          Hyperlocal Village Catchment
        </div>
      </div>

      {/* 2. HOW SEVERE? */}
      <div className={`border rounded-2xl p-5 shadow-lg flex flex-col justify-between ${getRiskColor(assessment.risk_level)}`}>
        <div>
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-black uppercase tracking-wider flex items-center space-x-1.5">
              <AlertCircle className="w-3.5 h-3.5" />
              <span>2. How Severe?</span>
            </span>
            <span className={`text-xs font-black px-2.5 py-0.5 rounded-full ${getRiskBadge(assessment.risk_level)}`}>
              {assessment.risk_level}
            </span>
          </div>

          <div className="mt-3 flex items-baseline space-x-2">
            <span className="text-4xl font-black text-white tracking-tight">
              {assessment.compound_risk_score}
            </span>
            <span className="text-sm font-semibold text-slate-400">/ 100</span>
          </div>
          <p className="text-xs font-medium mt-1">
            Compound Risk Index (PRD §9/§10 Model)
          </p>

          {/* Sub-hazard breakdown */}
          <div className="mt-4 space-y-2">
            <div>
              <div className="flex justify-between text-xs font-semibold mb-1 text-slate-300">
                <span>Flash Flood Factor</span>
                <span>{assessment.flood_risk_score}/100</span>
              </div>
              <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                <div
                  className="bg-sky-500 h-full rounded-full"
                  style={{ width: `${assessment.flood_risk_score}%` }}
                />
              </div>
            </div>

            <div>
              <div className="flex justify-between text-xs font-semibold mb-1 text-slate-300">
                <span>Landslide Factor</span>
                <span>{assessment.landslide_risk_score}/100</span>
              </div>
              <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                <div
                  className="bg-amber-500 h-full rounded-full"
                  style={{ width: `${assessment.landslide_risk_score}%` }}
                />
              </div>
            </div>
          </div>
        </div>

        <div className="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between text-[11px] text-slate-400">
          <span>Primary: {assessment.primary_hazard}</span>
          <button
            onClick={onOpenCitizenCard}
            className="text-white underline hover:text-blue-300 font-semibold"
          >
            Citizen Card &rarr;
          </button>
        </div>
      </div>

      {/* 3. HOW SOON? */}
      <div className="bg-slate-900 border border-slate-800 hover:border-slate-700 rounded-2xl p-5 shadow-lg flex flex-col justify-between">
        <div>
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-black uppercase tracking-wider text-rose-400 flex items-center space-x-1.5">
              <Clock className="w-3.5 h-3.5" />
              <span>3. How Soon?</span>
            </span>
            <span className="text-[10px] bg-rose-950/80 text-rose-300 border border-rose-800 px-2 py-0.5 rounded font-mono font-semibold">
              PRD §12
            </span>
          </div>

          <div className="mt-3">
            <span className="text-3xl font-black text-white">
              {assessment.lead_time.minutes ? `${assessment.lead_time.minutes} mins` : '12+ hours'}
            </span>
            <p className="text-xs font-semibold text-rose-400 mt-1 uppercase tracking-wide">
              {assessment.lead_time.label}
            </p>
          </div>

          <div className="mt-4 bg-slate-800/60 p-3 rounded-xl border border-slate-700/60 text-xs">
            <span className="text-slate-400 block text-[11px] uppercase font-semibold">Projection Dynamics:</span>
            <p className="text-slate-200 mt-1 font-medium leading-relaxed">
              {assessment.lead_time.trend_description}
            </p>
            <div className="mt-2 text-[11px] text-slate-400 flex items-center justify-between pt-2 border-t border-slate-700">
              <span>Confidence:</span>
              <span className="font-bold text-white">{(assessment.lead_time.confidence_score * 100).toFixed(0)}%</span>
            </div>
          </div>
        </div>

        <div className="mt-4 pt-3 border-t border-slate-800 text-[11px] text-slate-500">
          Non-guaranteed decision support
        </div>
      </div>

      {/* 4. WHAT NOW? */}
      <div className="bg-slate-900 border border-slate-800 hover:border-slate-700 rounded-2xl p-5 shadow-lg flex flex-col justify-between">
        <div>
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-black uppercase tracking-wider text-emerald-400 flex items-center space-x-1.5">
              <ShieldCheck className="w-3.5 h-3.5" />
              <span>4. What Now?</span>
            </span>
            <span className="text-xs font-bold text-slate-400">
              {assessment.action.priority}
            </span>
          </div>

          <div className="mt-3 bg-emerald-950/30 border border-emerald-800/60 p-3 rounded-xl">
            <p className="text-xs font-bold text-emerald-200 leading-snug">
              {assessment.action.action}
            </p>
          </div>

          <div className="mt-3 space-y-2 text-xs">
            <div className="flex items-start space-x-2 text-slate-300">
              <Home className="w-4 h-4 text-emerald-400 flex-shrink-0 mt-0.5" />
              <div>
                <span className="font-bold text-white block truncate">
                  {assessment.action.nearest_shelter_name}
                </span>
                <span className="text-[11px] text-slate-400">
                  {assessment.action.shelter_distance_km} km away &bull; High Ridge Zone
                </span>
              </div>
            </div>

            <div className="flex items-start space-x-2 text-slate-300">
              <Navigation className="w-4 h-4 text-sky-400 flex-shrink-0 mt-0.5" />
              <div className="text-[11px]">
                <span className="font-bold text-sky-300 block">
                  Route: {assessment.action.evacuation_route_id}
                </span>
                <span className="text-slate-400">
                  {assessment.action.safe_path_instructions}
                </span>
              </div>
            </div>
          </div>
        </div>

        <div className="mt-4 pt-3 border-t border-slate-800 flex items-center justify-between text-[11px]">
          <span className="text-amber-400 font-semibold flex items-center space-x-1">
            <AlertTriangle className="w-3 h-3" />
            <span>Avoid Valley Floor</span>
          </span>
          <span className="text-slate-500 font-mono">1077 NDRF</span>
        </div>
      </div>
    </div>
  );
};
