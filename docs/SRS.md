# Software Requirements Specification

**Version** 1.1 · Adapted from ISO/IEC/IEEE 29148
*Shall* = mandatory. *Should* = recommended, omission requires recorded justification.

## Conventions

`SRS-F-<AREA>-<n>` functional · `SRS-NF-<CAT>-<n>` non-functional · `SRS-D-<n>` data ·
`SRS-I-<n>` interface

## Response states

| State | Meaning | Scoring |
|---|---|---|
| `PASS` | Meets threshold | numerator + denominator |
| `FAIL` | Does not meet | denominator; raises Finding |
| `NA` | Absent, or gate false | excluded from both |
| `UNABLE` | Present, not assessable; reason required | excluded from score, reported as coverage |

`UNABLE` is deliberately distinct from `NA`. Conflating them hides assessment gaps in the
denominator.

## Audit lifecycle — `AUD`

1. Audit creatable and fully configurable with no network, including a previously unknown site.
2. Immutable code assigned at creation.
3. Instrument and standard versions recorded at creation; audit bound to them for life.
4. Sector captured from the twelve source categories; selects the instrument.
5. Team roster with roles: measurement, form, photography, user group.
6. Auditor name, profession, organisation captured.
7. **No transition to `CLOSED` while any item is `UNANSWERED`.**
8. Deferred items enumerated at closure; explicit acknowledgement required.
9. Reopening restricted to head surveyor; logged.
10. Approval locks all responses; later changes produce a new report version.

## Questionnaire engine — `QST`

1. Instruments defined as versioned JSON interpreted at runtime, **not compiled code**.
2. Display conditions evaluated against prior responses; gated items shown only when the condition holds.
3. When a gating answer excludes a branch, descendants set to `NA` automatically with a system reason naming the gate.
4. Answer types: boolean, tri-state with `UNABLE`, measurement with unit, single select, multi select, free text, count-pair.
5. Threshold tables supported where required quantity derives from a measured total.
6. **No silent blanks.** Every item resolves to a state or is explicitly deferred.
7. Reusable question groups defined once, instantiated at multiple locations. Checklist §5 and §6 repeat verbatim inside §9 — define once so a handrail change propagates.
8. Default order follows the travel chain.

## Measurement — `MSR`

1. Canonical storage: **integer tenths of a millimetre**.
1a. Both sources are imperial. Conversion rounds conservatively — **minima down, maxima up** — so conversion can never turn a failing measurement into a passing one. Rounding direction stored per threshold.
2. Entry accepted in mm, cm, inches or feet-and-inches; converted on entry, entered unit retained for display.
3. Slope stored as integer rise/run pair; entry as ratio, percentage or degrees.
4. Measured value persisted alongside derived state, so re-evaluation against another standard needs no re-survey.
5. `PASS`/`FAIL` derived automatically by applying the requirement operator.
6. Auditor may override the derived state; **free-text justification mandatory**.
7. Implausible values flagged for confirmation, not rejected.
8. No rounding before comparison.

## Evidence — `EVD`

1. Photographs initiated from within an item context, bound automatically — no manual association step.
2. Each object records timestamp, capturing user, coordinates where available.
3. Images resized to 1600 px long edge, JPEG q75, before persistence.
4. Original retained locally until upload confirmed, then discarded.
5. Voice notes recordable and bound to an item.
6. **A `FAIL` requires at least one evidence object before closure**, subject to an override that records a reason.
7. Consent recorded where identifiable persons appear; non-consented images excluded from issued reports.

## Sync — `SYN`

1. Entire lifecycle to closure functions with no network at any point.
2. Every write committed to local durable storage before success is reported to the user.
3. Each mutation carries a client-generated ID; applied idempotently.
4. **Structured data transmitted to completion before any imagery upload begins.**
5. Resumable after interruption without duplication or loss.
6. Conflicts last-writer-wins at field granularity; superseded value retained in history.
7. Failed mutations retried with exponential backoff, never silently discarded.
8. Pending mutation and object counts displayed to the user.

## Guidance — `GUI`

1. Plain-language guidance on every item: what is assessed and why.
2. Measurement-method note on every dimensional item: where to measure from and to.
3. Source diagrams displayed inline, available offline.
4. Guidance editable as content by an administrator without a release.

## Scoring — `SCR`

