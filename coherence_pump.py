#!/usr/bin/env python3
"""coherence_pump.py — published thin kernel.

N | N+3 energy sheet. One solve_ivp. Gate in a closure. Pack is readout.
Not a consciousness engine. Honesty of the file is the feature.
"""
from __future__ import annotations

import numpy as np
from scipy.integrate import solve_ivp

N = 56
N_LOAD = 4
N_SEED = 12
PHI = (1.0 + np.sqrt(5.0)) / 2.0
OMEGA0 = 2.0 * np.pi / 24.0

KAPPA_N = 0.04
GAMMA_N = 0.08
E_STAR = 1.0
KAPPA_S = 0.03
E_CORE = 1.05
KAPPA_H = 0.18
KAPPA_TH = 0.10
KAPPA_L = 0.06

ALPHA = 0.1
SNAP = 0.9
GATE_ON = 0.55
GATE_OFF = 0.42
RTOL = 1e-5
ATOL = 1e-6
T_END = 300.0
N_EVAL = 800
METHOD = "RK45"
LIVE_WEAK = 1e-4
EPS = 1e-12


def _as_N(x):
    x = np.asarray(x, dtype=float)
    if x.ndim == 0 or x.size == 1:
        return np.full(N, float(x))
    if x.size != N:
        raise ValueError(f"face length {x.size} != N={N}")
    return x


def _adj(graph):
    if graph is None:
        return None
    if isinstance(graph, dict):
        return None if graph.get("A") is None else np.asarray(graph["A"], dtype=float)
    return np.asarray(graph, dtype=float)


def _seed_mask(graph):
    if isinstance(graph, dict) and "seed_mask" in graph:
        s = np.asarray(graph["seed_mask"], dtype=float)
        if s.size != N:
            raise ValueError("seed_mask length != N")
        return s
    s = np.zeros(N, dtype=float)
    s[N - N_SEED :] = 1.0
    return s


def _load_mask(graph):
    if isinstance(graph, dict) and "load_mask" in graph:
        s = np.asarray(graph["load_mask"], dtype=float)
        if s.size != N:
            raise ValueError("load_mask length != N")
        return s
    s = np.zeros(N, dtype=float)
    s[:N_LOAD] = 1.0
    return s


def _K(graph):
    A = _adj(graph)
    if A is not None and A.shape == (N, N):
        return 0.5 * (A - A.T)
    K = np.zeros((N, N), dtype=float)
    for i in range(N):
        j = (i + 1) % N
        K[i, j] = 0.5
        K[j, i] = -0.5
    return K


def participation(E, graph):
    E = np.asarray(E, dtype=float)
    Ke = _K(graph) @ E
    return float(np.linalg.norm(Ke) / (np.linalg.norm(E) + EPS))


def face_ness(E, graph):
    E = np.asarray(E, dtype=float)
    load = _load_mask(graph)
    raw = KAPPA_N * (E_STAR - E) - GAMMA_N * (E - E.mean()) ** 2 * E
    return raw * (1.0 - load)


def face_seed(E, graph):
    E = np.asarray(E, dtype=float)
    return KAPPA_S * _seed_mask(graph) * (E_CORE - E)


def face_holonomy(E, theta, graph):
    E = np.asarray(E, dtype=float)
    if theta is None:
        return np.zeros(N)
    th_mid = float(np.asarray(theta, dtype=float)[1])
    curl = _K(graph) @ E
    return KAPPA_H * curl * np.sin(th_mid)


def face_load(E, graph):
    E = np.asarray(E, dtype=float)
    return -KAPPA_L * _load_mask(graph) * E


def face_fn(E, theta, t, graph, gate):
    out = {
        "ness": face_ness(E, graph),
        "seed": face_seed(E, graph),
        "load": face_load(E, graph),
        "coupling": participation(E, graph),
    }
    if theta is None:
        return out
    out["holonomy"] = face_holonomy(E, theta, graph)
    return out


def dE_dt(E, theta, t, graph, gate, faces):
    E = np.asarray(E, dtype=float)
    if E.size != N:
        raise ValueError(f"E length {E.size} != N={N}")
    dE = np.zeros(N, dtype=float)
    g = float(gate)
    if "ness" in faces:
        dE = dE + _as_N(faces["ness"])
    if "seed" in faces:
        dE = dE + _as_N(faces["seed"])
    if "load" in faces:
        dE = dE + _as_N(faces["load"])
    if "holonomy" in faces:
        dE = dE + g * _as_N(faces["holonomy"])
    return dE


