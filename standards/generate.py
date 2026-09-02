import csv, json, re
from collections import Counter, OrderedDict
from mapping_data import ROWS

# ---------------------------------------------------------------- CSV
with open("standards_mapping.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["requirement_key", "topic", "checklist_items", "checklist_value",
                "code_clause", "code_value", "authority", "applies",
                "verdict", "applied_value", "note"])
    for r in ROWS:
        w.writerow([r["key"], r["topic"], r["cl"], r["clv"], r["ref"], r["cv"],
                    r["auth"], r["app"], r["verdict"], r["applied"], r["note"]])

# ---------------------------------------------------------------- JSON seed
seed = {
    "standard": {
        "name": "Accessibility Code of Pakistan",
        "version": "2006",
        "authority_status": "BINDING_NO_PROVINCIAL_STATUTE_KP",
        "companion": "Design Manual and Guidelines for Accessibility 2006 (ADVISORY)",
        "unit_system": "imperial",
        "canonical_storage": "integer tenths of a millimetre",
        "rounding_rule": "minima round DOWN, maxima round UP, so unit conversion can never turn a fail into a pass",
        "note": "As of 2026 no Khyber Pakhtunkhwa statute binds this Code. Findings are departures from a minimum standard, not legal violations."
    },
    "requirements": [
        OrderedDict([
            ("key", r["key"]),
            ("topic", r["topic"]),
            ("citation", r["ref"] if r["ref"] != "-" else None),
            ("authority", r["auth"]),
            ("applies", r["app"]),
            ("code_value", r["cv"] if r["cv"] != "not specified" else None),
            ("checklist_value", r["clv"]),
            ("checklist_items", [i.strip() for i in r["cl"].split(",") if i.strip() and i.strip() != "-"]),
            ("verdict", r["verdict"]),
            ("applied_value", r["applied"]),
            ("threshold_mm_tenths", None),
            ("operator", None),
            ("severity", None),
            ("blocking", None),
            ("resolved", False),
            ("note", r["note"] or None),
        ]) for r in ROWS
    ],
}
with open("requirements_seed.json", "w", encoding="utf-8") as f:
    json.dump(seed, f, indent=2, ensure_ascii=False)

# ---------------------------------------------------------------- LaTeX
def esc(s):
    if s is None:
        return ""
    s = str(s)
    for a, b in [("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"),
                 ("$", r"\$"), ("#", r"\#"), ("_", r"\_"),
                 ("{", r"\{"), ("}", r"\}"), ("~", r"\textasciitilde{}"),
                 ("^", r"\textasciicircum{}"),
                 ("<", r"$<$"), (">", r"$>$")]:
        s = s.replace(a, b)
    return s

VLABEL = {
    "CODE_STRICTER":      r"\vcode",
    "CHECKLIST_STRICTER": r"\vchk",
    "CONFLICT":           r"\vconf",
    "MATCH":              r"\vmatch",
    "GAP_CHECKLIST":      r"\vgapc",
    "GAP_CODE":           r"\vgapk",
}

topics = OrderedDict()
for r in ROWS:
    topics.setdefault(r["topic"], []).append(r)

lines = []
for topic, rows in topics.items():
    lines.append(r"\multicolumn{5}{@{}l@{}}{\textbf{\color{pedogreen}%s}}\\[2pt]" % esc(topic))
    for r in rows:
        item = esc(r["key"])
        cl = esc(r["clv"])
        if r["cl"] != "-":
            cl = r"\textit{%s} --- %s" % (esc(r["cl"]), cl)
        cv = esc(r["cv"])
        if r["ref"] != "-":
            cv = r"\textit{%s} --- %s" % (esc(r["ref"]), cv)
        applied = esc(r["applied"])
        if r["auth"] == "UNSOURCED":
            applied += r"\newline\footnotesize\textcolor{warn}{no Code basis}"
        elif r["app"] not in ("ALL",):
            applied += r"\newline\footnotesize\textcolor{muted}{%s}" % esc(r["app"])
        note = ""
        if r["note"]:
            note = r"\newline\footnotesize\textcolor{muted}{%s}" % esc(r["note"])
        lines.append(r"\texttt{\footnotesize %s} & %s & %s & %s & %s%s\\[3pt]" % (
            item, cl, cv, VLABEL[r["verdict"]], applied, note))

counts = Counter(r["verdict"] for r in ROWS)
summary = "\n".join(
    r"%s & %d & %.0f\%% \\" % (VLABEL[k], counts[k], 100.0 * counts[k] / len(ROWS))
    for k in ["MATCH", "CODE_STRICTER", "CHECKLIST_STRICTER", "CONFLICT",
              "GAP_CHECKLIST", "GAP_CODE"]
)

with open("mapping_table.tex", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
with open("mapping_summary.tex", "w", encoding="utf-8") as f:
    f.write(summary + "\n")

print(f"rows: {len(ROWS)}")
print(f"topics: {len(topics)}")
for k, v in counts.most_common():
    print(f"  {k:20s} {v:3d}  {100.0*v/len(ROWS):.0f}%")

# --- emit summary as a complete tabular (avoids \input inside an alignment) ---
_order = ["MATCH", "CODE_STRICTER", "CHECKLIST_STRICTER", "CONFLICT",
          "GAP_CHECKLIST", "GAP_CODE"]
_rows = "\n".join(
    r"%s & %d & %.0f\%% \\" % (VLABEL[k], counts[k], 100.0 * counts[k] / len(ROWS))
    for k in _order)
_tab = (r"\begin{tabular}{@{}lrr@{}}" "\n"
        r"\toprule" "\n"
        r"\textbf{Verdict} & \textbf{Count} & \textbf{Share} \\" "\n"
        r"\midrule" "\n" + _rows + "\n"
        r"\midrule" "\n"
        + r"\textbf{Total} & \textbf{%d} & \textbf{100\%%} \\" % len(ROWS) + "\n"
        r"\bottomrule" "\n"
        r"\end{tabular}" "\n")
with open("mapping_summary.tex", "w", encoding="utf-8") as f:
    f.write(_tab)
print("summary tabular written")

# --- emit the full longtable environment (avoid \input inside an alignment) ---
_head = (r"\begin{longtable}{@{}L{3.0cm}L{6.2cm}L{7.6cm}L{2.5cm}L{5.0cm}@{}}" "\n"
         r"\toprule" "\n"
         r"\textbf{Requirement key} & \textbf{Checklist} & \textbf{Code 2006} & "
         r"\textbf{Verdict} & \textbf{Applied value / note} \\" "\n"
         r"\midrule" "\n" r"\endfirsthead" "\n"
         r"\toprule" "\n"
         r"\textbf{Requirement key} & \textbf{Checklist} & \textbf{Code 2006} & "
         r"\textbf{Verdict} & \textbf{Applied value / note} \\" "\n"
         r"\midrule" "\n" r"\endhead" "\n"
         r"\bottomrule" "\n" r"\endfoot" "\n")
with open("mapping_table.tex", "w", encoding="utf-8") as f:
    f.write(_head + "\n".join(lines) + "\n" + r"\end{longtable}" + "\n")
print("longtable written")
