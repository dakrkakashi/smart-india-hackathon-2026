import { RiskLevel } from '../types/risk';

export const RISK_HEX_COLORS: Record<RiskLevel, string> = {
  RED: '#dc2626',
  ORANGE: '#d97706',
  YELLOW: '#eab308',
  GREEN: '#059669',
};

export const RISK_BG_CLASSES: Record<RiskLevel, string> = {
  RED: 'bg-red-500/20 text-red-400 border-red-500/60',
  ORANGE: 'bg-amber-500/20 text-amber-400 border-amber-500/60',
  YELLOW: 'bg-yellow-500/20 text-yellow-300 border-yellow-500/60',
  GREEN: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/60',
};

export const RISK_BADGE_CLASSES: Record<RiskLevel, string> = {
  RED: 'bg-red-600 text-white',
  ORANGE: 'bg-amber-600 text-white',
  YELLOW: 'bg-yellow-500 text-slate-950 font-bold',
  GREEN: 'bg-emerald-600 text-white',
};

export function getRiskHex(level: RiskLevel): string {
  return RISK_HEX_COLORS[level] || RISK_HEX_COLORS.GREEN;
}