def dtheta_dt(E, theta, t, graph, gate):
    if theta is None:
        return None
    theta = np.asarray(theta, dtype=float)
    if theta.size != 3:
        raise ValueError(f"theta length {theta.size} != 3")
    E = np.asarray(E, dtype=float)
    seed = _seed_mask(graph)
    ebar = float(np.mean(E))
    e_contain = float(np.sum(seed * E) / (np.sum(seed) + EPS))
    w = OMEGA0 * np.array([1.0, 1.0 / PHI, 1.0 / PHI ** 2])
    dth = np.array([w[0] * ebar, w[1] * e_contain, w[2] * e_contain], dtype=float)
    dth[1] = dth[1] + KAPPA_TH * np.sin(theta[0] - theta[1])
    dth[2] = dth[2] + KAPPA_TH * np.sin(theta[1] - theta[2])
    return dth


def faces_in_dE_for(thesis):
    if thesis == "LIVE":
        return {"ness", "holonomy", "seed", "load"}
    return {"ness", "seed", "load"}


def slice_y(y):
    y = np.asarray(y, dtype=float)
    E = y[:N]
    if y.size == N:
        return {"E": E, "theta": None, "thesis": "DEFERRED"}
    if y.size == N + 3:
        return {"E": E, "theta": y[N : N + 3], "thesis": "LIVE"}
    raise ValueError(f"illegal y size {y.size}; stamped sizes are {N} or {N+3}")


class HysteresisGate:
    def __init__(self, start_open=False):
        self.open = bool(start_open)

    def __call__(self, E, theta, t, graph):
        e = float(np.mean(E))
        if e >= GATE_ON:
            self.open = True
        elif e <= GATE_OFF:
            self.open = False
        return 1.0 if self.open else 0.0


def combined_dynamics(t, y, graph, gate_fn, face_fn_):
    s = slice_y(y)
    g = float(gate_fn(s["E"], s["theta"], t, graph))
    faces = face_fn_(s["E"], s["theta"], t, graph, g)
    dE = dE_dt(s["E"], s["theta"], t, graph, g, faces)
    if s["theta"] is None:
        return np.asarray(dE, dtype=float)
    dth = dtheta_dt(s["E"], s["theta"], t, graph, g)
    if dth is None:
        dth = np.zeros(3)
    return np.concatenate([np.asarray(dE, dtype=float), np.asarray(dth, dtype=float)])


def ema_series(x, alpha=ALPHA):
    out = np.empty_like(x, dtype=float)
    out[0] = x[0]
    a = float(alpha)
    for k in range(1, x.size):
        out[k] = (1.0 - a) * out[k - 1] + a * x[k]
    return out


def first_upcross(t, y, level=SNAP):
    for k in range(1, y.size):
        if y[k - 1] < level <= y[k]:
            return float(t[k])
    return None


def spread(x):
    x = np.asarray(x, dtype=float)
    return float(np.max(x) - np.min(x))


def unpack_sol(sol):
    Y = np.asarray(sol.y)
    if Y.shape[0] not in (N, N + 3):
        raise ValueError(f"illegal y size {Y.shape[0]}")
    E = Y[:N, :]
    if Y.shape[0] == N:
        return E, None, "DEFERRED"
    return E, Y[N : N + 3, :], "LIVE"


