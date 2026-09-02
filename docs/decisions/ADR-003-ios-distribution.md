# ADR-003: iOS distribution

**Status:** Open — decision required before Phase 2
**Date raised:** 2026-09-02
**Supersedes:** PRD v0.3 non-goal NG5 ("Android-only, sideloaded APK")

## Context

PRD v0.3 scoped the field app to Android only, distributed as a sideloaded APK. That
choice was load-bearing for two constraints: no Play Store account ($25 one-off avoided),
and no recurring cost at all.

A stakeholder now requires iOS support.

The application code is not the problem. Expo / React Native is cross-platform, and the
capture, sync and storage layers are platform-agnostic. **Distribution is the problem.**

## The constraint this breaks

There is no free path to running an app on a non-jailbroken iPhone in the field.

| Path | Cost | Viability |
|---|---|---|
| Free Personal Team provisioning | $0 | **Unusable.** Profiles expire after 7 days. The app dies mid-week, every week, and must be re-signed from a Mac with the device physically present. |
| Apple Developer Program + TestFlight | **$99/year** | Works. 100 internal testers, builds valid for a year. |
| Apple Developer Enterprise Program | $299/year | Not eligible. Requires a legal entity with 100+ employees. |
| Public App Store | $99/year + review | Wrong distribution model for an internal tool; also invites App Review on a niche government-facing app. |

$99/year is roughly PKR 28,000/year. Against a stated target of PKR 0/month, this is the
only paid component in the entire stack. Supabase, Cloudflare R2, Cloudflare Pages, GitHub
Actions and APK sideloading are all genuinely free at projected volume.

A second, non-monetary cost: **iOS builds require macOS.** Either a Mac in the team or a
paid CI runner. Expo's cloud build service has a free tier with queue limits; verify
before assuming.

## Options

**A. Android only (status quo).** Zero cost preserved. Any iOS-carrying team member uses a
loaner Android handset for surveys. For a team of 3–6 this may be cheaper than $99/year,
once. Requires someone to actually own the loaner.

**B. Pay the $99.** Cleanest technically. Breaks NFR-CST-1 as written; that requirement
would need to be restated as "zero recurring *infrastructure* cost, with a single
identified per-annum distribution fee." Creates a renewal dependency — a lapsed membership
invalidates the signing certificate and installed builds stop working. That is exactly the
class of failure the continuity requirements exist to prevent, so it must go in the
runbook and on the handover checklist.

**C. Web app for iOS only.** A PWA fallback for iOS users while Android gets the native
build. Rejected: this is precisely the offline reliability trade-off already rejected in
PRD v0.2, and it splits the codebase into two capture implementations — the worst outcome
for maintainability.

## Recommendation

**Option A until the audit volume question is answered.**

The reasoning is proportion, not principle. This project is not yet justified at all —
annual audit volume is unknown and below roughly ten audits a year it should not be built.
Committing to a recurring fee and an annual renewal chore, on a tool that may not clear its
own justification bar, is premature.

If volume clears the bar and an iOS device genuinely cannot be replaced with a loaner,
Option B is correct and $99 is a trivial line against the labour saved. Decide then, with
the number in hand.

## Consequences if B is chosen

- `SRS-NF-CST-1` must be reworded; it currently reads "zero" without qualification.
- Renewal added to the runbook and to `docs/decisions/` as a recurring obligation.
- Certificate expiry added to the handover checklist — a lapsed cert breaks installed
  builds, not just new ones.
- macOS build capability required; confirm the Expo cloud build free tier covers the
  release cadence.
- MD3 on iOS: keep Material, do not go platform-adaptive. One design system is cheaper to
  maintain and this is an internal tool, not a consumer app competing on native feel. See
  `docs/UIUX.md`.

## Open question

Which team members actually carry iOS, and can they be issued an Android handset for
survey days? Nobody has confirmed this is a real constraint rather than an assumed one.
