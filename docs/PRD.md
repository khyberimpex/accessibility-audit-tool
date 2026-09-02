# Product Requirements Document

**Version** 0.4 · **Status** Draft · **Classification** Internal tool
**Supersedes** v0.3 (LaTeX). Revised for Markdown, MD3, GSD and the iOS constraint.

## Summary

Accessibility audits are conducted on paper: a team carries printed copies of a 71-page
checklist with ~250 items, records answers and measurements by hand, photographs findings
on personal phones, and reconstructs a report weeks later from notes and an unsorted camera
roll.

This specifies an internal tool replacing that workflow with an offline-first mobile
application, a small web console, and a report generator producing a **reviewable draft**
at survey close.

## Design positions

1. **Offline-first is non-negotiable.** Audits happen in stairwells, basements and rural
   facilities.
2. **The system produces a draft, not a final report.** The source checklist's own method
   prescribes re-evaluation and review before issue. Auto-publishing an unreviewed
   measurement is a liability.
3. **Standards are data, not code.** The checklist derives largely from US ADA guidance;
   the applicable Pakistani instrument is the Accessibility Code of Pakistan 2006.
4. **Boring beats clever.** Every choice serves the successor maintainer.
5. **Fast capture, slow decisions.** Optimise the 250 repetitive captures; add friction to
   overriding a verdict, closing an audit, and approving a report.

## Problem

- Most items are conditional. On paper, a gated item is answered by skipping — indistinguishable from an omission.
- The form offers only Yes and No, so a blank carries three possible meanings.
- Units are inconsistent: inches, feet-and-inches, and one stray metric value.
- The *Recommendation* column — the actual value of an audit — is left blank in the field and written later from memory.
- Photographic evidence is not bound to the finding it supports.
- Two auditors surveying the same building produce materially different reports.
- Repeat audits cannot demonstrate improvement; there is no stable baseline.

## Goals

| | Goal |
|---|---|
| G1 | Survey-to-draft from weeks to under one hour |
| G2 | Eliminate ambiguous and missing responses |
| G3 | Bind every finding to a measurement and evidence |
| G4 | Make output comparable across sites, auditors and time |
| G5 | Reduce training burden by embedding guidance in the instrument |
| G6 | Zero recurring infrastructure cost |
| G7 | Remain operable by someone who did not build it |

## Non-goals

Multi-tenancy, white-labelling, multi-standard comparison reporting, public signup or
account recovery, Play Store distribution, remediation costing, CAD integration,
measurement from photographs, certification or legal compliance determination.

## Users

| Role | Count | Defining constraint |
|---|---|---|
| Field surveyor | 3–6 | One-handed, mid-range phone, poor light, holding a tape measure. May be an untrained volunteer. |
| Head surveyor | 1–2 | Needs completeness visibility before the team leaves site. |
| User-group participant | 1–2/audit | May be a screen-reader user. **This persona is why the tool must meet WCAG 2.2 AA.** |
| Reviewer / admin | 1–2 | Sole approver; maintains the standards library. |

## Scope

**v1 (MVP):** one sector vertical (Education or Health), ~40–60 items not the full 250;
Android field app, offline-first; minimal web console; one standards set; photo capture
bound to item, timestamp and coordinates; draft report to DOCX and PDF.

**v2:** remaining sectors and full item set; re-audit mode against a baseline; portfolio
view; Urdu localisation.

## Standards divergence — the finding that reshaped this plan

114 requirements compared between the checklist and the Code. **Twelve agree.**

| Verdict | Count | Share |
|---|---:|---:|
| Match | 12 | 11% |
| Code stricter | 21 | 18% |
| Checklist stricter | 5 | 4% |
| Conflict | 24 | 21% |
| Absent from checklist | 43 | 38% |
| Absent from Code | 9 | 8% |

Consequences:

- Adopting the Code changes most thresholds and **adds 43 items that do not currently exist**.
- Phase 1 is larger than estimated. The mapping is done; authoring the missing items and obtaining consultant sign-off are not.
- Seven requirements are `UNSOURCED` — checklist-only with no Pakistani basis, including the 5 lbf door-force test and van-accessible parking. Both are ADA imports. Decide: retain as advisory, or drop.
- Adopting the Code's illumination requirement (55 lux minimum) **adds a light meter to the tool kit**.

Worst conflicts: `wc.centreline` (16–18 in vs 18–21 in — barely overlapping);
`parking.marking` (checklist says ground marking not required, Code says it is — direct
contradiction); `assembly.wheelchair.count` (the checklist contradicts *itself*, note says
5 %, table yields ~2.7–8 %, Code says 2 %).

## Legal status of the standard

Khyber Pakhtunkhwa has no provincial statute binding the Accessibility Code. It is the only
province not to have repealed the Disabled Persons (Employment and Rehabilitation)
Ordinance 1981, and the KP Empowerment of Persons with Disabilities Bill remains unadopted.
Punjab's 2022 Act and Sindh's 2018 Act both bind the Code expressly; KP has no equivalent.

Every finding is therefore a **departure from a published minimum standard, not a legal
violation**, and recommendation wording must reflect that.

This opens a different opportunity: with the bill pending and a UN committee recommending
its adoption, comparable audit data is itself an argument for adoption.

## Risks

| Risk | Severity | Mitigation |
|---|---|---|
| **Tool abandoned after author departs** | **Critical** | Continuity requirements as release gates. Runbook, second admin who has deployed unaided, org-owned accounts, tested restore. |
| **Instrument 38 % incomplete against the Code** | **Critical** | 43 items must be authored before pilot. |
| Build effort exceeds value at actual volume | High | Answer the volume question before Phase 2. Below ~10 audits/year, stop. |
| Conflicting thresholds issued as findings | High | Consultant sign-off on the mapping is a release gate for report issue. |
| RN performance on 2 GB Android 10 | High | Spike on real hardware, week one of Phase 2. Fallback breaks the single-language rule. |
| Free-tier terms change or project paused | Medium | Quota alerts at 70 %, weekly keep-alive, monthly export. |
| iOS breaks zero-cost constraint | Medium | See ADR-003. No free path exists. |
| Unclear ownership and credit | Medium | Agree scope, ownership, attribution in writing before Phase 2. |

## Release plan

| Phase | Duration | Outcome |
|---|---|---|
| 0 | 2 weeks | **Paper shadowing.** Two real audits, time each section, record hesitation. Obtain annual volume. **No code. Not optional.** |
| 1 | 5 weeks | Standards extraction. *Mapping delivered.* Remaining: author 43 items, assign severity weights, transcribe Design Manual, consultant sign-off. |
| 2 | 5 weeks | MVP field client, one sector, offline capture, photo binding, local SQLite. Performance spike week one. No sync, no report. |
| 3 | 3 weeks | Supabase schema with RLS, sync, R2 uploads, minimal console. |
| 4 | 3 weeks | Report generation, recommendation templates, sign-off. |
| 5 | 2 weeks | **Handover.** Runbook, second admin, restore test, exit review. A phase, not an afterthought. |
| 6 | — | Pilot on five buildings, then expand instrument coverage. |

## Open blockers

1. **Annual audit volume unknown.** Below ~10/year this should not be built. Blocking.
2. Consultant review of the standards mapping unsigned. Blocking for report issue.
3. 43 instrument items unauthored.
4. Severity weights and blocking-item designations unassigned.
5. Section-score caps unset.
6. iOS distribution decision open (ADR-003).
7. Design Manual not transcribed — scanned, no text layer. Resolves 9 `GAP: CODE` rows.
8. Second administrator unidentified.
9. Redistribution rights for source checklist diagrams unconfirmed.
10. Retention policy for unconsented imagery unset.