def pack(sol, graph, gate_fn, face_fn_, faces_in_dE, claim_snap_is_event=False):
    t = np.asarray(sol.t, dtype=float)
    E, theta, thesis = unpack_sol(sol)
    load = _load_mask(graph)
    seed = _seed_mask(graph)

    global_E = E.mean(axis=0)
    ema = ema_series(global_E)
    snap_time = first_upcross(t, ema, SNAP)

    ness = np.zeros_like(t)
    hol_mean = np.zeros_like(t)
    hol_rms = np.zeros_like(t)
    seed_f = np.zeros_like(t)
    gate = np.zeros_like(t)
    coupling = np.zeros_like(t)
    ipr = np.zeros_like(t)
    load_E = np.zeros_like(t)
    contain_E = np.zeros_like(t)

    for k in range(t.size):
        th = None if theta is None else theta[:, k]
        g = float(gate_fn(E[:, k], th, t[k], graph))
        gate[k] = g
        f = face_fn_(E[:, k], th, t[k], graph, g)
        ness[k] = float(np.mean(np.asarray(f.get("ness", 0.0))))
        hol_vec = np.asarray(f.get("holonomy", np.zeros(N)), dtype=float)
        hol_mean[k] = float(np.mean(hol_vec))
        hol_rms[k] = float(np.sqrt(np.mean(hol_vec ** 2)))
        seed_f[k] = float(np.mean(np.asarray(f.get("seed", 0.0))))
        coupling[k] = float(f.get("coupling", np.nan))
        e2 = E[:, k] ** 2
        s = e2.sum()
        ipr[k] = float((s * s) / (np.dot(e2, e2) + 1e-30)) / N
        load_E[k] = float(np.sum(load * E[:, k]) / (np.sum(load) + EPS))
        contain_E[k] = float(np.sum(seed * E[:, k]) / (np.sum(seed) + EPS))

    sink = sorted({"ness", "holonomy", "seed", "load"} - set(faces_in_dE))

    conv = pol = None
    rates = None
    if thesis == "LIVE":
        th_u = np.unwrap(theta, axis=1)
        rates = np.gradient(th_u, t, axis=1)
        conv = np.array([spread(th_u[:, k]) for k in range(t.size)])
        pol = np.array([spread(rates[:, k]) for k in range(t.size)])

    load_floor = float(np.min(load_E))
    load_final = float(load_E[-1])
    pump_live = bool(thesis == "LIVE" and load_final > 0.15)

    residuals = {
        "R_event": 1.0 if (snap_time is not None and claim_snap_is_event) else 0.0,
        "R_event_dirty": True,
        "R_circ": float(len(sink)),
        "thesis": thesis,
        "SINK": sink,
        "FACE_BUNDLE": "LOAD-HOLONOMY" if thesis == "LIVE" else "UNPAIRED",
        "PAIR": "LOAD-HOLONOMY" if thesis == "LIVE" else "UNPAIRED",
        "pump_live": pump_live,
    }

    return {
        "t": t,
        "global_E": global_E,
        "ema": ema,
        "snap_time": snap_time,
        "ness_force": ness,
        "holonomy_force": hol_mean,
        "holonomy_rms": hol_rms,
        "seed_force": seed_f,
        "gate_strength": gate,
        "coupling_density": coupling,
        "mean_ipr": ipr,
        "load_E": load_E,
        "contain_E": contain_E,
        "load_floor": load_floor,
        "load_final": load_final,
        "theta": theta,
        "rates": rates,
        "conv": conv,
        "pol": pol,
        "residuals": residuals,
        "thesis": thesis,
    }


def band(max_abs, absent=False):
    if absent:
        return "ABSENT"
    if max_abs <= RTOL:
        return "DEAD"
    if max_abs <= LIVE_WEAK:
        return "WEAK"
    return "LIVE"


def default_graph():
    A = np.zeros((N, N), dtype=float)
    for i in range(N):
        A[i, (i + 1) % N] = 1.0
    seed_mask = np.zeros(N, dtype=float)
    seed_mask[N - N_SEED :] = 1.0
    load_mask = np.zeros(N, dtype=float)
    load_mask[:N_LOAD] = 1.0
    return {"A": A, "seed_mask": seed_mask, "load_mask": load_mask}


def y0_cold(rng=None):
    rng = np.random.default_rng(56 if rng is None else rng)
    E = rng.uniform(0.40, 0.70, size=N)
    theta = np.array([0.20, -0.10, 0.05], dtype=float)
    return np.concatenate([E, theta])


def y0_colder(rng=None):
    rng = np.random.default_rng(56 if rng is None else rng)
    E = rng.uniform(0.18, 0.37, size=N)
    theta = np.array([0.20, -0.10, 0.05], dtype=float)
    return np.concatenate([E, theta])


def y0_hot(rng=None):
    rng = np.random.default_rng(56 if rng is None else rng)
    E = rng.uniform(0.82, 0.98, size=N)
    theta = np.array([0.20, -0.10, 0.05], dtype=float)
    return np.concatenate([E, theta])


def _gate_upcross_event(t, y):
    return float(np.mean(np.asarray(y, dtype=float)[:N]) - GATE_ON)


_gate_upcross_event.direction = 1.0
_gate_upcross_event.terminal = False


