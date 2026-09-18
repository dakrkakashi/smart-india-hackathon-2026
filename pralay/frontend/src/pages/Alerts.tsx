import { FC, useState } from 'react';
import { CheckCircle2, Radio } from 'lucide-react';

interface AlertItem {
  id: string;
  village: string;
  district: string;
  severity: 'RED' | 'ORANGE' | 'YELLOW';
  lead_time: string;
  hazard: string;
  message: string;
  channels: string[];
  dispatched_at: string;
}

const mockAlerts: AlertItem[] = [
  {
    id: 'ALT-2026-001',
    village: 'Raini',
    district: 'Chamoli',
    severity: 'RED',
    lead_time: '35 Minutes',
    hazard: 'Compound Flash Flood & Landslide',
    message: 'CRITICAL WARNING: Move immediately to Raini Upper Primary School. Rishi Ganga gorge water rising rapidly at 1.8 m/hr.',
    channels: ['NDRF Siren', 'SMS Cell Broadcast', 'CAP 1.2 Protocol', 'IVR Call Tree'],
    dispatched_at: '10 mins ago',
  },
  {
    id: 'ALT-2026-002',
    village: 'Tharali',
    district: 'Chamoli',
    severity: 'ORANGE',
    lead_time: '90 Minutes',
    hazard: 'Flash Flood',
    message: 'PREPARE FOR EVACUATION: Pindar river level approaching warning threshold. Secure livestock and prepare to move to GIC Tharali.',
    channels: ['SMS Cell Broadcast', 'Local Administration Radio'],
    dispatched_at: '25 mins ago',
  },
  {
    id: 'ALT-2026-003',
    village: 'Joshimath',
    district: 'Chamoli',
    severity: 'YELLOW',
    lead_time: '4 Hours',
    hazard: 'Slope Subsidence / Landslide',
    message: 'ADVISORY: Excessive soil moisture saturation detected on Sunil slope. Heavy vehicular transit restricted on bypass.',
    channels: ['Local Administration Bulletin', 'WhatsApp DMR Channel'],
    dispatched_at: '1 hour ago',
  },
];

export const Alerts: FC = () => {
  const [selectedAlert, setSelectedAlert] = useState<AlertItem>(mockAlerts[0]);

  const getSeverityStyle = (s: AlertItem['severity']) => {
    switch (s) {
      case 'RED':
        return 'bg-red-950/40 border-red-500/80 text-red-300';
      case 'ORANGE':
        return 'bg-amber-950/40 border-amber-500/80 text-amber-300';
      case 'YELLOW':
        return 'bg-yellow-950/40 border-yellow-500/80 text-yellow-300';
    }
  };

  const getBadgeStyle = (s: AlertItem['severity']) => {
    switch (s) {
      case 'RED':
        return 'bg-red-600 text-white animate-pulse';
      case 'ORANGE':
        return 'bg-amber-600 text-white';
      case 'YELLOW':
        return 'bg-yellow-500 text-slate-950';
    }
  };

  return (
    <div className="p-6 max-w-[1600px] mx-auto space-y-6">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 bg-slate-900 border border-slate-800 p-5 rounded-2xl shadow-lg">
        <div>
          <span className="text-xs font-black tracking-widest text-red-400 uppercase bg-red-950/60 border border-red-800/80 px-2.5 py-1 rounded-full">
            CAP 1.2 Multi-Channel Alert Gateway &bull; PRD §14
          </span>
          <h1 className="text-2xl font-black text-white mt-2">
            Disaster Alert & Dispatch Operations
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Plain-language bilingual citizen warnings, NDRF control room bulletins, and Common Alerting Protocol broadcasts
          </p>
        </div>

        <div className="flex items-center gap-2 bg-slate-800 border border-slate-700 px-3 py-1.5 rounded-xl text-xs text-slate-300">
          <Radio className="w-4 h-4 text-emerald-400" />
          <span>Gateway Active (Cell Broadcast & IVR Ready)</span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Alerts List */}
        <div className="space-y-3 lg:col-span-1">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400">
            Active Incident Bulletins ({mockAlerts.length})
          </h3>
          {mockAlerts.map((alert) => {
            const isSelected = alert.id === selectedAlert.id;
            return (
              <button
                key={alert.id}
                onClick={() => setSelectedAlert(alert)}
                className={`w-full text-left p-4 rounded-xl border transition-all ${
                  isSelected
                    ? 'bg-slate-800 border-blue-500 ring-2 ring-blue-500/40'
                    : 'bg-slate-900 border-slate-800 hover:border-slate-700'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-mono text-slate-400">{alert.id}</span>
                  <span className={`text-[10px] font-black px-2 py-0.5 rounded-full ${getBadgeStyle(alert.severity)}`}>
                    {alert.severity}
                  </span>
                </div>
                <h4 className="text-base font-bold text-white mt-2">
                  {alert.village}, {alert.district}
                </h4>
                <p className="text-xs text-slate-400 mt-0.5">
                  Lead Time: <span className="font-semibold text-rose-400">{alert.lead_time}</span>
                </p>
                <div className="mt-3 text-[11px] text-slate-500 flex justify-between">
                  <span>{alert.hazard}</span>
                  <span>{alert.dispatched_at}</span>
                </div>
              </button>
            );
          })}
        </div>

        {/* Alert Detail View */}
        <div className="lg:col-span-2">
          <div className={`border rounded-2xl p-6 shadow-xl ${getSeverityStyle(selectedAlert.severity)}`}>
            <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-800/80 pb-4">
              <div>
                <span className={`text-xs font-black px-3 py-1 rounded-full ${getBadgeStyle(selectedAlert.severity)}`}>
                  {selectedAlert.severity} PRIORITY DISPATCH
                </span>
                <h2 className="text-2xl font-black text-white mt-3">
                  {selectedAlert.village} ({selectedAlert.district} District)
                </h2>
              </div>
              <div className="text-right">
                <span className="text-xs text-slate-400 block">Estimated Lead Time</span>
                <span className="text-2xl font-black text-rose-400">{selectedAlert.lead_time}</span>
              </div>
            </div>

            <div className="mt-5 space-y-4">
              <div className="bg-slate-950/70 p-4 rounded-xl border border-slate-800">
                <span className="text-[11px] uppercase font-bold text-slate-400 block mb-1">
                  Citizen Directive / Public Announcement Text
                </span>
                <p className="text-sm font-semibold text-slate-100 leading-relaxed">
                  "{selectedAlert.message}"
                </p>
              </div>

              <div>
                <span className="text-[11px] uppercase font-bold text-slate-400 block mb-2">
                  Multi-Channel Dissemination Pipeline (PRD §15)
                </span>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
                  {selectedAlert.channels.map((ch) => (
                    <div key={ch} className="bg-slate-900/90 border border-slate-700/80 p-2.5 rounded-lg text-center">
                      <CheckCircle2 className="w-4 h-4 text-emerald-400 mx-auto mb-1" />
                      <span className="text-[11px] font-bold text-slate-200 block">{ch}</span>
                      <span className="text-[9px] text-emerald-400">Broadcasted</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="pt-4 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
                <span>Emergency Control: <strong>1077 (SEOC Uttarakhand) / 112</strong></span>
                <span className="text-slate-500 font-mono">Dispatched {selectedAlert.dispatched_at}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Alerts;
