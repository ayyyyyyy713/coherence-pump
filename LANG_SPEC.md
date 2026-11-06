# LANG_SPEC.md

Pack-side linguistic overlay only.  
These three keys annotate existing receipt fields.  
No term here is a face. No term writes \(\dot{E}\).  
Schema on the kernel receipt remains `mbcad.receipt.v0`.

## Frozen keys

### 1. Cut criterion
What is separated from the prior substrate.  
A semantic patch (`.patch` / `.sem`) is accepted only when the desugaring closes under the load of a target face already present in the receipt (`ness`, `seed`, `load`, or gated `holonomy` when `thesis=LIVE`).  
If the cut does not close, the step returns \(\emptyset\) and the patch is marked DIRTY.  
No new face is created by the cut.

### 2. Failure mode
What returns \(\emptyset\).  
The desugaring parser is a participation gate.  
It may rewrite only inside the stable manifold defined by a validated `mbcad.receipt.v0` receipt.  
Outside that manifold (participation density below the locked gate, or a claimed face not in `{ness, seed, load, holonomy}`), the step fails closed and returns \(\emptyset\).  
The prior receipt remains the only legal state.

### 3. Provenance stamp
How †/‡ is carried without restep.  
Provenance is carried by `patch_id` and the operator list on the decorated receipt.  
A successful cut that closes under an existing face may be stamped † (measured) or ‡ (commentary).  
The stamp does not restep the base engine and does not alter any key in `mbcad.receipt.v0`.  
A diagnostic that cannot be turned into a closing patch leaves the stamp unmarked.

## Status
Anything beyond these three keys remains neighbor-only.  
The linguistic layer is a packing extension, not a rewrite of the origin, language, theory, or goals already locked.  
No `--graph` or `--probe`. No second kernel.
