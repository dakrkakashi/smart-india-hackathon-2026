import { apiClient } from './client';
import { RiskAssessment, Shelter } from '../types/risk';
import { EvacuationRoute } from '../types/map';

export async function fetchVillageAssessments(district?: string): Promise<RiskAssessment[]> {
  const params = district && district !== 'ALL' ? { district } : undefined;
  const res = await apiClient.get<RiskAssessment[]>('/predictions/catchments', { params });
  return res.data;
}

export async function fetchShelters(regionId?: number): Promise<Shelter[]> {
  const params = regionId ? { region_id: regionId } : undefined;
  const res = await apiClient.get<Shelter[]>('/evacuations/shelters', { params });
  return res.data;
}

export async function fetchEvacuationRoute(villageId: number): Promise<EvacuationRoute> {
  const res = await apiClient.get<EvacuationRoute>(`/evacuations/route/${villageId}`);
  return res.data;
}

export async function fetchActiveAlerts(): Promise<any[]> {
  const res = await apiClient.get<any[]>('/alerts');
  return res.data;
}
