# Theory — published kernel (`coherence_pump.py`)

Honesty of the file is the feature. This page describes the running stepper.
The v1.7.3 quaternion / wildcard / horocycle story is archived at
`archive/v1.7.3-broken/theory.md` and does not apply here.

## Current state

Thin kernel on `main`. Three clocks in LIVE, not three quaternion layers.
`v1.7.3` is in `archive/`.

## What integrates

One `solve_ivp` call. State `y` is length **N=56** (thesis DEFERRED) or **N+3**
(thesis LIVE). The first N entries are an energy sheet `E`. LIVE appends three
containing clocks `θ`.

The gate is **not** in `y`. It is a closure (`HysteresisGate`) on raw `mean(E)`:

- open when `mean(E) ≥ 0.55`
- close when `mean(E) ≤ 0.42`

Pack / receipt run after the integration. They are readout, not a second steep.
`--confirm` is a second `solve_ivp` on frozen `(y0, graph, faces)`. CONFIRMED
is a restep, not a face.

## Faces that may enter Ė

| Face | Role | Who feels it |
|---|---|---|
| ness | restore toward `E_STAR`, damp outliers | all nodes except load |
| seed | restore toward `E_CORE` | seed mask (default last 12) |
| load | leak `-κ_L E` | load mask (default first 4) |
| holonomy | `κ_H (K E) sin(θ_mid)`, multiplied by gate | LIVE only |

`K` is the skew part of the adjacency (default: cycle). Participation / coupling
is readout of `||K E|| / ||E||`. It is not a face in Ė.

`flow` is gone. There is no graph-current ODE.

## Theses

- **DEFERRED** — integrate `E` only. Holonomy is a sink. FACE_BUNDLE prints `UNPAIRED`.
- **LIVE** — integrate `E` and `θ`. Holonomy may enter Ė when the gate is on.
  FACE_BUNDLE prints `LOAD-HOLONOMY`.

FACE_BUNDLE is a label, not a nest test. `PAIR` is an alias for one cycle.
`pump_live` is `LIVE and load_final > 0.15`. Soft flag.
`R_event` stays DIRTY. `R_event_gate` may be NATIVE.

## Default graph

Cycle of 56 nodes. Load on `0:4`. Seed on `44:55`. Street names are an external
legend, not in the kernel.

## What this is not

Not a consciousness engine, trading signal, healing protocol, cosmological
simulator, or music release. Those stacks stay separate.
