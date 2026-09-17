import React from 'react';
import { CircleMarker, Popup, Tooltip } from 'react-leaflet';
import { RiskAssessment } from '../../types/risk';
import { getRiskHex, RISK_BADGE_CLASSES } from '../../lib/riskColors';
import { AlertTriangle, Users, Activity, Clock, ShieldCheck, Mountain } from 'lucide-react';

interface Props {
  assessments: RiskAssessment[];
  selectedVillageId: number;
  onSelectVillage: (id: number) => void;
}

const SEVERITY_RADIUS: Record<string, number> = {
  RED: 14,
  ORANGE: 12,
  YELLOW: 10,
  GREEN: 8,
};

export const VillageRiskMarkers: React.FC<Props> = ({
  assessments,
  selectedVillageId,
  onSelectVillage,
}) => {
  return (
    <>
      {assessments.map((village) => {
        const isSelected = village.village_id === selectedVillageId;
        const color = getRiskHex(village.risk_level);
        const radius = (SEVERITY_RADIUS[village.risk_level] || 8) + (isSelected ? 4 : 0);

        return (
          <React.Fragment key={village.village_id}>
            {/* Outer highlight ring for selected village */}
            {isSelected && (
              <CircleMarker
                center={[village.latitude, village.longitude]}
                radius={radius + 8}
                pathOptions={{
                  color: color,
                  fillColor: color,
                  fillOpacity: 0.2,
                  weight: 2,
                  dashArray: '4, 4',
                }}
              />
            )}

            <CircleMarker
              center={[village.latitude, village.longitude]}
              radius={radius}
              pathOptions={{
                color: isSelected ? '#ffffff' : color,
                fillColor: color,
                fillOpacity: 0.85,
                weight: isSelected ? 3 : 1.5,
              }}
              eventHandlers={{
                click: () => onSelectVillage(village.village_id),
              }}
            >
              <Tooltip direction="top" offset={[0, -10]} opacity={0.95}>
                <div className="text-xs font-bold text-slate-900 flex items-center gap-1.5">
                  <span
                    className="w-2 h-2 rounded-full inline-block"
                    style={{ backgroundColor: color }}
                  />
                  <span>{village.village_name}</span>
                  <span className="text-[10px] px-1 rounded bg-slate-200">
                    {village.risk_level}
                  </span>
                </div>
              </Tooltip>

              <Popup className="custom-dark-popup">
                <div className="p-2 min-w-[260px] text-slate-100 font-sans space-y-2">
                  <div className="flex items-center justify-between border-b border-slate-700 pb-1.5">
                    <div>
                      <h4 className="font-bold text-base text-white">{village.village_name}</h4>
                      <p className="text-xs text-slate-400">
                        {village.district}, {village.state}
                      </p>
                    </div>
                    <span
                      className={`text-xs px-2 py-0.5 rounded-full font-bold ${
                        RISK_BADGE_CLASSES[village.risk_level]
                      }`}
                    >
                      {village.risk_level}
                    </span>
                  </div>

                  <div className="grid grid-cols-2 gap-2 text-xs py-1">
                    <div className="bg-slate-800/80 p-1.5 rounded">
                      <span className="text-slate-400 block text-[10px] uppercase">
                        Compound Risk
                      </span>
                      <span className="font-extrabold text-sm" style={{ color }}>
                        {village.compound_risk_score.toFixed(1)} / 100
                      </span>
                    </div>
                    <div className="bg-slate-800/80 p-1.5 rounded">
                      <span className="text-slate-400 block text-[10px] uppercase">
                        Primary Hazard
                      </span>
                      <span className="font-bold text-slate-200 text-xs">
                        {village.primary_hazard}
                      </span>
                    </div>
                  </div>

                  <div className="space-y-1 text-xs text-slate-300">
                    <div className="flex items-center gap-1.5">
                      <Clock className="w-3.5 h-3.5 text-amber-400 shrink-0" />
                      <span>
                        Lead Time:{' '}
                        <strong>
                          {village.lead_time.minutes
                            ? `${village.lead_time.minutes} mins`
                            : 'Monitoring'}
                        </strong>
                      </span>
                    </div>

                    <div className="flex items-center gap-1.5">
                      <Users className="w-3.5 h-3.5 text-blue-400 shrink-0" />
                      <span>
                        Population at Risk: <strong>{village.population_at_risk}</strong>
                      </span>
                    </div>

                    <div className="flex items-center gap-1.5">
                      <Mountain className="w-3.5 h-3.5 text-purple-400 shrink-0" />
                      <span>
                        Slope: <strong>{village.slope_degrees}&deg;</strong> | Rain 1h:{' '}
                        <strong>{village.rainfall_1h_mm} mm</strong>
                      </span>
                    </div>

                    <div className="flex items-center gap-1.5">
                      <Activity className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                      <span className="truncate">
                        Sensors: <strong>{village.sensor_health_status}</strong>
                      </span>
                    </div>
                  </div>

                  {village.action?.action && (
                    <div className="bg-slate-800/90 border-l-2 border-amber-400 p-2 text-[11px] text-amber-200 rounded-r">
                      <div className="flex items-center gap-1 font-semibold text-amber-300 mb-0.5">
                        <AlertTriangle className="w-3 h-3 shrink-0" />
                        <span>Directive</span>
                      </div>
                      <p className="line-clamp-2">{village.action.action}</p>
                    </div>
                  )}

                  <button
                    onClick={() => onSelectVillage(village.village_id)}
                    className="w-full mt-2 py-1.5 px-3 bg-blue-600 hover:bg-blue-500 text-white rounded text-xs font-bold transition flex items-center justify-center gap-1.5"
                  >
                    <ShieldCheck className="w-3.5 h-3.5" />
                    <span>
                      {isSelected ? 'Route Active' : 'Select & Show Evacuation Route'}
                    </span>
                  </button>
                </div>
              </Popup>
            </CircleMarker>
          </React.Fragment>
        );
      })}
    </>
  );
};
