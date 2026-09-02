# ADR-001: Offline-first, device as system of record

**Status:** Accepted

## Context

Audits happen inside stairwells, basements and rural facilities across Khyber Pakhtunkhwa.
Connectivity at the point of capture cannot be assumed.

## Decision

The device is the system of record until sync. Every write commits to local SQLite before
the user is told it succeeded. The entire audit lifecycle up to closure functions with no
network connection at any point.

## Consequences

- Rejected: PWA. Android background sync and large-file camera handling are not reliable
  enough to risk field data loss. Rejected on reliability, not cost.
- Rejected: any design treating the server as authoritative during capture.
- Requires an outbox with client-generated idempotent mutation IDs.
- Conflict resolution is last-writer-wins at field granularity, superseded values retained.
- Structured data syncs before imagery, so a partial sync still delivers findings.

## Cost of reversing

Total. This decision shapes the data layer, the sync design and the client choice. It is
not retrofittable.
