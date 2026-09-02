# Accessibility Audit Tool

Offline-first field application replacing a paper-based accessibility audit process for
public infrastructure in Khyber Pakhtunkhwa, Pakistan.

**Internal tool.** One organisation, fixed roster, free-tier infrastructure.

## Start here

| If you are… | Read |
|---|---|
| Claude Code, any session | `CLAUDE.md` — the operating contract |
| deciding whether to build this | `docs/PRD.md` — especially the open blockers |
| implementing | `docs/SRS.md` — numbered, testable requirements |
| designing screens | `docs/UIUX.md` |
| choosing infrastructure | `docs/ARCHITECTURE.md` |
| wondering why a choice was made | `docs/decisions/` |

## Project status

Phase 0 (paper shadowing) **not started**. Phase 1 (standards extraction) partly complete —
the mapping is delivered but unreviewed, and 43 instrument items remain unauthored.

**This project is not yet justified.** Annual audit volume is unknown. Below roughly ten
audits a year it should not be built. That number is the first thing to obtain.

## Where truth lives

`standards/mapping_data.py` is the single source for every threshold. The CSV, the JSON
seed and the LaTeX table are generated from it:

```
cd standards && python3 generate.py
```

Edit the source, regenerate. Never hand-edit a generated file.

`standards/requirements_seed.json` is consumed by both the documents and the application.
It lives in the repo precisely so it exists once. **Do not copy it into Claude Project
knowledge as a separate artefact** — point the project at the repo instead, or you
recreate the duplication the generator was built to remove.

## The headline finding

114 requirements were compared between the PEDO checklist and the Accessibility Code of
Pakistan 2006.

**Twelve agree.**

43 Code requirements have no checklist item at all. 24 conflict outright, several with
barely-overlapping ranges. The checklist is substantially an adaptation of United States
ADA guidance, and auditing against it alone silently omits illumination levels, emergency
egress computation, areas of refuge and signage sizing.

## Design

Figma file: `m0eF3ftqZuQSSyB4b8fpzC`
https://www.figma.com/design/m0eF3ftqZuQSSyB4b8fpzC

| Screen | Status |
|---|---|
| Field capture — measured item | Built |
| Field capture — boolean / tri-state | Not built |
| Override justification | Not built. **Build in React, not Figma** — the computation must be real |
| Guidance panel expanded | Not built |
| Audit closure | Not built |
| Jump control / item list | Not built |

These six carry every decision worth testing. Do not attempt to prototype all 250 items.
Take the prototype into Phase 0 shadowing — showing it during the same site visit turns
measurement into a design review at almost no extra cost.

Figma cannot test derived verdicts across a range of inputs, conditional branching at
scale, offline behaviour, or performance. It tests flow, hierarchy, and whether the thing
works one-handed.

## Working method

GSD phase loop: Discuss → Plan → Execute → Verify → Ship. One phase per fresh context.
Specs in `docs/` are the contract; if code and spec disagree, say which is wrong rather
than silently picking one.
