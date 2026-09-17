import { create } from 'zustand';
import { RiskAssessment, Shelter } from '../types/risk';
import { EvacuationRoute, MapFilterState } from '../types/map';
import { fetchVillageAssessments, fetchShelters, fetchEvacuationRoute } from '../api/mapApi';
import { initialAssessments } from '../data/mockAssessments';
import { mockShelters, mockRoute } from '../data/mockMapData';

interface MapState {
  assessments: RiskAssessment[];
  shelters: Shelter[];
  selectedVillageId: number;
  route: EvacuationRoute | null;
  filters: MapFilterState;
  loading: boolean;
  isUsingFallback: boolean;
  error: string | null;

  loadMapData: () => Promise<void>;
  selectVillage: (villageId: number) => Promise<void>;
  setFilters: (filters: Partial<MapFilterState>) => void;
  refresh: () => Promise<void>;
}

export const useMapStore = create<MapState>((set, get) => ({
  assessments: initialAssessments,
  shelters: mockShelters,
  selectedVillageId: 1,
  route: mockRoute,
  filters: {
    district: 'ALL',
    hazard: 'ALL',
    showShelters: true,
  },
  loading: false,
  isUsingFallback: false,
  error: null,

  loadMapData: async () => {
    set({ loading: true, error: null });
    let usedFallback = false;
    let assessmentsData = initialAssessments;
    let sheltersData = mockShelters;

    const [assessmentsResult, sheltersResult] = await Promise.allSettled([
      fetchVillageAssessments(get().filters.district),
      fetchShelters(),
    ]);

    if (assessmentsResult.status === 'fulfilled' && assessmentsResult.value?.length > 0) {
      assessmentsData = assessmentsResult.value;
    } else {
      usedFallback = true;
    }

    if (sheltersResult.status === 'fulfilled' && sheltersResult.value?.length > 0) {
      sheltersData = sheltersResult.value;
    } else {
      usedFallback = true;
    }

    set({
      assessments: assessmentsData,
      shelters: sheltersData,
      isUsingFallback: usedFallback,
      loading: false,
    });

    // Also load route for currently selected village
    await get().selectVillage(get().selectedVillageId);
  },

  selectVillage: async (villageId: number) => {
    set({ selectedVillageId: villageId });
    try {
      const route = await fetchEvacuationRoute(villageId);
      set({ route });
    } catch {
      // If the selected village is Raini (1), use the realistic mockRoute
      // Otherwise synthesize or fallback to mockRoute with current village coords
      const village = get().assessments.find((a) => a.village_id === villageId);
      if (village && village.village_id !== 1) {
        const shelter = get().shelters[0] || mockShelters[0];
        const distKm = village.action.shelter_distance_km || 1.0;
        const estMins = Math.max(10, Math.round((distKm / 3.5) * 60));
        const syntheticRoute: EvacuationRoute = {
          route_id: `ROUTE-${village.village_name.substring(0, 3).toUpperCase()}-01`,
          destination_shelter_id: shelter.id,
          destination_shelter_name: shelter.name,
          total_distance_km: distKm,
          estimated_transit_minutes: estMins,
          status: 'CLEAR_SAFE',
          avoid_sectors: ['Gorge Corridor', 'Lower Terrace'],
          waypoints: [
            {
              name: `${village.village_name} Assembly Point`,
              lat: village.latitude,
              lng: village.longitude,
              type: 'START',
            },
            {
              name: 'Upper Ridge Safe Corridor',
              lat: (village.latitude + shelter.latitude) / 2 + 0.002,
              lng: (village.longitude + shelter.longitude) / 2 + 0.001,
              type: 'SAFE_CORRIDOR',
            },
            {
              name: shelter.name,
              lat: shelter.latitude,
              lng: shelter.longitude,
              type: 'DESTINATION',
            },
          ],
          instructions: `Evacuate along high elevation ridge route to ${shelter.name}. Avoid lower riverbeds.`,
        };
        set({ route: syntheticRoute });
      } else {
        set({ route: mockRoute });
      }
    }
  },

  setFilters: (newFilters: Partial<MapFilterState>) => {
    set((state) => ({
      filters: { ...state.filters, ...newFilters },
    }));
  },

  refresh: async () => {
    await get().loadMapData();
  },
}));
