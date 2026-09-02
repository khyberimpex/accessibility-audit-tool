# Architecture

## Shape

Device is authoritative until sync. Everything else follows from that.

```
Android handset (2 GB RAM, Android 10+)
  Expo / React Native  ──►  Questionnaire engine  ──►  SQLite  ◄──  Outbox
                                    │                                  │
                            Instrument cache                           │
                            (JSON + diagrams)                          │
                                                                       ▼
                                          Supabase (Postgres + Auth + RLS)  ── structured
                                          Cloudflare R2 (objects)           ── imagery

Browser (reviewer)
  React console  ──►  DOCX generator (client-side)  ──►  browser print-to-PDF
```

No server is administered. No render service exists.

## Decisions and why

| Decision | Reason |
|---|---|
| SQLite as field system of record | Any design treating the server as authoritative during capture cannot satisfy offline-first. |
| Outbox pattern | Decouples capture latency from connectivity; makes retry, ordering and idempotence tractable. |
| Split storage: Supabase + R2 | Supabase's 1 GB file allowance binds at roughly 80 audits. R2's 10 GB with no egress fee binds at roughly 800. |
| Client-side report rendering | Removes an entire service and its recurring cost. |
| RLS at the database | Client code is not a trust boundary. A modified APK must not read another surveyor's data. |
| Single language (TypeScript) | Maintainability by a successor outweighs any per-component optimum. |

## Rejected

- **Self-hosted Appwrite** — capable, but a VPS means patching, backups and uptime. Fails cost and successor-maintainability.
- **Appwrite Cloud** — 2 GB storage holds ~160 audits of photos; imagery moves to R2 regardless. Once split, Supabase's larger regional community wins on handover.
- **Firebase** — Firestore fits this relational domain poorly; costs scale unpredictably.
- **Custom API on a VPS** — over-built for six surveyors.
- **PWA** — cheapest, but Android background sync and large-file camera handling remain unreliable enough to risk field data loss. Rejected on reliability, not cost.

## Free-tier limits

Verified September 2026. Re-check before Phase 2; tiers change without notice.

| Resource | Free | Projected |
|---|---|---|
| Supabase database | 500 MB, shared CPU, 500 MB RAM | ~2 MB/audit. RAM is the real ceiling — keep aggregation client-side. |
| Supabase egress | 5 GB/month | Structured data only. **Never proxy imagery through Supabase** or this binds first. |
| Supabase file storage | 1 GB | Unused by design. |
| R2 storage | 10 GB-month | ~12 MB/audit → ~800 audits. |
| R2 egress | none charged | The reason R2 was chosen. |
| R2 Class A (writes) | 1M/month | ~60/audit. Unreachable. |
| R2 Class B (reads) | 10M/month | Unreachable. |
| Cloudflare Pages builds | 500/month | Far above need. |
| GitHub Actions | 2,000 min/month | ~10 min per APK build. |

**Known annoyance:** Supabase pauses inactive free projects after about a week. Mitigate
with a scheduled GitHub Action keep-alive; document manual unpause in the runbook. Do not
discover this in the field.

## Data model

Entities: `standard` → `requirement` → `threshold`; `instrument` → `question`;
`site` → `audit` → `response` → `evidence` / `finding` → `recommendation`; `report`.

Two things differ from a naive model:

**`threshold` is separate from `requirement`.** The Code sets different values by
construction status (new vs existing) and by location (interior vs exterior). Ramp running
slope maxes at 1:12 for new build but permits up to 1:8 for existing development *only*
where an alternative stepped approach exists. One threshold per requirement cannot express
that.

**`site` carries scoping attributes** — ownership type, gross floor area, construction
status. Code clause 3.2.4 exempts existing privately-owned public-use buildings under
2,500 sq ft. Without these three fields the exemption cannot be evaluated, and exemption
drives automatic `NA` propagation across whole branches.

## Sync

1. Connectivity detected.
2. **Structured data first.** Mutations pushed in order, idempotent by client-generated
   `mutation_id`. Conflicts resolve last-writer-wins at field granularity; superseded
   values retained in history.
3. **Imagery second, lower priority.** Resumable uploads from byte offset. Local original
   discarded only on confirmed upload.

Findings must reach the server before megabytes of photos do. A partial sync should still
leave the reviewer with something to read.

## Performance

Reference device: mid-range Android, 2 GB RAM, Android 10.

Levers: read only from local SQLite and never await the network in a capture path; parse
the instrument once at audit open and hold it in memory; render one item rather than
virtualising a long list; resize images off the UI thread.

**Risk:** React Native on 2 GB Android 10 is exactly where the 150 ms item-navigation
target gets tested. If it doesn't hold, the fallback is native Kotlin, which breaks the
single-language rule. Run the spike on real hardware in week one of Phase 2 — not after
the app is built.

## Distribution

Android: signed APK built by GitHub Actions on tag, sideloaded to a known fleet. No Play
Store account.

iOS: **open decision.** No free path exists. See `decisions/ADR-003-ios-distribution.md`.

## Continuity

Abandonment is the most probable failure mode for an internally-built tool, and the
highest-cost one.

- Runbook covering deploy, key rotation, database unpause, user provisioning, instrument
  editing, backup restore, sync failure diagnosis — written for someone who has never seen
  the codebase.
- At least one person other than the author holds full admin credentials **and has
  performed a deploy unaided**.
- All repositories, service accounts and domains owned by an organisational identity,
  never a personal account.
- Monthly database export to organisation-controlled storage; one restore tested before
  handover.
- Instrument and guidance content editable without a release, so ordinary changes never
  require a developer.
