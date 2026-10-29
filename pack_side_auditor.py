"""pack_side_auditor.py — pack-side greybin integration.

All methods stay outside the stepper.
No greybin term enters Ė.
No new face.
Schema id remains mbcad.receipt.v0.
This file has no import path to any face function or to solve_ivp.
"""

from typing import Dict, Tuple, List, Any

# Vocabulary overlay — comment / README / language sketch only.
# Never imported by the kernel.
VOCAB_OVERLAY = {
    "closure": "y_shape / SINK emptiness",
    "defect": "non-empty SINK",
    "topological reduction": "holonomy band when LIVE",
    "coherence occupancy": "side-quest note only",
    "seed-forced-closure": "named token from Geometric SM production",
    "return-exceeds-perturbation": "named token from Self-Return / FVC production",
    "irreducible-under-current-sheet": "named token from ruliobiology production",
}

def validate_receipt_v0(receipt: Dict[str, Any]) -> Tuple[bool, str]:
    """Pure validator against mbcad.receipt.v0. Boolean only."""
    required = {"thesis", "y_shape", "SINK", "R_event"}
    missing = required - set(receipt.keys())
    if missing:
        return False, f"missing keys: {sorted(missing)}"
    if receipt.get("R_event") != "DIRTY":
        return False, "R_event must be DIRTY"
    return True, "ok"

def production_seed_forced_closure(receipt: Dict[str, Any]) -> List[str]:
    """Geometric SM closure → named token."""
    if receipt.get("thesis") == "LIVE" and not receipt.get("SINK"):
        return ["seed-forced-closure"]
    return []

def production_return_exceeds_perturbation(receipt: Dict[str, Any]) -> List[str]:
    """Self-Return / FVC → named token."""
    load = receipt.get("load_final", 0.0)
    contain = receipt.get("contain_E_end", 0.0)
    gate = receipt.get("gate_frac_on", 1.0)
    if load > contain and gate < 1.0:
        return ["return-exceeds-perturbation"]
    return []

def production_irreducible_under_current_sheet(receipt: Dict[str, Any]) -> List[str]:
    """Ruliobiology polyplexy → named token."""
    if receipt.get("thesis") == "DEFERRED" and receipt.get("holonomy_band") == "DEAD":
        return ["irreducible-under-current-sheet"]
    return []

def check_greybin_consistency(receipt: Dict[str, Any]) -> Tuple[bool, str]:
    """Validator extension. Boolean only. Does not modify receipt or stepper."""
    ok, reason = validate_receipt_v0(receipt)
    if not ok:
        return False, reason
    # Poole/Lean style example
    if receipt.get("R_event") == "DIRTY" and not receipt.get("events_passed", False):
        return False, "unpaired-event"
    # Higgs-Gauge lattice style example
    if receipt.get("gate_frac_on") == 1.0 and receipt.get("probe_requested", False):
        return False, "gate-never-dropped"
    return True, "ok"

def audit(receipt: Dict[str, Any]) -> Dict[str, Any]:
    """Pack-side auditor composition.
    Validates, applies named productions, emits decorated v0 or refusal.
    No import path to any face function or to solve_ivp.
    """
    ok, reason = check_greybin_consistency(receipt)
    if not ok:
        return {"status": "REFUSAL", "reason": reason, "schema": "mbcad.receipt.v0"}
    tokens: List[str] = []
    tokens += production_seed_forced_closure(receipt)
    tokens += production_return_exceeds_perturbation(receipt)
    tokens += production_irreducible_under_current_sheet(receipt)
    decorated = dict(receipt)
    decorated["named_tokens"] = tokens
    decorated["schema"] = "mbcad.receipt.v0"
    decorated["pack_side"] = True
    return decorated

if __name__ == "__main__":
    # Example cold receipt (no kernel call)
    example = {
        "thesis": "LIVE",
        "y_shape": 59,
        "SINK": [],
        "R_event": "DIRTY",
        "load_final": 0.053,
        "contain_E_end": 1.021,
        "gate_frac_on": 0.96,
        "holonomy_band": "DEAD",
        "events_passed": True,
        "probe_requested": False,
    }
    result = audit(example)
    print(result)
