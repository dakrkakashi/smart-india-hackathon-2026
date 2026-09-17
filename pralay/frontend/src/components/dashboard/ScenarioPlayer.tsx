import { useState, useEffect, FC } from 'react';
import { Play, Pause, SkipForward, RotateCcw, AlertTriangle, CloudRain, Droplets, Waves, Radio } from 'lucide-react';
import { DemonstrationStep } from '../../types/risk';

interface Props {
  steps: DemonstrationStep[];
  currentStepIndex: number;
  onStepChange: (index: number) => void;
  onShowCitizenCard: () => void;
}

export const ScenarioPlayer: FC<Props> = ({
  steps,
  currentStepIndex,
  onStepChange,
  onShowCitizenCard,
}) => {
  const [isPlaying, setIsPlaying] = useState(false);

  useEffect(() => {
    let timer: any;
    if (isPlaying) {
      timer = setInterval(() => {
        if (currentStepIndex < steps.length - 1) {
          onStepChange(currentStepIndex + 1);
        } else {
          setIsPlaying(false);
        }
      }, 3500);
    }
    return () => clearInterval(timer);
  }, [isPlaying, currentStepIndex, steps.length, onStepChange]);

  if (!steps || steps.length === 0) return null;
  const current = steps[currentStepIndex];

  const getBadgeColor = (lvl: string) => {
    switch (lvl) {
      case 'RED': return 'bg-red-500 text-white animate-pulse';
      case 'ORANGE': return 'bg-orange-500 text-white';
      case 'YELLOW': return 'bg-yellow-500 text-slate-900';
      default: return 'bg-emerald-500 text-white';
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-700/80 rounded-2xl p-5 shadow-xl text-slate-100 mb-6">
      {/* Top Bar: Title and Controls */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-blue-500/20 text-blue-400 rounded-lg">
            <Radio className="w-5 h-5 animate-pulse" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="text-xs uppercase font-bold tracking-widest text-blue-400">
                PRD §23 Live Simulation Engine
              </span>
              <span className={`text-xs font-black px-2 py-0.5 rounded-full ${getBadgeColor(current.assessment.risk_level)}`}>
                {current.assessment.risk_level}
              </span>
            </div>
            <h3 className="text-base font-bold text-white mt-0.5">
              Step {current.step} / 12: {current.description}
            </h3>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex items-center space-x-2">
          <button
            onClick={() => setIsPlaying(!isPlaying)}
            className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg font-semibold text-xs transition-colors ${
              isPlaying
                ? 'bg-amber-600 hover:bg-amber-500 text-white'
                : 'bg-blue-600 hover:bg-blue-500 text-white'
            }`}
          >
            {isPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
            <span>{isPlaying ? 'Pause' : 'Auto Play'}</span>
          </button>

          <button
            onClick={() => onStepChange(Math.min(steps.length - 1, currentStepIndex + 1))}
            disabled={currentStepIndex >= steps.length - 1}
            className="p-1.5 bg-slate-800 hover:bg-slate-700 disabled:opacity-40 rounded-lg text-slate-200 transition-colors"
            title="Next Step"
          >
            <SkipForward className="w-4 h-4" />
          </button>

          <button
            onClick={() => { setIsPlaying(false); onStepChange(0); }}
            className="p-1.5 bg-slate-800 hover:bg-slate-700 rounded-lg text-slate-200 transition-colors"
            title="Reset to Step 1"
          >
            <RotateCcw className="w-4 h-4" />
          </button>

          {/* Quick Jump Buttons for demonstration */}
          <button
            onClick={() => onStepChange(6)}
            className="px-2.5 py-1 bg-red-950/60 border border-red-800 text-red-300 hover:bg-red-900/80 rounded-lg text-xs font-semibold"
          >
            Jump to Step 7 (Lead Time 35m)
          </button>

          {current.citizen_card && (
            <button
              onClick={onShowCitizenCard}
              className="px-2.5 py-1 bg-emerald-900/60 border border-emerald-700 text-emerald-300 hover:bg-emerald-800 rounded-lg text-xs font-semibold"
            >
              View Citizen Warning Card
            </button>
          )}
        </div>
      </div>

      {/* Progress Bar */}
      <div className="w-full bg-slate-800 h-2 rounded-full mt-4 overflow-hidden">
        <div
          className="bg-blue-500 h-full transition-all duration-300 ease-out"
          style={{ width: `${((currentStepIndex + 1) / steps.length) * 100}%` }}
        />
      </div>

      {/* Real-time Environmental Telemetry at this Step */}
      <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-6 gap-3 mt-4">
        <div className="bg-slate-800/60 p-2.5 rounded-xl border border-slate-700/60">
          <div className="flex items-center space-x-1.5 text-slate-400 text-xs font-medium">
            <CloudRain className="w-3.5 h-3.5 text-sky-400" />
            <span>Rainfall Rate</span>
          </div>
          <p className="text-sm font-bold text-white mt-1">
            {current.environmental_inputs.rainfall_intensity_mm_hr} <span className="text-xs font-normal text-slate-400">mm/h</span>
          </p>
        </div>

        <div className="bg-slate-800/60 p-2.5 rounded-xl border border-slate-700/60">
          <div className="flex items-center space-x-1.5 text-slate-400 text-xs font-medium">
            <Droplets className="w-3.5 h-3.5 text-indigo-400" />
            <span>Soil Saturation</span>
          </div>
          <p className="text-sm font-bold text-white mt-1">
            {current.environmental_inputs.soil_moisture_pct} <span className="text-xs font-normal text-slate-400">%</span>
          </p>
        </div>

        <div className="bg-slate-800/60 p-2.5 rounded-xl border border-slate-700/60">
          <div className="flex items-center space-x-1.5 text-slate-400 text-xs font-medium">
            <Waves className="w-3.5 h-3.5 text-teal-400" />
            <span>River Level</span>
          </div>
          <p className="text-sm font-bold text-white mt-1">
            {current.environmental_inputs.river_level_m} <span className="text-xs font-normal text-slate-400">m</span>
          </p>
        </div>

        <div className="bg-slate-800/60 p-2.5 rounded-xl border border-slate-700/60">
          <div className="flex items-center space-x-1.5 text-slate-400 text-xs font-medium">
            <AlertTriangle className="w-3.5 h-3.5 text-amber-400" />
            <span>Compound Score</span>
          </div>
          <p className="text-sm font-bold text-amber-300 mt-1">
            {current.assessment.compound_risk_score} <span className="text-xs font-normal text-slate-400">/ 100</span>
          </p>
        </div>

        <div className="bg-slate-800/60 p-2.5 rounded-xl border border-slate-700/60">
          <div className="text-xs font-medium text-slate-400">Est. Lead Time</div>
          <p className="text-sm font-black text-rose-400 mt-1">
            {current.assessment.estimated_lead_time_minutes ? `${current.assessment.estimated_lead_time_minutes} min` : 'Normal'}
          </p>
        </div>

        <div className="bg-slate-800/60 p-2.5 rounded-xl border border-slate-700/60">
          <div className="text-xs font-medium text-slate-400">Assigned Shelter</div>
          <p className="text-xs font-bold text-emerald-400 mt-1 truncate" title={current.decisions.recommended_shelter}>
            {current.decisions.recommended_shelter}
          </p>
        </div>
      </div>
    </div>
  );
};
