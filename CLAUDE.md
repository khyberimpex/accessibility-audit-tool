# CLAUDE.md

Operating contract for Claude Code on this repository. Read this before touching anything.

## What this is

An offline-first Android (and possibly iOS — see ADR-003) field application plus a small
web console, replacing a paper-based accessibility audit process for public infrastructure
in Khyber Pakhtunkhwa, Pakistan.

**Internal tool.** One organisation, fixed hand-provisioned roster, no commercial
distribution, no multi-tenancy. Do not build for scale that will never arrive.

## Non-negotiables

These are not preferences. Violating one is a bug, not a style disagreement.

1. **Offline-first.** The device is the system of record until sync. Never `await` a
   network call in a capture path. Every write commits to local SQLite before the user is
   told it succeeded.
2. **Drafts, not verdicts.** The system generates a *draft* report. Only a named human
   approver turns it into an issued one. Never auto-publish.
3. **Standards are data.** Thresholds live in `standards/requirements_seed.json`, never in
   application code. If you find yourself typing `1.12` or `48` into a component, stop.
4. **Boring beats clever.** Every choice is made for the successor maintainer. No custom
   framework, no unusual pattern, no dependency with a thin community. If a competent
   junior can't follow it, rewrite it.
5. **The tool must itself be accessible.** WCAG 2.2 AA is a release gate, not an
   aspiration. An inaccessible accessibility-audit tool is not shippable.
6. **Zero recurring cost.** Free tiers only. Flag any change that would require a paid
   tier before you make it.

## Language and stack

- TypeScript everywhere. One language across field app and console. Do not add a second
  runtime.
- React Native via Expo. Local store: SQLite (`expo-sqlite`) with an outbox table.
- Backend: Supabase free tier (Postgres + Auth + RLS). Photos: Cloudflare R2.
- UI: Material Design 3 via `react-native-paper`. See `docs/UIUX.md` — **dynamic colour
  is disabled deliberately**; do not re-enable it.
- Report rendering happens in the browser. Never introduce a server-side render service.

## Units — read this before writing any comparison

Both source instruments are **imperial**. The Accessibility Code of Pakistan 2006 is in
inches and feet. The checklist mixes inches, feet-and-inches, and one stray metric value.

- Canonical storage is **integer tenths of a millimetre** (`_mm10` suffix on every field).
- Conversion rounds **conservatively**: minima round DOWN, maxima round UP. Unit
  conversion must never turn a failing measurement into a passing one.
- Never compare floats. Never round before comparing.

## Response states

Four states, and the distinction between the last two matters:

| State | Meaning | Scoring |
|---|---|---|
| `PASS` | Element exists and meets threshold | numerator + denominator |
| `FAIL` | Element exists, does not meet threshold | denominator; raises a Finding |
| `NA` | Element absent, or gating condition false | excluded from both |
| `UNABLE` | Present but not assessable; reason required | excluded from score, reported as coverage gap |

Conflating `NA` and `UNABLE` hides real assessment gaps inside the denominator. Don't.

## Legal framing — affects user-facing copy

No Khyber Pakhtunkhwa statute binds the Accessibility Code of Pakistan 2006. KP is the
only province that has not repealed the 1981 Ordinance, and the KP Empowerment of Persons
with Disabilities Bill remains unadopted.

**Findings are departures from a published minimum standard, never legal violations.**
Any string that says "violation", "illegal", or "non-compliant with the law" is wrong.
Use "does not meet", "departs from", "below the Code minimum".

## Standards authority

Every requirement carries an authority status:

- `BINDING` — stated in the Code. May generate a `FAIL`.
- `ADVISORY` — Design Manual, or a Code clause phrased as *should* / *where possible*.
  **Never generates a `FAIL`.** Advisory observation only.
- `UNSOURCED` — checklist only, no Pakistani basis. Same rule as advisory.

Seven requirements are currently `UNSOURCED`, including the 5 lbf door-force test and the
whole van-accessible-parking concept. Both are ADA imports.

## The state of the instrument

`standards/standards_mapping.csv` compares 114 requirements. **Twelve agree.**
43 Code requirements have no checklist item yet — they must be authored before pilot.
24 conflict outright.

**The mapping is not consultant-reviewed. No threshold may be cited in an issued report
until it is.** Treat this as a hard gate.

## Task ergonomics

The app optimises for the ~250 repetitive captures, and adds friction to three actions:

- Overriding a derived verdict
- Closing an audit
- Approving a report

Make capture fast. Make those three deliberate. If overriding a FAIL is as quick as
recording one, findings will get overridden.

Launch behaviour: open directly on the next unanswered item of the active audit. No
dashboard, zero taps to work. One persistent jump control that accepts an item code
(`6.3`) or a word (`ramp`), because surveyors move through a building physically, not in
document order.

## Performance budget

Reference device: mid-range Android, 2 GB RAM, Android 10.

| Target | Budget |
|---|---|
| Item-to-item navigation | < 150 ms |
| Cold start to resumable audit | < 4 s |
| Photo capture to persisted evidence | < 2 s |
| Battery, sustained field use | < 12 %/hour excluding camera |

**Run the performance spike on real hardware in week one of Phase 2.** If React Native
can't hold 150 ms on the reference device, that is a stack-level finding and must surface
early, not after the app is built.

## Working method — GSD

This project uses the GSD phase loop: **Discuss → Plan → Execute → Verify → Ship**.

- Do not start executing during Discuss. Capture decisions first.
- One phase per fresh context. Do not carry a full build history in one window.
- Every phase ends with a written verification against the spec, not a claim of success.
- Specs live in `docs/`. If code and spec disagree, the spec is wrong or the code is —
  say which, do not silently pick one.

## Repository map

```
CLAUDE.md              this file
docs/PRD.md            what and why, scope, risks, release plan
docs/SRS.md            numbered, testable requirements
docs/UIUX.md           MD3 system, interaction rules, accessibility gates
docs/ARCHITECTURE.md   stack, data model, sync, deployment
docs/decisions/        ADRs — one file per irreversible choice
standards/             the single source of truth for thresholds
```

`standards/mapping_data.py` is the source; the CSV, the JSON seed and the LaTeX table are
all generated from it by `generate.py`. **Edit the source, regenerate. Never hand-edit a
generated file.**

## Things that will look like bugs but are not

- The colour palette is harsh. Deliberate — surveyors read this in direct sun and in
  unlit stairwells.
- The evidence block is styled as an obstacle. Deliberate — it is one.
- `UNABLE` requires typing a reason. Deliberate.
- Some sections have no items at all for some sectors. Correct — instruments are
  sector-gated.

## Open blockers

1. **Annual audit volume is unknown.** Below ~10 audits/year this project should not be
   built. Nobody has produced the number.
2. Consultant review of the standards mapping is unsigned.
3. 43 instrument items unauthored.
4. Severity weights and blocking-item designations unassigned.
5. iOS distribution decision open — see `docs/decisions/ADR-003-ios-distribution.md`.
