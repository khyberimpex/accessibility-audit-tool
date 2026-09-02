# UI/UX Specification

Material Design 3, with three deliberate departures. Read the departures before the rest —
they are the parts most likely to be "fixed" back by someone who doesn't know why.

## Departures from stock MD3

### 1. Dynamic colour is disabled

Material You derives the palette from the user's wallpaper. For an audit tool this is
disqualifying: a surveyor's phone background would change what `PASS` and `FAIL` look
like, and two surveyors would see different colours for the same finding. Evidence
consistency depends on the palette being fixed.

Set a static `MD3Theme`. Do not read `DynamicColorIOS` or Android's dynamic scheme.

### 2. High-contrast scheme, not standard

MD3's standard tonal surfaces are low-contrast by design. Field conditions are direct
Peshawar sun and unlit stairwells. Use the high-contrast variant, and treat the comfortable
mid-greys as unusable.

Minimum contrast: **4.5:1 text, 3:1 non-text interface elements** (`SRS-NF-ACC-4`).
Verify on a real handset outdoors, not on a monitor.

### 3. Touch targets at MD3's 48 dp, not the SRS's 44 dp

MD3 specifies 48×48 dp. `SRS-I-4` specifies 44. Adopt 48 — the stricter of the two. The
SRS figure is a floor, not a target.

## Colour semantics

State colour is never the only signal. Every state carries **shape and text** as well
(`SRS-NF-ACC-5`), because colour-blind surveyors exist and because glare flattens hue.

| State | Glyph | Treatment |
|---|---|---|
| `PASS` | ✓ | filled, success container |
| `FAIL` | ✕ | filled, error container, heaviest weight on screen |
| `NA` | — | outlined, neutral |
| `UNABLE` | ? | outlined, warning tone |

Authority status also gets a visible treatment. `ADVISORY` and `UNSOURCED` findings must
be visually distinct from `BINDING` ones, because they can never generate a failure and a
surveyor needs to see that without reading the fine print.

## Interaction principle: fast capture, slow decisions

The app performs roughly 250 repetitive captures per audit and three consequential
decisions. These get opposite treatment.

**Optimise ruthlessly:**
- Launch opens directly on the next unanswered item. No dashboard, no audit picker when an
  audit is active.
- One item per screen. Item code, prompt, guidance affordance, answer control and evidence
  control all visible without scrolling on the reference device (`SRS-I-1`).
- Advance in one gesture (`SRS-I-2`).
- Verdicts derive from measurements automatically. The surveyor enters numbers, not
  judgements.
- Conditional branching and scoping exemptions remove items silently. **This is the largest
  step reduction available** — larger than any navigation change. An exempt building or an
  absent lift should never present items to dismiss.
- One persistent jump control accepting an item code (`6.3`) or a word (`ramp`). Surveyors
  move through a building physically, not in document order.

**Add friction deliberately:**
- Overriding a derived verdict requires a typed justification. No preset reasons — a
  dropdown makes overriding a tap.
- Closing an audit enumerates unanswered, deferred, and `FAIL`-without-evidence items and
  requires explicit acknowledgement.
- Approving a report requires a named approver and locks the responses.

A tool where overriding a `FAIL` is as fast as recording one will have its findings
overridden. That is the failure mode this asymmetry exists to prevent.

## Screen inventory

| Screen | Status | Notes |
|---|---|---|
| Field capture — measured item | Prototyped (Figma) | Reference for all capture screens |
| Field capture — boolean / tri-state | Not built | Simpler variant of the above |
| Override justification | **Not built. Highest risk.** | Where a surveyor talks themselves out of a finding |
| Guidance panel expanded | Not built | Replaces formal training; carries the diagram |
| Item list / section progress | Not built | Secondary to the jump control |
| Site setup with scoping gate | Not built | Captures ownership, floor area, construction status |
| Audit closure | Not built | Friction screen |
| Reviewer console | Not built | Web, not mobile |

**Do not build a full component kit yet.** Build the override flow, guidance panel, item
list and closure first, then let the kit fall out of what those five screens actually
share. Designing a system for 250 items across 12 sectors before Phase 0 has been run is
the over-investment the PRD warns about.

## Accessibility gates

Release-blocking, not aspirational.

- WCAG 2.2 AA across field app and console.
- Fully operable with TalkBack (`SRS-NF-ACC-2`). **Automated tooling cannot verify this.**
  A manual pass by an actual screen-reader user is required, and the user-group participant
  persona is the natural reviewer.
- Console fully keyboard-operable with a visible focus indicator throughout.
- Functional at 200 % text scaling without truncation.
- All form controls programmatically labelled.

`react-native-paper` ships MD3 with accessibility roles already wired. That is a
maintainability argument as much as an accessibility one — it is less code to hand over.

## Copy rules

- Never "violation", "illegal", or "non-compliant with the law". Use "does not meet",
  "departs from", "below the Code minimum". See `CLAUDE.md` for why.
- Cite the clause on screen at the point of measurement, not in an appendix. Where the
  checklist and the Code diverge, say so inline — a surveyor trained on the paper form will
  otherwise apply the old exception from memory.
- Plain-language guidance on every item, and a measurement-method note on every dimensional
  item stating where to measure from and to.

## Localisation

English at launch. All strings externalised from day one, layout direction-agnostic ahead
of Urdu (`SRS-I-7`, `SRS-I-8`). Retrofitting RTL is far more expensive than allowing for it.

## Platform

If iOS ships (see ADR-003), keep Material Design on both platforms. Do not go
platform-adaptive. One design system is cheaper to maintain and to hand over, and this is
an internal tool with a known roster — not a consumer app competing on native feel.