def run(y0, graph=None, start_open=None):
    y0 = np.asarray(y0, dtype=float)
    if y0.size not in (N, N + 3):
        raise ValueError(f"illegal y size {y0.size}")
    thesis = "LIVE" if y0.size == N + 3 else "DEFERRED"
    graph = default_graph() if graph is None else graph

    ebar0 = float(np.mean(y0[:N]))
    if start_open is None:
        start_open = ebar0 >= GATE_ON
    gate_fn = HysteresisGate(start_open=start_open)

    sol = solve_ivp(
        fun=lambda t, y: combined_dynamics(t, y, graph, gate_fn, face_fn),
        t_span=(0.0, T_END),
        y0=y0,
        method=METHOD,
        t_eval=np.linspace(0.0, T_END, N_EVAL),
        rtol=RTOL,
        atol=ATOL,
        dense_output=False,
        events=_gate_upcross_event,
    )
    if not sol.success:
        raise RuntimeError(sol.message)

    pack_gate = HysteresisGate(start_open=start_open)
    result = pack(
        sol,
        graph,
        pack_gate,
        face_fn,
        faces_in_dE_for(thesis),
        claim_snap_is_event=False,
    )
    result["success"] = bool(sol.success)
    result["nfev"] = int(sol.nfev)
    result["final_global_E"] = float(result["global_E"][-1])
    result["final_ema"] = float(result["ema"][-1])
    result["ema_max"] = float(result["ema"].max())
    result["gate_frac_on"] = float(np.mean(result["gate_strength"] >= 0.5))
    result["y0_mean"] = ebar0
    ev = getattr(sol, "t_events", None)
    gate_events = np.asarray(ev[0], dtype=float) if ev and len(ev) and ev[0] is not None else np.array([])
    result["gate_upcross_times"] = gate_events
    result["R_event_gate"] = "NATIVE" if gate_events.size else "ABSENT"
    result["coupling_mean"] = float(np.mean(result["coupling_density"]))
    result["coupling_max"] = float(np.max(result["coupling_density"]))
    result["hol_rms_max"] = float(np.max(result["holonomy_rms"]))
    return result


def receipt(result):
    th = result["thesis"]
    r = result["residuals"]
    ness_m = float(np.max(np.abs(result["ness_force"])))
    seed_m = float(np.max(np.abs(result["seed_force"])))
    hol_mean_m = float(np.max(np.abs(result["holonomy_force"])))
    hol_rms_m = float(np.max(result["holonomy_rms"]))
    coup_m = float(np.max(result["coupling_density"]))
    if result["rates"] is None:
        thd_m, thd_b = 0.0, "ABSENT"
    else:
        thd_m = float(np.max(np.abs(result["rates"])))
        thd_b = band(thd_m)
    lines = [
        f"thesis:        {th}",
        f"snap_time:     {result['snap_time']}",
        f"SINK:          {r['SINK']}",
        f"FACE_BUNDLE:   {r['FACE_BUNDLE']}",
        f"PAIR:          {r['PAIR']}   (alias of FACE_BUNDLE; not a nest test)",
        f"pump_live:     {r['pump_live']}",
        f"ness band:     {band(ness_m):<6}  max={ness_m:.2e}",
        f"seed band:     {band(seed_m):<6}  max={seed_m:.2e}",
        f"holonomy mean: {band(hol_mean_m, absent=('holonomy' in r['SINK'])):<6}  max={hol_mean_m:.2e}   (structurally ~0)",
        f"holonomy rms:  {band(hol_rms_m, absent=('holonomy' in r['SINK'])):<6}  max={hol_rms_m:.2e}",
        f"coupling:      {band(coup_m):<6}  max={coup_m:.2e}  mean={result['coupling_mean']:.2e}",
        f"theta_dot:     {thd_b:<6}  max={thd_m:.2e}",
        f"load_final:    {result['load_final']:.3f}   floor={result['load_floor']:.3f}",
        f"contain_E_end: {result['contain_E'][-1]:.3f}",
        f"R_event        DIRTY   (snap is a candidate)",
        f"R_event_gate   {result.get('R_event_gate', 'ABSENT')}",
        f"gate_upcross   {np.asarray(result.get('gate_upcross_times', [])).tolist()}",
        f"R_circ         {r['R_circ']}",
        "",
        f"success:        {result['success']}",
        f"nfev:           {result['nfev']}",
        f"final_global_E: {result['final_global_E']:.3f}",
        f"final_ema:      {result['final_ema']:.3f}",
        f"ema_max:        {result['ema_max']:.3f}",
        f"gate_frac_on:   {result['gate_frac_on']:.2f}",
        f"y0_mean:        {result['y0_mean']:.3f}",
    ]
    return "\n".join(lines)



