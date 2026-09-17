# SIH 2026 Submission Deck Creation Plan

## Feature Name
PRALAY — SIH 2026 6-Slide Presentation (.pptx & .pdf)

## Status
COMPLETED ✅

## Overview
Created the official Smart India Hackathon 2026 idea-submission presentation for PRALAY (SIH PS 26192, Flash Flood Prediction System for Hilly Regions). The deck strictly follows the SIH 2026 template: **exactly 6 slides** — (1) Title Page, (2) Proposed Solution, (3) Technical Approach, (4) Feasibility and Viability, (5) Impact and Benefits, (6) Research and References.

## Problem Statement Alignment
- Organization: Ministry of Home Affairs | Department: NDRF / DM Division | Theme: Disaster Management | Category: Software
- PS 26192: integrate rainfall, soil moisture, slope stability, historical inventories, and real-time IoT into hyper-local village/ward-level forecasts with actionable lead time for evacuation.

## Messaging Rules (from `plans/prd file`)
- USP line: **"Compound Risk → Lead Time → Action"** (never "AI + IoT + GIS disaster management platform")
- Structure solution around 4 North Star questions: WHERE / HOW SEVERE / HOW SOON / WHAT NOW
- Use "estimated lead time" phrasing — never guaranteed warning time
- Do NOT claim achieved prediction accuracy; targets are: FPR < 10%, FNR < 5%, F1 > 0.90, lead time 30–45 min
- Risk scale: GREEN / YELLOW / ORANGE / RED
- Final message: **DETECT EARLIER. IDENTIFY LOCALLY. ACT IN TIME.**

---

## Design System
- **Base:** Dark navy (#0B1F3A) + card surfaces; accent roles: GREEN #22C55E, YELLOW #FACC15, ORANGE #F97316, RED #EF4444
- **Layout:** Asymmetric card grids, clean padding, bold metric callouts
- **Signature callout:** "35 minutes" lead-time stat card
- **16:9** widescreen (13.333 in × 7.5 in)

---

## Completed Tasks

### Phase 1 — Content Sourcing & Script (Completed ✅)
- [x] 1.1 Single source of truth script: `pralay/scripts/ppt_content.py` & `plans/SIH_PPT_CONTENT_STORYBOARD.md`
- [x] 1.2 Approved slide copy respecting all guardrail messaging rules

### Phase 2 & 3 — Deck Architecture & Python Generator (Completed ✅)
- [x] 2.1 Native vector shapes, cards, badges, and multi-column layouts via `python-pptx`
- [x] 3.1 Script: `pralay/scripts/build_sih_deck.py`
- [x] 3.2 Automated validation assertions (slide count == 6, guardrail keywords, 16:9 widescreen)

### Phase 4 — Slide Implementation (Completed ✅)
- [x] 4.1 **Slide 1 — Title Page**: PS 26192, Theme Disaster Management, Category Software, MHA/NDRF, Hero Tagline, 35 minutes callout, 4-tier risk status strip.
- [x] 4.2 **Slide 2 — Proposed Solution**: Problem vs Solution comparison, 4 North Star Question Cards, Dual-Interface Paradigm (Authority Control Room vs Citizen Alert Card).
- [x] 4.3 **Slide 3 — Technical Approach**: 5-Step Pipeline (Sense → Validate & Fuse → Assess → Predict → Act), Compound Risk formulation, Engineering Safety Guardrails, Tech stack chips.
- [x] 4.4 **Slide 4 — Feasibility and Viability**: 3-Phase Rollout Roadmap (Phase A completed prototype in Chamoli, Phase B IoT telemetry, Phase C State scale), Field Risk Mitigation Matrix, Economic Viability (₹15,000/node).
- [x] 4.5 **Slide 5 — Impact and Benefits**: Target KPI cards (30–45 min lead time, FPR < 10%, FNR < 5%, F1 > 0.90), Stakeholder Benefits (NDRF, Officials, Citizens), Closing Mantra: DETECT EARLIER. IDENTIFY LOCALLY. ACT IN TIME.
- [x] 4.6 **Slide 6 — Research and References**: 4-Quadrant Architecture (Datasets & APIs, Geotechnical Models, Historical Archives, NDMA/WMO/Sendai Standards).

### Phase 5 — Build, Render & QA (Completed ✅)
- [x] 5.1 Generated `PRALAY_SIH_2026_Presentation.pptx` (both root and `pralay/`)
- [x] 5.2 Automated tests passing: `pralay/tests/test_deck_requirements.py` (5/5 tests passed in 0.27s)
- [x] 5.3 Exported publication-ready PDF: `PRALAY_SIH_2026_Presentation.pdf`
- [x] 5.4 Comprehensive speaker notes attached to all 6 slides
