import { FC, useState } from 'react';
import { Activity, BatteryCharging, Cpu } from 'lucide-react';

interface SensorNode {
  id: string;
  name: string;
  type: string;
  location: string;
  district: string;
  status: 'ONLINE' | 'WARNING' | 'CRITICAL';
  battery_pct: number;
  last_ping: string;
  current_val: string;
  unit: string;
  trend: 'RISING' | 'STEADY' | 'FALLING';
}

const mockSensors: SensorNode[] = [
  {
    id: 'IOT-RG-01',
    name: 'Tipping Bucket Rain Gauge',
    type: 'Precipitation Sensor',
    location: 'Raini Upper Ridge (Elev 2,340m)',
    district: 'Chamoli',
    status: 'ONLINE',
    battery_pct: 94,
    last_ping: '10s ago',
    current_val: '85.0',
    unit: 'mm/h',
    trend: 'RISING',
  },
  {
    id: 'IOT-WL-01',
    name: 'Ultrasonic River Level Radar',
    type: 'Hydrology Gauge',
    location: 'Rishi Ganga Gorge Bridge',
    district: 'Chamoli',
    status: 'WARNING',
    battery_pct: 88,
    last_ping: '15s ago',
    current_val: '6.8',
    unit: 'meters',
    trend: 'RISING',
  },
  {
    id: 'IOT-SM-01',
    name: 'Soil Moisture TDR Probe (3-Depth)',
    type: 'Geotechnical Probe',
    location: 'Raini Slope Transect A',
    district: 'Chamoli',
    status: 'ONLINE',
    battery_pct: 91,
    last_ping: '30s ago',
    current_val: '86.0',
    unit: '% saturation',
    trend: 'RISING',
  },
  {
    id: 'IOT-INC-01',
    name: 'Biaxial MEMS Inclinometer',
    type: 'Slope Displacement',
    location: 'Joshimath Sunil Subsidence Escarpment',
    district: 'Chamoli',
    status: 'ONLINE',
    battery_pct: 96,
    last_ping: '45s ago',
    current_val: '3.4',
    unit: 'mm creep/day',
    trend: 'STEADY',
  },
  {
    id: 'IOT-RG-02',
    name: 'Optical Rain Gauge',
    type: 'Precipitation Sensor',
    location: 'Pindar Riverbank Station',
    district: 'Chamoli (Tharali)',
    status: 'ONLINE',
    battery_pct: 85,
    last_ping: '20s ago',
    current_val: '45.0',
    unit: 'mm/h',
    trend: 'RISING',
  },
  {
    id: 'IOT-WL-02',
    name: 'Doppler River Velocity Radar',
    type: 'Hydrology Gauge',
    location: 'Mandakini River Ghat',
    district: 'Rudraprayag (Sonprayag)',
    status: 'ONLINE',
    battery_pct: 98,
    last_ping: '12s ago',
    current_val: '1.4',
    unit: 'meters',
    trend: 'STEADY',
  },
];

export const Sensors: FC = () => {
  const [filterDistrict, setFilterDistrict] = useState<string>('ALL');

  const filtered = filterDistrict === 'ALL'
    ? mockSensors
    : mockSensors.filter((s) => s.district.toLowerCase().includes(filterDistrict.toLowerCase()));

  const getStatusBadge = (status: SensorNode['status']) => {
    switch (status) {
      case 'ONLINE':
        return 'bg-emerald-950/60 border border-emerald-700/60 text-emerald-400';
      case 'WARNING':
        return 'bg-amber-950/60 border border-amber-700/60 text-amber-400 animate-pulse';
      case 'CRITICAL':
        return 'bg-red-950/60 border border-red-700/60 text-red-400 animate-pulse';
    }
  };

  return (
    <div className="p-6 max-w-[1600px] mx-auto space-y-6">
      {/* Page Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 bg-slate-900 border border-slate-800 p-5 rounded-2xl shadow-lg">
        <div>
          <span className="text-xs font-black tracking-widest text-sky-400 uppercase bg-sky-950/60 border border-sky-800/80 px-2.5 py-1 rounded-full">
            IoT Edge Telemetry &bull; PRD §7
          </span>
          <h1 className="text-2xl font-black text-white mt-2">
            Sensor Grid & Edge Ingestion Monitor
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Real-time MQTT & HTTP telemetry from precipitation, ultrasonic river stage, and slope moisture sensors
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 bg-slate-800 border border-slate-700 px-3 py-1.5 rounded-xl text-xs text-slate-300">
            <Cpu className="w-4 h-4 text-blue-400" />
            <span>6/6 Nodes Reporting (100%)</span>
          </div>
          <select
            value={filterDistrict}
            onChange={(e) => setFilterDistrict(e.target.value)}
            className="bg-slate-800 border border-slate-700 text-xs text-slate-200 px-3 py-2 rounded-xl focus:outline-none focus:ring-1 focus:ring-blue-500"
          >
            <option value="ALL">All Catchments</option>
            <option value="Chamoli">Chamoli Basin</option>
            <option value="Rudraprayag">Rudraprayag Basin</option>
          </select>
        </div>
      </div>

      {/* Grid of Sensors */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">
        {filtered.map((sensor) => (
          <div
            key={sensor.id}
            className="bg-slate-900 border border-slate-800 hover:border-slate-700 rounded-2xl p-5 shadow-lg flex flex-col justify-between transition-all"
          >
            <div>
              <div className="flex items-center justify-between">
                <span className="text-[11px] font-mono text-slate-400 bg-slate-800/70 px-2 py-0.5 rounded">
                  {sensor.id}
                </span>
                <span className={`text-[11px] font-bold px-2 py-0.5 rounded-full ${getStatusBadge(sensor.status)}`}>
                  ● {sensor.status}
                </span>
              </div>

              <h3 className="text-base font-bold text-white mt-3">
                {sensor.name}
              </h3>
              <p className="text-xs text-slate-400">
                {sensor.location}
              </p>

              <div className="mt-4 p-3 bg-slate-950/60 border border-slate-800 rounded-xl flex items-center justify-between">
                <div>
                  <span className="text-[10px] uppercase font-bold text-slate-400 block">Telemetry Reading</span>
                  <div className="flex items-baseline space-x-1.5 mt-0.5">
                    <span className="text-2xl font-black text-white">{sensor.current_val}</span>
                    <span className="text-xs text-sky-400 font-semibold">{sensor.unit}</span>
                  </div>
                </div>
                <div className="text-right text-xs">
                  <span className="text-slate-500 text-[10px] block">Trend</span>
                  <span className={`font-bold ${sensor.trend === 'RISING' ? 'text-amber-400' : 'text-emerald-400'}`}>
                    {sensor.trend === 'RISING' ? '▲ Rising' : '━ Steady'}
                  </span>
                </div>
              </div>
            </div>

            <div className="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs text-slate-400">
              <span className="flex items-center gap-1">
                <BatteryCharging className="w-3.5 h-3.5 text-emerald-400" />
                <span>{sensor.battery_pct}% Battery</span>
              </span>
              <span className="flex items-center gap-1">
                <Activity className="w-3.5 h-3.5 text-blue-400" />
                <span>Ping: {sensor.last_ping}</span>
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Sensors;
