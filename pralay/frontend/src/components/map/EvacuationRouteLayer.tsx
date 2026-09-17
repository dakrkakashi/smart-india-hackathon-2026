import React from 'react';
import { Polyline, CircleMarker, Popup, Tooltip } from 'react-leaflet';
import { EvacuationRoute } from '../../types/map';
import { LatLngTuple } from 'leaflet';
import { Navigation, AlertTriangle, Clock } from 'lucide-react';

interface Props {
  route: EvacuationRoute | null;
}

export const EvacuationRouteLayer: React.FC<Props> = ({ route }) => {
  if (!route || !route.waypoints || route.waypoints.length < 2) {
    return null;
  }

  const positions: LatLngTuple[] = route.waypoints.map((w) => [w.lat, w.lng]);
  const startWp = route.waypoints[0];
  const destWp = route.waypoints[route.waypoints.length - 1];
  const intermediateWps = route.waypoints.slice(1, -1);

  return (
    <>
      {/* Route Glow Polyline */}
      <Polyline
        positions={positions}
        pathOptions={{
          color: '#0284c7',
          weight: 7,
          opacity: 0.4,
        }}
      />

      {/* Main Dashed Evacuation Polyline */}
      <Polyline
        positions={positions}
        pathOptions={{
          color: '#38bdf8',
          weight: 4,
          dashArray: '8, 8',
          opacity: 0.95,
        }}
      >
        <Popup className="custom-dark-popup">
          <div className="p-2 min-w-[260px] text-slate-100 font-sans space-y-2">
            <div className="flex items-center gap-1.5 text-sky-400 font-bold text-xs border-b border-slate-700 pb-1">
              <Navigation className="w-4 h-4" />
              <span>Safe Evacuation Corridor</span>
            </div>

            <p className="text-xs font-semibold text-white">{route.route_id}</p>
            <p className="text-xs text-slate-300">{route.instructions}</p>

            <div className="grid grid-cols-2 gap-2 text-xs bg-slate-800 p-2 rounded">
              <div>
                <span className="text-slate-400 text-[10px] block">Distance</span>
                <span className="font-bold text-white">{route.total_distance_km} km</span>
              </div>
              <div>
                <span className="text-slate-400 text-[10px] block">Est. Transit</span>
                <span className="font-bold text-sky-300 flex items-center gap-1">
                  <Clock className="w-3 h-3" />
                  ~{route.estimated_transit_minutes} mins
                </span>
              </div>
            </div>

            {route.avoid_sectors && route.avoid_sectors.length > 0 && (
              <div className="text-[11px] bg-red-950/40 border border-red-800/60 p-1.5 rounded">
                <span className="text-red-300 font-semibold flex items-center gap-1">
                  <AlertTriangle className="w-3 h-3" /> Hazard Sectors Avoided:
                </span>
                <ul className="list-disc list-inside text-red-200 text-[10px] mt-0.5">
                  {route.avoid_sectors.map((s, idx) => (
                    <li key={idx}>{s}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </Popup>
      </Polyline>

      {/* Start Waypoint Marker */}
      <CircleMarker
        center={[startWp.lat, startWp.lng]}
        radius={7}
        pathOptions={{
          color: '#ffffff',
          fillColor: '#22c55e', // Green
          fillOpacity: 1,
          weight: 2,
        }}
      >
        <Tooltip direction="top" offset={[0, -6]}>
          <span className="text-xs font-bold text-slate-900">Start: {startWp.name}</span>
        </Tooltip>
      </CircleMarker>

      {/* Intermediate Waypoints (Ridge By-pass / Safe Elevation) */}
      {intermediateWps.map((wp, idx) => (
        <CircleMarker
          key={`wp-${idx}`}
          center={[wp.lat, wp.lng]}
          radius={5}
          pathOptions={{
            color: '#ffffff',
            fillColor: '#38bdf8', // Cyan
            fillOpacity: 0.9,
            weight: 1.5,
          }}
        >
          <Tooltip direction="top" offset={[0, -5]}>
            <span className="text-xs font-semibold text-slate-900">
              Safe Corridor: {wp.name}
            </span>
          </Tooltip>
        </CircleMarker>
      ))}

      {/* Destination Waypoint Marker */}
      <CircleMarker
        center={[destWp.lat, destWp.lng]}
        radius={8}
        pathOptions={{
          color: '#ffffff',
          fillColor: '#f59e0b', // Amber/Gold
          fillOpacity: 1,
          weight: 2,
        }}
      >
        <Tooltip direction="top" offset={[0, -6]}>
          <span className="text-xs font-bold text-slate-900">
            Destination: {destWp.name}
          </span>
        </Tooltip>
      </CircleMarker>
    </>
  );
};
