"""parallel_reader.py — pack-side only.

Loads a validated mbcad.receipt.v0 dict and one greybin artifact.
Emits a side report. Shares no state with the stepper.
No import path to any face function or to solve_ivp.
"""

from typing import Dict, Any

# Mock greybin artifact (Mnetv1-style mesh stats).
# In a real reader this would be loaded from a file or another process.
MOCK_MNETV1 = {
    "chi": 2,
    "P": 12,
    "levels": "L0–L5",
    "note": "χ=2 held; no shared adjacency with energy sheet",
}

def parallel_read(receipt: Dict[str, Any], greybin: Dict[str, Any] = None) -> Dict[str, Any]:
    """Juxtapose a validated receipt with a greybin artifact. No merge."""
    if greybin is None:
        greybin = MOCK_MNETV1
    report = {
        "schema": "mbcad.receipt.v0",
        "pack_side": True,
        "receipt_summary": {
            "thesis": receipt.get("thesis"),
            "y_shape": receipt.get("y_shape"),
            "SINK": receipt.get("SINK"),
            "load_final": receipt.get("load_final"),
            "gate_frac_on": receipt.get("gate_frac_on"),
        },
        "greybin_summary": greybin,
        "juxtaposition": (
            f"receipt load_final={receipt.get('load_final')}; "
            f"greybin χ={greybin.get('chi')} held across {greybin.get('levels')}; "
            "no shared adjacency"
        ),
    }
    return report

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
    }
    report = parallel_read(example)
    print(report)
