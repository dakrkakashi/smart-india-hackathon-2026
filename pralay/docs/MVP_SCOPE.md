# PRALAYADARSHI MVP Scope Guardrails
**Reference: PRD §22 & §29**

## The Four North Star Questions
Every feature, service, and API response must directly serve one or more of these four operational questions:
1. **WHERE is the risk?** (Village / Ward spatial identifier, latitude, longitude, boundary)
2. **HOW SEVERE?** (Risk Level: GREEN, YELLOW, ORANGE, RED; Compound Risk Score 0–100)
3. **HOW SOON?** (Estimated Lead Time in minutes/hours; always explicitly labeled "Estimated")
4. **WHAT NOW?** (Prescribed operational action, designated shelter, evacuation route avoiding hazard corridors)

## Scope Checklist & Guardrails
- [x] **Transparent Weighted Risk Model First**: Initial engine uses deterministic, physical hydrology and geotechnical heuristics (rainfall accumulation, river rate-of-rise, slope angle, soil saturation) before claiming black-box ML.
- [x] **No Unsubstantiated Accuracy Claims**: Metrics reflect test and historical simulation benchmarks.
- [x] **Sensor Failure Transparency**: Missing sensor readings flag the source as UNAVAILABLE or DEGRADED; never assumed safe/zero.
- [x] **Alert Fatigue Protection**: Minimum 30-minute cooldown suppression for recurring alerts of equal severity for any single zone.
- [x] **Bilingual/Plain-Language Citizen Notice**: Citizen interface delivers unambiguous instructions without technical jargon.
