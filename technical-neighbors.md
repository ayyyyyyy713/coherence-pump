# Technical neighbors (pack-side, below neighbor bar)

Moved from neighbors.md by the 2026-11-23 hygiene pass. Original numbers kept for reference. Commentary only. Not productions in the auditor. Do not write \(\dot{E}\). Do not become faces. Schema remains `mbcad.receipt.v0`.

## 92. Relaxation critical dynamics residual of strong-to-weak spontaneous symmetry breaking

**Source:** Jiaqiang Li, Xianquan Yan, Han-Ze Li, Shuai Yin, Shuo Liu, “Relaxation Critical Dynamics of Strong-to-Weak Spontaneous Symmetry Breaking.” arXiv:2611.20581, quant-ph / cond-mat.stat-mech / cond-mat.str-el. https://arxiv.org/abs/2611.20581

**Loop:** Strong-to-weak SSB residual → critical relaxation residual under dynamical scaling → residual packing of the order-parameter residual that remains after the transition.

**mbcad reading:** Residual-control packing of a symmetry-breaking residual. The residual that remains after the critical relaxation is the weak-SSB residual that is re-checked against the strong residual. No shared adjacency with the energy-sheet faces and no term that writes \(\dot{E}\).

**Status:** residual-control / packing-observation neighbor (critical dynamics of SSB). Not a production in the auditor. Does not write \(\dot{E}\). Does not become a face. Schema remains `mbcad.receipt.v0`.

## 107. Codon-torus duplex residual packing

**Source:** Dr-Logvinovich/codon-torus-syntax. Double-stranded codon torus \(\mathbb{T}_4^3 = (\mathbb{Z}/4\mathbb{Z})^3\); duplex fibration; zero-RNG analytic residual decompositions of codon mutual information across 100 RefSeq genomes. https://github.com/Dr-Logvinovich/codon-torus-syntax

**Loop:** 64 codons → cut by reverse-complement isometry and duplex fibration → residual: 56 duplex channels + 8 doublets → closed by exact analytic residual decompositions (antisense dominance 74–88 %, isochore-free screen memory in 100/100 genomes, Klein \(V_4\) quadrant residual).

**mbcad reading:** Pack-side example of geometric residual packing. The duplex residual packs the codon space under a fixed-point-free isometry. Exact analytic residuals are certified to \(<10^{-15}\). No shared adjacency with the energy-sheet faces and no term that writes \(\dot{E}\). Adjacent to geometric-packing and residual-control neighbors.

**Status:** geometric packing / residual-control neighbor (codon-torus duplex). Not a production in the auditor. Does not write \(\dot{E}\). Does not become a face. Schema remains `mbcad.receipt.v0`.

## 110. Zed dependency-graph residual packing

**Source:** Luke Hutchison, Zed (zedlanguage/zed). Reactive dataflow programming language in which a program is a dependency graph of once-defined values. Compiler handles scheduling, parallelism, memory, incremental recomputation, and static rejection of failure classes. https://github.com/zedlanguage/zed

**Loop:** Source definitions → cut by dependency graph → residual: only affected residuals recompute; failure, units, and cost residuals are statically gated → closed by bit-identical parallel results and first-class failure propagation.

**mbcad reading:** Packing observation of dependency-graph residual. Unused work is cut; participation constraints are enforced at compile time. No shared adjacency with the energy-sheet faces and no term that writes \(\dot{E}\). Overlay readings remain cut-from. Adjacent to language-relay and packing-observation neighbors.

**Status:** linguistic / packing-observation neighbor (dependency-graph residual). Not a production in the auditor. Does not write \(\dot{E}\). Does not become a face. Schema remains `mbcad.receipt.v0`.
