import React from 'react';
import { MapFilterState } from '../../types/map';
import { HazardType } from '../../types/risk';
import { Filter, RefreshCw, Home } from 'lucide-react';

interface Props {
  filters: MapFilterState;
  onFilterChange: (filters: Partial<MapFilterState>) => void;
  onRefresh: () => void;
  loading: boolean;
  totalVillages: number;
  filteredVillages: number;
}

export const MapFilters: React.FC<Props> = ({
  filters,
  onFilterChange,
  onRefresh,
  loading,
  totalVillages,
  filteredVillages,
}) => {
  return (
    <div className="bg-slate-900 border border-slate-800 p-4 rounded-2xl shadow-lg flex flex-wrap items-center justify-between gap-4">
      <div className="flex flex-wrap items-center gap-3">
        <div className="flex items-center gap-2 text-slate-400 text-xs font-bold uppercase tracking-wider">
          <Filter className="w-4 h-4 text-blue-400" />
          <span>Filters:</span>
        </div>

        {/* District Filter */}
        <select
          value={filters.district}
          onChange={(e) => onFilterChange({ district: e.target.value })}
          className="bg-slate-800 border border-slate-700 text-slate-200 text-xs font-semibold rounded-xl px-3 py-2 focus:outline-none focus:border-blue-500 transition"
        >
          <option value="ALL">All Districts</option>
          <option value="Chamoli">Chamoli</option>
          <option value="Rudraprayag">Rudraprayag</option>
        </select>

        {/* Hazard Type Filter */}
        <select
          value={filters.hazard}
          onChange={(e) => onFilterChange({ hazard: e.target.value as 'ALL' | HazardType })}
          className="bg-slate-800 border border-slate-700 text-slate-200 text-xs font-semibold rounded-xl px-3 py-2 focus:outline-none focus:border-blue-500 transition"
        >
          <option value="ALL">All Hazards</option>
          <option value="FLASH_FLOOD">Flash Flood</option>
          <option value="LANDSLIDE">Landslide</option>
          <option value="COMPOUND">Compound</option>
          <option value="NONE">Nominal (Safe)</option>
        </select>

        {/* Shelter Toggle Button */}
        <button
          type="button"
          onClick={() => onFilterChange({ showShelters: !filters.showShelters })}
          className={`flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs font-bold transition border ${
            filters.showShelters
              ? 'bg-sky-950/80 text-sky-300 border-sky-600/70 shadow-sm'
              : 'bg-slate-800 text-slate-400 border-slate-700 hover:text-slate-200'
          }`}
        >
          <Home className="w-3.5 h-3.5" />
          <span>{filters.showShelters ? 'Shelters Visible' : 'Shelters Hidden'}</span>
        </button>
      </div>

      <div className="flex items-center gap-3">
        <span className="text-xs text-slate-400">
          Showing <strong className="text-white">{filteredVillages}</strong> of{' '}
          <strong className="text-white">{totalVillages}</strong> villages
        </span>

        <button
          onClick={onRefresh}
          disabled={loading}
          className="flex items-center gap-1.5 px-3 py-2 bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-200 rounded-xl text-xs font-semibold transition disabled:opacity-50"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin text-blue-400' : ''}`} />
          <span>Refresh</span>
        </button>
      </div>
    </div>
  );
};
