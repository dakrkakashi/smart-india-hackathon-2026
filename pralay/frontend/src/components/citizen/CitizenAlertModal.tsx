import { FC } from 'react';
import { AlertOctagon, PhoneCall, ShieldAlert, Navigation, Home, X } from 'lucide-react';
import { CitizenAlertCard } from '../../types/risk';

interface Props {
  card: CitizenAlertCard | null;
  isOpen: boolean;
  onClose: () => void;
}

export const CitizenAlertModal: FC<Props> = ({ card, isOpen, onClose }) => {
  if (!isOpen || !card) return null;

  const isRed = card.severity_label.includes('RED');
  const isOrange = card.severity_label.includes('ORANGE');

  const bgHeader = isRed
    ? 'bg-red-600'
    : isOrange
    ? 'bg-amber-600'
    : 'bg-yellow-500';

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="w-full max-w-md bg-slate-900 border border-slate-700 rounded-2xl overflow-hidden shadow-2xl">
        {/* Urgent Header */}
        <div className={`${bgHeader} px-6 py-5 text-white flex items-center justify-between`}>
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-black/20 rounded-full animate-pulse">
              <AlertOctagon className="w-8 h-8 text-white" />
            </div>
            <div>
              <span className="text-xs font-black uppercase tracking-wider bg-black/30 px-2 py-0.5 rounded">
                National Disaster Alert (NDMA / SDMA)
              </span>
              <h2 className="text-xl font-extrabold mt-1">{card.severity_label}</h2>
              <p className="text-xs text-white/90 font-medium">{card.hazard_title}</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded-full hover:bg-black/20 transition-colors text-white"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        {/* Body */}
        <div className="p-6 space-y-4 text-slate-100">
          {/* Target Village & Estimated Lead Time */}
          <div className="grid grid-cols-2 gap-3 bg-slate-800/80 p-4 rounded-xl border border-slate-700">
            <div>
              <span className="text-xs uppercase text-slate-400 font-semibold">Your Location</span>
              <p className="text-lg font-bold text-white mt-0.5">{card.village_name}</p>
            </div>
            <div>
              <span className="text-xs uppercase text-slate-400 font-semibold">Est. Lead Time</span>
              <p className="text-lg font-black text-amber-400 mt-0.5 flex items-center">
                ⏱ {card.estimated_lead_time}
              </p>
            </div>
          </div>

          {/* Action Directive */}
          <div className="bg-red-950/40 border border-red-800/80 p-4 rounded-xl">
            <div className="flex items-start space-x-3">
              <ShieldAlert className="w-6 h-6 text-red-400 flex-shrink-0 mt-0.5" />
              <div>
                <h4 className="text-xs font-bold uppercase text-red-300">Action Directive</h4>
                <p className="text-sm font-semibold text-white mt-1 leading-snug">
                  {card.action_directive}
                </p>
              </div>
            </div>
          </div>

          {/* Designated Shelter */}
          <div className="bg-slate-800/60 border border-slate-700 p-4 rounded-xl space-y-2">
            <div className="flex items-center space-x-2 text-emerald-400">
              <Home className="w-5 h-5" />
              <h4 className="text-xs font-bold uppercase">Designated Safe Shelter</h4>
            </div>
            <p className="text-sm font-semibold text-slate-200">
              {card.assigned_shelter}
            </p>
          </div>

          {/* Evacuation Advice */}
          <div className="bg-slate-800/60 border border-slate-700 p-4 rounded-xl space-y-2">
            <div className="flex items-center space-x-2 text-sky-400">
              <Navigation className="w-5 h-5" />
              <h4 className="text-xs font-bold uppercase">Evacuation Route Advice</h4>
            </div>
            <p className="text-xs text-slate-300 leading-relaxed">
              {card.evacuation_advice}
            </p>
          </div>

          {/* Emergency Helpline */}
          <div className="flex items-center justify-between pt-2 border-t border-slate-800 text-xs text-slate-400">
            <span className="flex items-center space-x-1.5 text-amber-300 font-semibold">
              <PhoneCall className="w-4 h-4" />
              <span>{card.emergency_contact}</span>
            </span>
            <span className="text-[11px] text-slate-500">{card.timestamp}</span>
          </div>
        </div>

        {/* Footer */}
        <div className="p-4 bg-slate-950 border-t border-slate-800 text-center">
          <button
            onClick={onClose}
            className="w-full py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-sm font-semibold rounded-lg transition-colors"
          >
            Acknowledge & Close
          </button>
        </div>
      </div>
    </div>
  );
};
