"""parallel_reader.py — pack-side only.

Loads a validated mbcad.receipt.v0 dict and one greybin artifact.
Emits a side report. Shares no state with the stepper.
No import path to any face function or to solve_ivp.
The mock greybin is explicitly a stub, not a measured receipt.
"""

from typing import Dict, Any

# Explicit stub. Not a measured Mnetv1 receipt.
STUB_GREYBIN = {
    "source": "STUB",
    "chi": 2,
    "P": 12,
    "levels": "L0–L5",
    "note": "stub only; no shared adjacency with energy sheet",
}

def parallel_read(receipt: Dict[str, Any], greybin: Dict[str, Any] = None) -> Dict[str, Any]:
    """Juxtapose a validated receipt with a greybin artifact. No merge."""
    if greybin is None:
        greybin = STUB_GREYBIN
    report = {
        "schema": "pack-side.report.v0",
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
            f"greybin source={greybin.get('source')} χ={greybin.get('chi')} "
            f"across {greybin.get('levels')}; no shared adjacency"
        ),
    }
    return report

if __name__ == "__main__":
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