1. Weighted conformance score per section and overall.
2. `NA` excluded from numerator and denominator.
3. `UNABLE` excluded from score, reported separately as coverage deficit.
4. Per-item severity weight applied.
5. Failure of a **blocking** item caps the section score at a configured maximum regardless of other passes.
6. **No score displayed or exported without its coverage percentage.**
7. Computation deterministic and reproducible from stored responses alone.

```
score(s) = min( Σ(w_i for PASS in s) / Σ(w_i for PASS∪FAIL in s) × 100 , cap(s) )
coverage(s) = |PASS ∪ FAIL| / |items in s not NA|
```

## Recommendations — `REC`

1. At least one template per requirement, keyed to failure mode.
2. Templates interpolate measured value, required value, computed deficit.
3. Generated text editable; edit records editor and timestamp without discarding the original.
4. Priority from severity weight; effort band of immediate / short term / capital works.
5. Template edit frequency tracked, to drive template improvement.
6. Where no template exists, emit a placeholder that **blocks approval** until replaced.
7. Text describes a **departure from the cited minimum standard**. Never asserts a legal violation — no KP statute binds the Code.

## Report and sign-off — `RPT`

1. Draft available within five minutes of reaching `SYNCED`.
2. Every unapproved report visibly watermarked as draft on every page.
3. Order: cover; executive summary; methodology and team; coverage statement; section results; prioritised action plan; full item appendix; evidence appendix; approval block.
4. **Coverage statement precedes all scores.**
5. Names standard and version applied; discloses any item where the applied threshold differs from the Code.
6. Exports to DOCX and PDF.
7. Approval requires an authenticated reviewer or admin; records identity and timestamp.
8. Issued versions immutable and all retained.
9. States the legal status of the standard, including whether any provincial statute binds it.
10. `ADVISORY` and `UNSOURCED` findings appear in a **separate advisory section**, visually distinct.

## Standards administration — `STD`

1. Standards and requirements creatable and versionable through the console.
2. Each requirement carries a citation to its clause.
3. Where checklist and Code values differ, both storable, one marked applied.
4. Publishing a new version never alters an existing audit.
5. Guidance text and diagrams editable without a release.
6. **A requirement supports multiple thresholds** discriminated by applicability — at minimum construction status (new/existing) and location (interior/exterior). The Code sets different values for each.
7. Each requirement carries authority: `BINDING` (Code), `ADVISORY` (Design Manual, or a Code clause phrased *should* / *where possible*), `UNSOURCED` (checklist only).
8. **`ADVISORY` and `UNSOURCED` requirements never generate a `FAIL`.** Advisory observation only.

## Users and access — `USR`

1. Accounts created only by an administrator. No self-service registration.
2. Four roles: surveyor, head surveyor, reviewer, administrator.
3. Permissions enforced by row-level security **at the database**, not solely in client code.
4. Deactivating a user immediately invalidates their ability to sync.
5. At least two accounts hold the administrator role at all times.

## Data — `D`

1. Structured audit data under 2 MB per completed audit.
2. Evidence referenced by key; binary content never in the database.
3. Referential integrity enforced across audits, responses, evidence, findings, reports.
4. A response unique per audit and question.
5. A finding exists only for a `FAIL` response.
6. Superseded response values retained in an append-only history table.
7. Full database export monthly to organisation-controlled storage.
8. Evidence containing identifiable persons without consent retained but never in an issued report.
9. Local device data encrypted at rest.
10. Retention: audits indefinitely; local copies discarded after confirmed sync; unconsented imagery reviewed annually.
11. **Site record captures ownership type, gross floor area and construction status** — Code 3.2.4 exempts existing privately-owned public-use buildings under 2,500 sq ft, and 5.2.3 varies the ramp threshold by construction status.
12. Where the site satisfies an exemption, affected items set to `NA` automatically with the exempting clause recorded as the reason.

## Interfaces — `I`

