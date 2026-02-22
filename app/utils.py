# app/utils.py
import re
from typing import List, Tuple

# Optimized pattern:
# - [A-Z]{2,5}: Standard acronyms (BP, SOB, HTN)
# - Specific medical shorthand: Pt (Patient), Hx (History), Rx (Prescription), etc.
# - Slash notations: c/o (complains of), s/p (status post)
ABBR_PATTERN = re.compile(r'\b[A-Z]{2,5}\b|\b(?:Pt|Hx|Rx|Dx|Tx|Sx|c/o|w/o|s/p|h/o)\b', re.IGNORECASE)

def find_abbreviations(text: str):
    """
    Find candidate abbreviations (all-caps tokens length 2-5).
    Returns list of unique tokens preserving order.
    """
    matches = ABBR_PATTERN.findall(text)
    seen = set()
    ordered = []
    for m in matches:
        if m not in seen:
            ordered.append(m)
            seen.add(m)
    return ordered

def highlight_expansions(text: str, expansions: dict):
    """
    Returns HTML with abbreviations replaced by annotated spans.
    expansions: {abbr: (chosen_expansion, confidence)}
    """
    out = text
    for abbr, (exp, conf) in expansions.items():
        # replace whole word only (case-sensitive)
        repl = f'<span title="Confidence: {conf:.2f}">{abbr} → <strong>{exp}</strong></span>'
        out = re.sub(rf'\b{re.escape(abbr)}\b', repl, out)
    return out
