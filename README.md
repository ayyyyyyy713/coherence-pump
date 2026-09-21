# Coherence Pump

A single-stepper dynamical kernel with pack-as-readout.

`coherence_pump.py` integrates an N=56 energy field with one `solve_ivp` call. The gate lives in a closure, not in the state vector. After the run, `pack()` / `receipt()` print a frozen record. That record is not a second integration.

This is not a consciousness engine, trading signal, healing protocol, or cosmological simulator. Honesty of the file is the feature.

## What the kernel does

- State `y` is length **N** (DEFERRED) or **N+3** (LIVE).
- DEFERRED integrates the energy sheet only. LIVE adds three containing clocks.
- Faces that may enter `dE`: ness, seed, load. LIVE may also admit gated holonomy.
- Load is a sink. Ness is withheld on the load nodes.
- `R_event` stays **DIRTY**. A snap time is a candidate, not an event.
- `R_event_gate` is **NATIVE** or **ABSENT**. Rising `mean(E)-0.55` from `solve_ivp` events=. Snap is not this.
- `--ic colder` starts below the latch so the gate can rise.
- `--confirm` is a second `solve_ivp` on frozen `(y0, graph, faces)`. CONFIRMED is a restep, not a face.
- `pump_live` is a soft flag. Do not read it as “learned to pump.”
- `FACE_BUNDLE` is `LOAD-HOLONOMY` or `UNPAIRED`. `PAIR` is an alias. Not a nest test.

Same present energy readout can sit under two theses. LIVE and DEFERRED are different legal next moves, not two spellings of one story.

Receipt keys are frozen in [`receipt.schema.md`](receipt.schema.md) (`mbcad.receipt.v0`).

## Quick Start

```bash
git clone https://github.com/ayyyyyyy713/coherence-pump.git
cd coherence-pump
pip install -r requirements.txt
python coherence_pump.py --deferred --no-plot
python coherence_pump.py --no-plot
python coherence_pump.py --detroit-receipt --no-plot
python coherence_pump.py --ic colder --no-plot
python coherence_pump.py --ic colder --confirm --no-plot