def _scalar_keys(result):
    gates = np.asarray(result.get("gate_upcross_times", []), dtype=float)
    return {
        "thesis": result["thesis"],
        "FACE_BUNDLE": result["residuals"]["FACE_BUNDLE"],
        "SINK": tuple(result["residuals"]["SINK"]),
        "pump_live": bool(result["residuals"]["pump_live"]),
        "load_final": float(result["load_final"]),
        "contain_E_end": float(result["contain_E"][-1]),
        "gate_frac_on": float(result["gate_frac_on"]),
        "final_global_E": float(result["final_global_E"]),
        "y0_mean": float(result["y0_mean"]),
        "R_event_gate": result.get("R_event_gate", "ABSENT"),
        "gate_upcross0": float(gates[0]) if gates.size else None,
        "nfev": int(result["nfev"]),
    }


def confirm(y0, graph=None):
    """Second solve_ivp on frozen (y0, graph, faces). Pack stays readout."""
    y0 = np.asarray(y0, dtype=float).copy()
    graph = default_graph() if graph is None else graph
    a = run(y0, graph=graph)
    b = run(y0, graph=graph)
    ka, kb = _scalar_keys(a), _scalar_keys(b)
    drift = []
    for k in ka:
        va, vb = ka[k], kb[k]
        if isinstance(va, float) and va is not None and vb is not None:
            if abs(va - vb) > 1e-9:
                drift.append(f"{k}: {va} vs {vb}")
        elif va != vb:
            drift.append(f"{k}: {va} vs {vb}")
    status = "DRIFT" if drift else "CONFIRMED"
    lines = [
        f"confirm:       {status}",
        f"frozen y_shape: {int(y0.size)}",
        f"faces:         {sorted(faces_in_dE_for(a['thesis']))}",
        f"series_a nfev: {ka['nfev']}",
        f"series_b nfev: {kb['nfev']}",
        f"load_final:    {ka['load_final']:.6f} / {kb['load_final']:.6f}",
        f"contain_E_end: {ka['contain_E_end']:.6f} / {kb['contain_E_end']:.6f}",
        f"gate_frac_on:  {ka['gate_frac_on']:.4f} / {kb['gate_frac_on']:.4f}",
        f"R_event_gate:  {ka['R_event_gate']} / {kb['R_event_gate']}",
        f"gate_upcross:  {ka['gate_upcross0']} / {kb['gate_upcross0']}",
    ]
    if drift:
        lines.append("drift:         " + " | ".join(drift))
    return status, "\n".join(lines), a, b


def detroit_receipt(result):
    r = result["residuals"]
    return "\n".join(
        [
            f"thesis:        {result['thesis']}",
            f"SINK:          {r['SINK']}",
            f"pump_live:     {r['pump_live']}",
            f"load_final:    {result['load_final']:.3f}",
            f"contain_E_end: {result['contain_E'][-1]:.3f}",
            f"gate_frac_on:  {result['gate_frac_on']:.2f}",
        ]
    )


if __name__ == "__main__":
    import argparse
    import sys

    p = argparse.ArgumentParser()
    p.add_argument("--deferred", action="store_true")
    p.add_argument("--no-plot", action="store_true")
    p.add_argument("--detroit-receipt", action="store_true")
    p.add_argument("--ic", choices=("cold", "colder", "hot"), default="cold")
    p.add_argument("--confirm", action="store_true")
    args = p.parse_args()

    if not args.no_plot:
        print("plot: ABSENT — published kernel has no plotter (pass --no-plot to silence)", file=sys.stderr)

    if args.ic == "colder":
        y0 = y0_colder()
    elif args.ic == "hot":
        y0 = y0_hot()
    else:
        y0 = y0_cold()
    if args.deferred:
        y0 = y0[:N]
    if args.confirm:
        status, text, _, _ = confirm(y0)
        print(text)
        sys.exit(0 if status == "CONFIRMED" else 2)
    result = run(y0)
    print(detroit_receipt(result) if args.detroit_receipt else receipt(result))
    sys.exit(0)

