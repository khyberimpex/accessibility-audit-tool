# ADR-004: Material Design 3, with dynamic colour disabled

**Status:** Accepted

## Decision

Material Design 3 via `react-native-paper`, using the **high-contrast** scheme, with
**dynamic colour explicitly disabled**. Material on both platforms if iOS ships — no
platform-adaptive UI.

## Why MD3

Native to Android, which is the primary and possibly only platform. `react-native-paper`
ships MD3 with accessibility roles and TalkBack support already wired, which serves the
WCAG 2.2 AA release gate and the maintainability requirement at the same time. It is less
code to hand over.

MD3's 48 dp touch target is stricter than the 44 dp in `SRS-I-4`. Adopt 48.

## Why dynamic colour is disabled

Material You derives its palette from the user's wallpaper. In an audit tool this would
mean a surveyor's phone background changes what `PASS` and `FAIL` look like, and two
surveyors see different colours for the same finding. Evidence consistency requires a fixed
palette. This is disqualifying, not a preference.

## Why high-contrast, not standard

MD3's standard tonal surfaces are low-contrast by design. Field conditions are direct sun
and unlit stairwells. The comfortable mid-greys are unusable outdoors. Contrast floors:
4.5:1 text, 3:1 non-text.

## Why not platform-adaptive on iOS

One design system is cheaper to build, cheaper to hand over, and this is an internal tool
with a known roster — not a consumer app competing on native feel. Two design languages
would double the component surface for no user benefit.
