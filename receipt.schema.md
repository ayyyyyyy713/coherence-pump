# mbcad.receipt.v0

schema: mbcad.receipt.v0
file: coherence_pump.py
thesis: LIVE | DEFERRED
y_shape: N | N+3
FACE_BUNDLE: LOAD-HOLONOMY | UNPAIRED
  # Face list in this run. Not a nest test.
PAIR: alias of FACE_BUNDLE (kept one cycle for old printers).
R_pair: removed. Do not read a pairing score.
SINK: [faces withheld from dE]
R_event: DIRTY
  # snap/EMA upcross is a candidate. Never promote it.
R_event_gate: NATIVE | ABSENT
  # rising mean(E)-0.55 recorded by solve_ivp events=. Snap is not this.
bands: ness, seed, holonomy_mean, holonomy_rms, coupling, theta_dot
       ∈ {ABSENT, DEAD, WEAK, LIVE}
  # flow is not a face. Do not band it.
load_final / load_floor / contain_E_end / final_global_E / final_ema
gate_frac_on / y0_mean / nfev / success
pump_live: true|false
  # soft flag: LIVE and load_final > 0.15. Not competence.
Qstar: pack-only; no resteep
center: unmarked

detroit-receipt subset:
  load_final, contain_E_end, gate_frac_on, SINK, pump_live, thesis

Not a consciousness engine, trading signal, healing protocol,
or cosmological simulator. Honesty of the file is the feature.
