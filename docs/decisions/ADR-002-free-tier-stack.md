# ADR-002: Free-tier managed stack, no administered server

**Status:** Accepted

## Context

Internal tool, single organisation, 3–6 surveyors. Built by one person who is job-hunting
and will not maintain it indefinitely. Target recurring cost PKR 0.

## Decision

Supabase free tier for Postgres, Auth and row-level security. Cloudflare R2 for photo
objects. Cloudflare Pages for the console. GitHub Actions for builds and keep-alive.
Report rendering client-side in the browser.

## Why split storage

Supabase's free file allowance is 1 GB — roughly 80 audits of compressed photos. R2 gives
10 GB with no egress charge, roughly 800. Splitting is slightly more work and buys an
order of magnitude.

Supabase's 5 GB monthly egress makes this a hard rule rather than a preference: proxying
imagery through Supabase would burn the allowance in a few hundred report views.

## Why not self-host

Appwrite self-hosted is technically capable and avoids vendor limits, but a VPS means
patching, backups and uptime. That fails the cost constraint and, more importantly, the
successor-maintainability requirement. The person who inherits this should not need DevOps.

## Consequences

- No server-side rendering component may ever be introduced.
- Supabase pauses inactive free projects after ~1 week; a scheduled keep-alive is a
  functional dependency, not an optimisation.
- Quota alerts at 70 % required.
- Free-tier terms change without notice. Verified September 2026; re-check before Phase 2.
