import React from 'react';
import { CircleMarker, Popup, Tooltip } from 'react-leaflet';
import { Shelter } from '../../types/risk';
import { Home, Phone, User, CheckCircle2 } from 'lucide-react';

interface Props {
  shelters: Shelter[];
  visible: boolean;
}

export const ShelterMarkers: React.FC<Props> = ({ shelters, visible }) => {
  if (!visible) return null;

  return (
    <>
      {shelters.map((shelter) => {
        const occupancyPct =
          shelter.capacity > 0
            ? Math.round((shelter.current_occupancy / shelter.capacity) * 100)
            : 0;

        return (
          <CircleMarker
            key={`shelter-${shelter.id}`}
            center={[shelter.latitude, shelter.longitude]}
            radius={9}
            pathOptions={{
              color: '#ffffff',
              fillColor: '#0284c7', // Sky blue
              fillOpacity: 0.9,
              weight: 2,
            }}
          >
            <Tooltip direction="bottom" offset={[0, 8]} opacity={0.95}>
              <div className="text-xs font-semibold text-slate-900 flex items-center gap-1">
                <span>🏠</span>
                <span>{shelter.name}</span>
              </div>
            </Tooltip>

            <Popup className="custom-dark-popup">
              <div className="p-2 min-w-[260px] text-slate-100 font-sans space-y-2">
                <div className="border-b border-slate-700 pb-1.5 flex items-start justify-between gap-2">
                  <div>
                    <div className="flex items-center gap-1.5 text-sky-400 font-semibold text-xs">
                      <Home className="w-3.5 h-3.5" />
                      <span>Safe Relief Shelter</span>
                    </div>
                    <h4 className="font-bold text-sm text-white mt-0.5">{shelter.name}</h4>
                    <p className="text-[11px] text-slate-400">{shelter.shelter_type}</p>
                  </div>
                  <span
                    className={`text-[10px] px-2 py-0.5 rounded font-bold uppercase ${
                      shelter.is_available
                        ? 'bg-emerald-950 text-emerald-300 border border-emerald-800'
                        : 'bg-red-950 text-red-300 border border-red-800'
                    }`}
                  >
                    {shelter.is_available ? 'Available' : 'Full'}
                  </span>
                </div>

                <div className="bg-slate-800/80 p-2 rounded space-y-1">
                  <div className="flex justify-between text-xs">
                    <span className="text-slate-400">Capacity Status:</span>
                    <span className="font-bold text-white">
                      {shelter.current_occupancy} / {shelter.capacity} ({occupancyPct}% full)
                    </span>
                  </div>
                  <div className="w-full bg-slate-700 rounded-full h-1.5 overflow-hidden">
                    <div
                      className={`h-full rounded-full transition-all ${
                        occupancyPct > 80 ? 'bg-red-500' : occupancyPct > 50 ? 'bg-amber-500' : 'bg-emerald-500'
                      }`}
                      style={{ width: `${Math.min(100, occupancyPct)}%` }}
                    />
                  </div>
                  <div className="flex justify-between text-[11px] text-slate-400 pt-0.5">
                    <span>Available Spots:</span>
                    <span className="font-semibold text-emerald-400">
                      {shelter.available_capacity ?? shelter.capacity - shelter.current_occupancy}
                    </span>
                  </div>
                </div>

                {shelter.elevation_meters && (
                  <div className="text-xs text-slate-300">
                    Elevation:{' '}
                    <strong className="text-white">{shelter.elevation_meters} m</strong> (Non-flood terrace)
                  </div>
                )}

                <div className="flex flex-wrap gap-1 text-[10px]">
                  {shelter.has_drinking_water && (
                    <span className="px-1.5 py-0.5 rounded bg-blue-950 text-blue-300 border border-blue-800 flex items-center gap-0.5">
                      <CheckCircle2 className="w-3 h-3" /> Water
                    </span>
                  )}
                  {shelter.has_power_backup && (
                    <span className="px-1.5 py-0.5 rounded bg-yellow-950 text-yellow-300 border border-yellow-800 flex items-center gap-0.5">
                      <CheckCircle2 className="w-3 h-3" /> Power
                    </span>
                  )}
                  {shelter.has_medical_facility && (
                    <span className="px-1.5 py-0.5 rounded bg-red-950 text-red-300 border border-red-800 flex items-center gap-0.5">
                      <CheckCircle2 className="w-3 h-3" /> First-Aid
                    </span>
                  )}
                </div>

                {shelter.contact_person && (
                  <div className="border-t border-slate-700/80 pt-1.5 text-[11px] text-slate-300 space-y-0.5">
                    <div className="flex items-center gap-1 text-slate-400">
                      <User className="w-3 h-3" />
                      <span>{shelter.contact_person}</span>
                    </div>
                    {shelter.contact_phone && (
                      <div className="flex items-center gap-1 text-slate-400">
                        <Phone className="w-3 h-3" />
                        <span className="font-mono">{shelter.contact_phone}</span>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </Popup>
          </CircleMarker>
        );
      })}
    </>
  );
};
