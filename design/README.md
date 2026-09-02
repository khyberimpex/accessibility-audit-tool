# Design assets

## Figma

File key `m0eF3ftqZuQSSyB4b8fpzC`
https://www.figma.com/design/m0eF3ftqZuQSSyB4b8fpzC

Screen inventory and prototype scope are in the root `README.md`.

## Diagrams

`diagrams/*.puml` are the PlantUML sources for the figures in `docs/SRS.md`. All share
`_style.iuml`. They are text, so they diff and review like code — do not replace them with
exported images.

Rebuild (PlantUML cannot emit PDF directly here, so go via SVG):

```
java -jar plantuml.jar -tsvg diagrams/fig03_class.puml
python3 -c "import cairosvg; cairosvg.svg2pdf(url='diagrams/fig03_class.svg', write_to='diagrams/fig03_class.pdf')"
```

| File | Type |
|---|---|
| fig01_context | system context |
| fig02_usecase | UML use case |
| fig03_class | UML class — note `Threshold` split from `Requirement` |
| fig04_state_audit | audit lifecycle state machine |
| fig05_state_response | response state machine |
| fig06_seq_capture | sequence: measured item capture |
| fig07_seq_sync | sequence: sync, structured before imagery |
| fig08_activity_report | activity: scoring through sign-off |
| fig09_component | component / deployment |
| fig10_er | entity-relationship |

The activity diagram uses swimlanes deliberately — as a single column it renders 4.5x
taller than wide and is unreadable at print size.