1. One item per screen; code, prompt, guidance affordance, answer control and evidence control visible without scrolling on the reference device.
2. Item-to-item navigation in no more than one deliberate gesture.
3. Persistent completeness indicator: answered, deferred, remaining.
4. Touch targets **48 × 48 dp** (MD3; stricter than the original 44).
5. Pass, fail, NA and unable distinguishable by shape and text, not colour alone.
6. Usable at 200 % text scaling without truncation.
7. All strings resolved through a resource layer; none hard-coded.
8. Layout direction-agnostic ahead of RTL. *(v2)*
9. Rear camera at resolution sufficient for a 1600 px long edge after resizing.
10. Location read where granted; fully functional where denied, recorded as unavailable.
11. Microphone for voice notes; fully functional where denied.
12. Free storage checked before an audit; warn below ~30 MB.
13. Supabase over PostgREST with a bearer token from Supabase Auth.
14. All database access subject to RLS. **No client holds a service-role key.**
15. R2 uploads over HTTPS using pre-signed, time-limited URLs from the backend.
16. Console generates DOCX in-browser; PDF via the browser print pipeline.
17. Build pipeline produces a signed APK on tagged commits.
18. TLS 1.2 or later for all traffic.
19. Sync degrades gracefully on intermittent connectivity, resuming from the last acknowledged mutation.
20. Object uploads resumable from a byte offset.
21. 2000 ms round-trip latency tolerated without user-visible failure.

## Non-functional

### Accessibility — `ACC` (release gate)

1. WCAG 2.2 Level AA, field app and console.
2. Fully operable with TalkBack. **Automated tooling cannot verify this — a manual pass by an actual screen-reader user is required.**
3. Console fully keyboard-operable with a visible focus indicator throughout.
4. Text contrast ≥ 4.5:1; non-text interface contrast ≥ 3:1.
5. No information conveyed by colour alone.
6. All form controls programmatically labelled.

### Performance — `PRF`

1. Item-to-item navigation < 150 ms on the reference device.
2. Cold start to resumable audit < 4 s.
3. Photo capture to persisted, resized evidence < 2 s.
4. < 12 % battery per hour sustained field use, excluding camera.
5. Draft report generation < 5 min for 250 items and 100 evidence objects.

### Reliability — `REL`

1. No committed response or evidence lost on process termination, battery exhaustion or forced close.
2. Field capture availability independent of backend availability.
3. Backend availability target 99.5 % monthly, excluding provider maintenance and free-tier pauses.
4. Scheduled keep-alive prevents free-tier suspension; its failure raises an alert.

### Security — `SEC`

1. TLS 1.2+.
2. Local storage encrypted at rest.
3. No service-role or admin credential embedded in a distributed client.
4. Pre-signed upload URLs expire within 15 minutes.
5. Approval and reopening written to an append-only log no role can modify.
6. Device loss mitigated by account revocation and encryption at rest. Remote wipe out of scope.

### Maintainability — `MNT`

1. One language across all components.
2. No custom framework or unconventional architectural pattern.
3. Runbook covering deploy, key rotation, database unpause, user provisioning, instrument editing, backup restore and sync failure diagnosis — written for a reader unfamiliar with the codebase.
4. Instrument content and guidance modifiable by a non-developer through the console.
5. At least one person other than the author holds full admin credentials **and has performed a deployment unaided**.
6. All repositories, service accounts and domains owned by an organisational identity, never personal.
7. A backup restore tested at least once before handover.

### Cost — `CST`

1. Recurring infrastructure cost zero at projected volume. *(iOS distribution would break this — see ADR-003.)*
2. Administrator alerted at 70 % of any free-tier quota.
3. No component requires a paid tier before 50 completed audits.

## Verification

| Group | Method | Approach |
|---|---|---|
| `AUD` | T | State-machine tests over every legal and illegal transition |
| `QST` | T | Fixture instruments exercising each branch and answer type |
| `MSR` | T | Property-based tests over conversion; round-trip equality |
| `EVD` | D | Field demonstration on reference device including permission-denied paths |
| `SYN` | T | Simulated partition, forced kill mid-sync, duplicate mutation replay |
| `SCR` | T | Golden-file tests including `NA`-heavy and blocking-failure cases |
| `REC` | I | Template review against the divergence log; placeholder-blocks-approval test |
| `RPT` | D+I | Three fixture audits; inspect ordering, watermark, disclosure |
| `STD` | T | Publish a new version, assert prior audits unchanged |
| `USR` | T | RLS policy tests attempting cross-role reads with a valid token |
| `ACC` | I+D | Automated scan **plus** manual TalkBack pass by a screen-reader user |
| `PRF` | T | Instrumented timing on real hardware, not an emulator |
| `REL` | T | Kill-and-resume matrix; keep-alive failure alert |
| `SEC` | I+T | Credential scan of the built APK; pre-signed URL expiry |
| `MNT` | I | Handover checklist signed at Phase 5 exit |
| `CST` | A | Quota projection against measured per-audit consumption after pilot |
