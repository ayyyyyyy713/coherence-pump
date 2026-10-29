"""pack_side_auditor.py — pack-side greybin integration.

All methods stay outside the stepper.
No greybin term enters Ė.
No new face.
This file has no import path to any face function or to solve_ivp.
Decorated output does not reuse the schema id mbcad.receipt.v0.
"""

from typing import Dict, Tuple, List, Any

# Vocabulary overlay — comment only. Never imported by the kernel.
VOCAB_OVERLAY = {
    "closure": "y_shape / SINK emptiness (commentary)",
    "defect": "non-empty SINK (commentary)",
    "topological reduction": "holonomy band when LIVE (commentary)",
    "coherence occupancy": "side-quest note only",
}

def validate_receipt_v0(receipt: Dict[str, Any]) -> Tuple[bool, str]:
    """Pure validator against the keys that are actually in mbcad.receipt.v0."""
    required = {"thesis", "y_shape", "SINK", "R_event"}
    missing = required - set(receipt.keys())
    if missing:
        return False, f"missing keys: {sorted(missing)}"
    if receipt.get("R_event") != "DIRTY":
        return False, "R_event must be DIRTY"
    return True, "ok"

def commentary_seed_forced_closure(receipt: Dict[str, Any]) -> List[str]:
    """Commentary token only. Does not claim the run measured a closure."""
    if receipt.get("thesis") == "LIVE" and not receipt.get("SINK"):
        return ["commentary:seed-forced-closure"]
    return []

def commentary_return_exceeds_perturbation(receipt: Dict[str, Any]) -> List[str]:
    """Commentary token only."""
    load = receipt.get("load_final", 0.0)
    contain = receipt.get("contain_E_end", 0.0)
    gate = receipt.get("gate_frac_on", 1.0)
    if load > contain and gate < 1.0:
        return ["commentary:return-exceeds-perturbation"]
    return []

def commentary_irreducible_under_current_sheet(receipt: Dict[str, Any]) -> List[str]:
    """Commentary token only."""
    if receipt.get("thesis") == "DEFERRED" and receipt.get("holonomy_band") == "DEAD":
        return ["commentary:irreducible-under-current-sheet"]
    return []

def check_greybin_consistency(receipt: Dict[str, Any]) -> Tuple[bool, str]:
    """Validator extension. Boolean only. Does not demand keys absent from v0."""
    return validate_receipt_v0(receipt)

def audit(receipt: Dict[str, Any]) -> Dict[str, Any]:
    """Pack-side auditor.
    Validates against actual v0 keys.
    Emits commentary tokens only.
    Decorated object does not claim schema mbcad.receipt.v0.
    """
    ok, reason = check_greybin_consistency(receipt)
    if not ok:
        return {"status": "REFUSAL", "reason": reason, "schema": "mbcad.receipt.v0"}
    tokens: List[str] = []
    tokens += commentary_seed_forced_closure(receipt)
    tokens += commentary_return_exceeds_perturbation(receipt)
    tokens += commentary_irreducible_under_current_sheet(receipt)
    decorated = dict(receipt)
    decorated["named_tokens"] = tokens
    decorated["pack_side"] = True
    decorated["schema"] = "pack-side.decorated.v0"  # not mbcad.receipt.v0
    return decorated

if __name__ == "__main__":
    # Real colder LIVE receipt shape (no injected keys)
    example = {
        "thesis": "LIVE",
        "y_shape": 59,
        "SINK": [],
        "R_event": "DIRTY",
        "load_final": 0.053,
        "contain_E_end": 1.021,
        "gate_frac_on": 0.96,
        "holonomy_band": "DEAD",
    }
    result = audit(example)
    print(result)
