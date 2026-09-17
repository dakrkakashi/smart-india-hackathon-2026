import React from 'react';
import { MapContainer, TileLayer } from 'react-leaflet';
import { RiskAssessment, Shelter } from '../../types/risk';
import { EvacuationRoute } from '../../types/map';
import { VillageRiskMarkers } from './VillageRiskMarkers';
import { ShelterMarkers } from './ShelterMarkers';
import { EvacuationRouteLayer } from './EvacuationRouteLayer';
import { RiskLegend } from './RiskLegend';

interface Props {
  assessments: RiskAssessment[];
  shelters: Shelter[];
  selectedVillageId: number;
  route: EvacuationRoute | null;
  showShelters: boolean;
  onSelectVillage: (id: number) => void;
}

export const RiskMapView: React.FC<Props> = ({
  assessments,
  shelters,
  selectedVillageId,
  route,
  showShelters,
  onSelectVillage,
}) => {
  // Center of pilot region: Chamoli & Rudraprayag (Garhwal Himalaya)
  const defaultCenter: [number, number] = [30.45, 79.35];

  return (
    <div className="relative w-full h-[640px] rounded-2xl overflow-hidden border border-slate-800 shadow-2xl bg-slate-950">
      <MapContainer
        center={defaultCenter}
        zoom={10}
        scrollWheelZoom={true}
        className="w-full h-full"
        style={{ background: '#090d16' }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://tile.openstreetmap.org/{z}/{x}/{y}.png"
          className="map-tiles"
        />

        {/* Evacuation Route Polyline & Waypoints */}
        <EvacuationRouteLayer route={route} />

        {/* Shelter Markers */}
        <ShelterMarkers shelters={shelters} visible={showShelters} />

        {/* Village Risk Markers */}
        <VillageRiskMarkers
          assessments={assessments}
          selectedVillageId={selectedVillageId}
          onSelectVillage={onSelectVillage}
        />
      </MapContainer>

      {/* Map Legend Overlay */}
      <RiskLegend />
    </div>
  );
};
