# Mnet residual note (pack-side only)

Pure face-refinement residual from the Mnet / Mnetv1 Goldberg kernel.

Input: a Goldberg face.  
Output: refined face + invariant check (P=12, χ=2).

The residual is the invariant suite. It is published as a standalone receipt so a pack-side auditor can read the topology constraint without importing the mesh, the Unity port, or any adjacency matrix.

No term from this residual enters \(\dot{E}\). Schema remains `mbcad.receipt.v0`.
