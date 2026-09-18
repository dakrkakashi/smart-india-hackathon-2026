import { useState, useEffect } from 'react';
import axios from 'axios';
import { NorthStarDecisionPanes } from '../components/dashboard/NorthStarDecisionPanes';
import { ScenarioPlayer } from '../components/dashboard/ScenarioPlayer';
import { VillageCatchmentList } from '../components/dashboard/VillageCatchmentList';
import { CitizenAlertModal } from '../components/citizen/CitizenAlertModal';
import { RiskAssessment, DemonstrationStep, CitizenAlertCard } from '../types/risk';
import { initialAssessments } from '../data/mockAssessments';
import { mockScenarioSteps } from '../data/mockScenarioData';

export default function Dashboard() {
  const [assessments, setAssessments] = useState<RiskAssessment[]>(initialAssessments);
  const [selectedVillageId, setSelectedVillageId] = useState<number>(1);
  const [scenarioSteps, setScenarioSteps] = useState<DemonstrationStep[]>(mockScenarioSteps);
  const [currentStepIndex, setCurrentStepIndex] = useState<number>(6); // Default Step 7 (Lead time 35m)
  const [isCitizenModalOpen, setIsCitizenModalOpen] = useState<boolean>(false);
  const [citizenCard, setCitizenCard] = useState<CitizenAlertCard | null>(null);

  // Fetch real-time API data if backend is reachable, fallback to mock seamlessly
  useEffect(() => {
    let isMounted = true;
    const fetchData = async () => {
      try {
        const predRes = await axios.get('/api/v1/predictions', { timeout: 3000 });
        if (isMounted && Array.isArray(predRes.data) && predRes.data.length > 0) {
          setAssessments(predRes.data);
        }
      } catch (err) {
        // API unreachable, deterministic offline state maintained
      }

      try {
        const scenRes = await axios.post('/api/v1/scenarios/run-12-step?village_id=1', null, { timeout: 3000 });
        if (isMounted && scenRes.data && Array.isArray(scenRes.data.steps) && scenRes.data.steps.length > 0) {
          setScenarioSteps(scenRes.data.steps);
        }
      } catch (err) {
        // Built-in 12-step scenario loaded by default
      }
    };

    fetchData();
    return () => {
      isMounted = false;
    };
  }, []);

  const selectedAssessment =
    assessments.find((a) => a.village_id === selectedVillageId) || assessments[0] || initialAssessments[0];

  const handleOpenCitizenCard = async () => {
    try {
      const res = await axios.get(`/api/v1/alerts/citizen/${selectedVillageId}`, { timeout: 3000 });
      if (res.data && typeof res.data === 'object' && 'severity_label' in res.data) {
        setCitizenCard(res.data);
        setIsCitizenModalOpen(true);
        return;
      }
    } catch (e) {
      // Synthesize from active assessment
    }

    // Synthesize fallback card from current assessment state
    if (selectedAssessment) {
      const synth: CitizenAlertCard = {
        severity_label: selectedAssessment.risk_level,
        hazard_title: `${selectedAssessment.primary_hazard} WARNING`,
        village_name: selectedAssessment.village_name,
        estimated_lead_time: selectedAssessment.lead_time.minutes
          ? `${selectedAssessment.lead_time.minutes} Minutes`
          : 'Advisory Status',
        action_directive: selectedAssessment.action.action,
        assigned_shelter: selectedAssessment.action.nearest_shelter_name || 'Designated High Ground Shelter',
        evacuation_advice: selectedAssessment.action.safe_path_instructions || 'Ascend immediately to upper terrace.',
        emergency_contact: '1077 (State Emergency Operation Centre) / 112',
        timestamp: new Date().toLocaleTimeString(),
      };
      setCitizenCard(synth);
      setIsCitizenModalOpen(true);
    }
  };

  const handleStepChange = (stepIndex: number) => {
    setCurrentStepIndex(stepIndex);
    if (scenarioSteps[stepIndex]) {
      const step = scenarioSteps[stepIndex];
      // Update assessment for Raini (village_id = 1) dynamically to reflect scenario step
      setAssessments((prev) =>
        prev.map((a) => {
          if (a.village_id === 1) {
            return {
              ...a,
              risk_level: step.assessment.risk_level,
              compound_risk_score: step.assessment.compound_risk_score,
              flood_risk_score: step.assessment.flood_risk_score,
              landslide_risk_score: step.assessment.landslide_risk_score,
              primary_hazard: step.assessment.primary_hazard,
              lead_time: {
                ...a.lead_time,
                minutes: step.assessment.estimated_lead_time_minutes,
                hours: step.assessment.estimated_lead_time_minutes
                  ? Number((step.assessment.estimated_lead_time_minutes / 60).toFixed(2))
                  : null,
                trend_description: `Step ${step.step}: ${step.description}`,
              },
              rainfall_1h_mm: step.environmental_inputs.rainfall_intensity_mm_hr,
              rainfall_24h_mm: step.environmental_inputs.rainfall_accum_24h_mm,
              soil_moisture_pct: step.environmental_inputs.soil_moisture_pct,
              river_level_m: step.environmental_inputs.river_level_m,
              river_rate_of_rise_m_per_hr: step.environmental_inputs.river_rate_of_rise_m_hr,
              action: {
                ...a.action,
                action: step.decisions.action,
                nearest_shelter_name: step.decisions.recommended_shelter,
                affected_zone: step.decisions.affected_zone,
              },
            };
          }
          return a;
        })
      );
    }
  };

  return (
    <div className="p-6 max-w-[1600px] mx-auto space-y-6">
      {/* Header Banner */}
      <div className="flex flex-wrap items-center justify-between gap-4 bg-slate-900 border border-slate-800 p-5 rounded-2xl shadow-lg">
        <div>
          <span className="text-xs font-black tracking-widest text-blue-400 uppercase bg-blue-950/60 border border-blue-800/80 px-2.5 py-1 rounded-full">
            Smart India Hackathon 2026 &bull; Problem Statement 26192
          </span>
          <h1 className="text-2xl font-black text-white mt-2">
            PRALAYADARSHI: Early Warning & Compound Disaster Decision Support
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Deterministic Physics + Multi-Hazard Real-Time Lead-Time Engine & Safe Evacuation Routing
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <button
            onClick={handleOpenCitizenCard}
            className="px-4 py-2.5 bg-gradient-to-r from-red-600 to-rose-600 hover:from-red-500 hover:to-rose-500 text-white font-bold text-xs rounded-xl shadow-lg shadow-red-900/30 transition-all flex items-center space-x-2"
          >
            <span>📱</span>
            <span>View Citizen Warning Card (PRD §18)</span>
          </button>
        </div>
      </div>

      {/* 12-Step PRD §23 Scenario Simulation Player */}
      {scenarioSteps.length > 0 && (
        <ScenarioPlayer
          steps={scenarioSteps}
          currentStepIndex={currentStepIndex}
          onStepChange={handleStepChange}
          onShowCitizenCard={handleOpenCitizenCard}
        />
      )}

      {/* The 4 North Star Decision Panes (PRD §1 & §12) */}
      <NorthStarDecisionPanes
        assessment={selectedAssessment}
        onOpenCitizenCard={handleOpenCitizenCard}
      />

      {/* Village Catchments & Pilot Sectors */}
      <VillageCatchmentList
        assessments={assessments}
        selectedVillageId={selectedVillageId}
        onSelectVillage={setSelectedVillageId}
      />

      {/* Citizen Plain-Language Warning Modal */}
      <CitizenAlertModal
        card={citizenCard}
        isOpen={isCitizenModalOpen}
        onClose={() => setIsCitizenModalOpen(false)}
      />
    </div>
  );
}
