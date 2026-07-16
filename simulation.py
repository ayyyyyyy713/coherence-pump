"""
Coherence Pump v1.7.3
=====================

A multi-scale dynamical system exploring convergence, polarization,
and recursive coherence through a three-layer quaternion graph flow model.

Core Components:
- 56-node base system with Mereon-style nesting and oscillatory layer
- L6b-style control layer for modulation and improvisation
- Three-scale quaternion-delta structure (Fine / Mid / Coarse)
- Explicit graph flow layer with directed cyclic currents
- Multiple higher-order behaviors:
    • Phase-gradient modulation
    • Emergent wildcard layer
    • Self-referential modulation
    • Coherence-gated polarization (bifurcation)
    • Horocycle-style averaging across scales
    • Recursive contraction toward attractor
    • Coherence locking at high density

Key Dynamics:
- Coupling density acts as a continuous gating variable
- Gate with hysteresis controls activation of higher-order mechanisms
- Convergence and polarization occur together as coherence increases
- Self-reference allows the system to influence its own trajectory

Usage:
    python simulation.py

Outputs:
    - v1.7.3_coherence_run.csv (main simulation data)
    - Can be visualized using animate.py

Author: Cole (with iterative development alongside Grok)
License: Apache 2.0
"""

import numpy as np
from scipy.integrate import solve_ivp
import pandas as pd
from numpy.linalg import eigimport numpy as np
from scipy.integrate import solve_ivp
import pandas as pd
from numpy.linalg import eig

# ====================== PARAMETERS ======================
N = 56
N_L6b = 10

beta_base = 0.05
C_mean = 0.85
D_mean = 1.15
w_mean = 1.0

# Layering & Coupling
USE_MEREON_NESTING = True
phi = (1 + np.sqrt(5)) / 2
np.random.seed(42)
layer = np.zeros(N, dtype=int)
layer[:30] = 0      # Outer
layer[30:44] = 1    # Focusing
layer[44:] = 2      # Inner
layer_coupling = np.array([1.0, 1/phi, 1/phi**2])

# Rhythmic & Persistence
USE_BREATH_RHYTHM = True
breath_frequency = 0.25
breath_amplitude = 0.65

USE_PERSISTENCE = True
persistence_rate = 0.02
persistence_decay = 0.005

# Dynamic Gating
USE_DYNAMIC_T = True
T_activation_threshold = 0.55
T_smoothing = 0.15
GATE_ACTIVATION_THRESHOLD = 0.55
GATE_DEACTIVATION_THRESHOLD = 0.42

# Advanced Mechanisms
USE_ENGINEERED_STRUCTURE = True
structure_stabilization = 0.4
USE_HYPERDIMENSIONAL_RELEASE = True
release_strength = 0.5
release_activation_bonus = 0.3

# L6b Layer
L6b_modulation_strength = 0.6
L6b_base_facilitation = 0.3
L6b_improvisation_factor = 0.25
L6b_burst_probability = 0.06
L6b_burst_strength = 0.7

# Quaternion Downsampling
DOWN_SAMPLE_FINE_TO_MID = 8
DOWN_SAMPLE_MID_TO_COARSE = 7

# Physical Parameters
T_compression = 24.0
omega0 = 2 * np.pi / T_compression
angle_factor = np.sin(np.deg2rad(51.84))
light_speed_scale = 1.0018

# EMA Settings
USE_EMA_COHERENCE = True
ema_alpha = 0.1
snap_threshold = 0.9

# ====================== GRAPH & INITIAL CONDITIONS ======================
np.random.seed(42)
adj_matrix = np.zeros((N, N))
for i in range(N):
    adj_matrix[i, (i+1)%N] = 1.0
    adj_matrix[i, (i-1)%N] = 1.0
for i in range(N):
    for j in range(N):
        if np.random.rand() < 0.12 and i != j:
            adj_matrix[i, j] = np.random.uniform(0.6, 1.4)

np.random.seed(123)
L6b_to_main_base = np.random.rand(N_L6b, N) * 0.8

# Initial state
E0 = np.random.uniform(0.7, 1.1, N)
x0 = np.random.uniform(-0.4, 0.4, N)
v0 = np.zeros(N)
P0 = 0.3
E_L6b0 = np.random.uniform(0.5, 1.0, N_L6b)
Q_fine0 = np.array([1.0, 0.0, 0.0, 0.0])
Q_mid0  = np.array([1.0, 0.0, 0.0, 0.0])
Q_coarse0 = np.array([1.0, 0.0, 0.0, 0.0])

y0 = np.concatenate([E0, x0, v0, [P0], E_L6b0, Q_fine0, Q_mid0, Q_coarse0])

# ====================== QUATERNION HELPERS ======================
def quat_mult(q1, q2):
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    return np.array([
        w1*w2 - x1*x2 - y1*y2 - z1*z2,
        w1*x2 + x1*w2 + y1*z2 - z1*y2,
        w1*y2 - x1*z2 + y1*w2 + z1*x2,
        w1*z2 + x1*y2 - y1*x2 + z1*w2
    ])

def quat_normalize(q):
    norm = np.linalg.norm(q)
    return q / norm if norm > 1e-12 else np.array([1.0, 0.0, 0.0, 0.0])

# ====================== MAIN DYNAMICS ======================
def combined_dynamics(t, y, adj_matrix, beta_base, C_mean, D_mean, w_mean,
                      omega0, angle_factor, light_speed_scale,
                      breath_frequency, breath_amplitude, USE_BREATH_RHYTHM,
                      layer, layer_coupling, USE_MEREON_NESTING,
                      USE_OFFLOADING, offloading_strength,
                      USE_PERSISTENCE, persistence_rate, persistence_decay,
                      USE_DYNAMIC_T, T_activation_threshold, T_smoothing,
                      USE_ENGINEERED_STRUCTURE, structure_stabilization,
                      USE_HYPERDIMENSIONAL_RELEASE, release_strength, release_activation_bonus,
                      N_L6b, L6b_modulation_strength, L6b_base_facilitation,
                      L6b_improvisation_factor, L6b_burst_probability, L6b_burst_strength, L6b_to_main_base,
                      GATE_ACTIVATION_THRESHOLD, GATE_DEACTIVATION_THRESHOLD,
                      DOWN_SAMPLE_FINE_TO_MID, DOWN_SAMPLE_MID_TO_COARSE):

    # === State unpacking ===
    E = y[:N]
    x = y[N:2*N]
    v = y[2*N:3*N]
    P = y[3*N] if USE_PERSISTENCE else 0.0
    E_L6b = y[3*N + 1 : 3*N + 1 + N_L6b]
    Q_fine = y[3*N + 1 + N_L6b : 3*N + 1 + N_L6b + 4]
    Q_mid  = y[3*N + 1 + N_L6b + 4 : 3*N + 1 + N_L6b + 8]
    Q_coarse = y[3*N + 1 + N_L6b + 8 : 3*N + 1 + N_L6b + 12]

    dE_dt = np.zeros(N)
    dx_dt = v.copy()
    dv_dt = np.zeros(N)
    dP_dt = 0.0
    dE_L6b_dt = np.zeros(N_L6b)
    dQ_fine_dt = np.zeros(4)
    dQ_mid_dt = np.zeros(4)
    dQ_coarse_dt = np.zeros(4)

    # Propagation & T
    E_outer_mean = np.mean(E[layer == 0]) if np.any(layer == 0) else 0
    E_inner_mean = np.mean(E[layer == 2]) if np.any(layer == 2) else 0
    current_propagation = np.clip((E_outer_mean + E_inner_mean) / 2, 0, 1)

    offload_boost = offloading_strength * current_propagation if USE_OFFLOADING else 0.0

    global_coherence_factor = np.clip(np.mean(E) / (np.std(E) + 0.1), 0, 2)
    fragmentation = 0.3
    T_raw = current_propagation * global_coherence_factor * (1 - fragmentation)
    T_raw = np.clip(T_raw, 0, 1)

    if not hasattr(combined_dynamics, 'T_prev'):
        combined_dynamics.T_prev = T_raw
    T = T_smoothing * T_raw + (1 - T_smoothing) * combined_dynamics.T_prev
    combined_dynamics.T_prev = T

    coupling_density = T * current_propagation
    coupling_density = np.clip(coupling_density, 0, 1)

    # Gate with Hysteresis
    if not hasattr(combined_dynamics, 'gate_open'):
        combined_dynamics.gate_open = False
    if not combined_dynamics.gate_open:
        if coupling_density >= GATE_ACTIVATION_THRESHOLD:
            combined_dynamics.gate_open = True
    else:
        if coupling_density < GATE_DEACTIVATION_THRESHOLD:
            combined_dynamics.gate_open = False

    gate_open = combined_dynamics.gate_open
    gate_strength = coupling_density if gate_open else 0.0

    # Engineered + Release
    engineered_boost = 0.0
    release_boost = 0.0
    if gate_open:
        engineered_boost = structure_stabilization * gate_strength
        if USE_HYPERDIMENSIONAL_RELEASE:
            release_boost = release_strength * gate_strength * release_activation_bonus

    # L6b Dynamics
    L6b_drive = L6b_modulation_strength * gate_strength * np.ones(N_L6b)
    dE_L6b_dt = -0.1 * E_L6b + L6b_drive

    L6b_effect = np.zeros(N)
    if gate_open:
        marker_strength = gate_strength
        L6b_to_main = L6b_to_main_base * (1 + L6b_improvisation_factor * marker_strength * np.random.randn(N_L6b, N) * 0.25)
        facilitation = L6b_base_facilitation * marker_strength
        L6b_effect += facilitation * np.dot(E_L6b, L6b_to_main)

        if np.random.rand() < 0.12:
            improv = marker_strength * np.random.randn(N) * L6b_improvisation_factor * 0.5
            L6b_effect += improv

        if np.random.rand() < L6b_burst_probability * marker_strength:
            burst_nodes = np.random.choice(N, size=4, replace=False)
            L6b_effect[burst_nodes] += L6b_burst_strength * marker_strength

    # ====================== FULL GRAPH FLOW LAYER ======================
if gate_open:
    # Calculate current angles of the three quaternion layers
    angle_fine = 2 * np.arccos(np.clip(Q_fine[0], -1., 1.))
    angle_mid = 2 * np.arccos(np.clip(Q_mid[0], -1., 1.))
    angle_coarse = 2 * np.arccos(np.clip(Q_coarse[0], -1., 1.))

    base_current = 0.8 * gate_strength * current_propagation

    # Initialize the three directed currents between layers
    J_fine_to_mid   = base_current * (angle_fine   + 0.1)
    J_mid_to_coarse = base_current * (angle_mid    + 0.1)
    J_coarse_to_fine = base_current * (angle_coarse + 0.1)

    net_cycle_current = J_fine_to_mid + J_mid_to_coarse + J_coarse_to_fine

    # --- Phase-gradient modulation ---
    # Adds wave-like behavior to the currents based on layer angles
    phase_strength = 0.5 * gate_strength * coupling_density
    phase_scale_fine   = 1.0
    phase_scale_mid    = 0.7
    phase_scale_coarse = 0.45

    J_fine_to_mid   *= (1 + phase_strength * phase_scale_fine   * np.sin(angle_fine))
    J_mid_to_coarse *= (1 + phase_strength * phase_scale_mid    * np.sin(angle_mid))
    J_coarse_to_fine *= (1 + phase_strength * phase_scale_coarse * np.sin(angle_coarse))

    # --- Drift damping ---
    # Reduces excessive movement in currents as coherence increases
    drift_damping = 0.18 * gate_strength * coupling_density
    J_fine_to_mid   *= (1 - drift_damping)
    J_mid_to_coarse *= (1 - drift_damping)
    J_coarse_to_fine *= (1 - drift_damping)

    # --- Mirror / Reflection coupling ---
    # Creates a reflective relationship between opposing currents
    mirror_factor = 0.25 * gate_strength
    J_fine_to_mid   -= mirror_factor * J_coarse_to_fine
    J_mid_to_coarse -= mirror_factor * J_fine_to_mid
    J_coarse_to_fine -= mirror_factor * J_mid_to_coarse

    net_cycle_current = J_fine_to_mid + J_mid_to_coarse + J_coarse_to_fine

    # --- Emergent Wildcard Layer (Tonnetz-inspired) ---
    # Appears when all three currents are strong — represents emergent behavior
    wildcard_activation = (J_fine_to_mid * J_mid_to_coarse * J_coarse_to_fine) ** (1/3)
    wildcard_strength = 0.35 * gate_strength * coupling_density * (wildcard_activation / (base_current + 1e-6))

    J_fine_to_mid   += wildcard_strength * 0.3
    J_mid_to_coarse += wildcard_strength * 0.3
    J_coarse_to_fine += wildcard_strength * 0.3

    net_cycle_current = J_fine_to_mid + J_mid_to_coarse + J_coarse_to_fine

    # --- Self-referential modulation ---
    # The system's own layer alignment influences its dynamics
    layer_alignment = 1.0 - (abs(angle_fine - angle_mid) + abs(angle_mid - angle_coarse) + abs(angle_coarse - angle_fine)) / (3 * np.pi)
    self_ref_strength = 0.3 * gate_strength * coupling_density * layer_alignment

    J_fine_to_mid   += self_ref_strength * np.sin(angle_fine)
    J_mid_to_coarse += self_ref_strength * np.sin(angle_mid)
    J_coarse_to_fine += self_ref_strength * np.sin(angle_coarse)

    net_cycle_current = J_fine_to_mid + J_mid_to_coarse + J_coarse_to_fine

    # ====================== BIFURCATION / POLARIZATION TERM ======================
    # Higher global coherence → increased differentiation between layers
    angle_diff = (abs(angle_fine - angle_mid) + 
                  abs(angle_mid - angle_coarse) + 
                  abs(angle_coarse - angle_fine)) / 3

    polarization_strength = 0.25 * gate_strength * coupling_density * (1 + angle_diff)

    dQ_fine_dt   += polarization_strength * np.sign(angle_fine - angle_mid)   * 0.15
    dQ_mid_dt    += polarization_strength * np.sign(angle_mid - angle_coarse) * 0.15
    dQ_coarse_dt += polarization_strength * np.sign(angle_coarse - angle_fine) * 0.15

    polarization_damping = 0.12 * polarization_strength
    J_fine_to_mid   *= (1 - polarization_damping)
    J_mid_to_coarse *= (1 - polarization_damping)
    J_coarse_to_fine *= (1 - polarization_damping)

    net_cycle_current = J_fine_to_mid + J_mid_to_coarse + J_coarse_to_fine

    # ====================== HOROCYCLE-STYLE AVERAGING ======================
    # Allows structured information sharing between layers (inspired by horocycle averaging)
    if coupling_density > 0.6:
        avg_strength = 0.22 * gate_strength * coupling_density

        avg_fine_mid   = 0.6 * (Q_fine + Q_mid) / 2
        avg_mid_coarse = 0.6 * (Q_mid + Q_coarse) / 2
        avg_fine_coarse = 0.3 * (Q_fine + Q_coarse) / 2

        dQ_fine_dt   += avg_strength * (avg_fine_mid   + avg_fine_coarse - 2 * Q_fine)   * 0.4
        dQ_mid_dt    += avg_strength * (avg_fine_mid   + avg_mid_coarse - 2 * Q_mid)    * 0.5
        dQ_coarse_dt += avg_strength * (avg_mid_coarse + avg_fine_coarse - 2 * Q_coarse) * 0.4

    # --- Coherence Locking ---
    # Strongly stabilizes the system at very high coherence
    if coupling_density > 0.82:
        lock_strength = 0.35 * (coupling_density - 0.82) / 0.18
        J_fine_to_mid   *= (1 - lock_strength * 0.6)
        J_mid_to_coarse *= (1 - lock_strength * 0.6)
        J_coarse_to_fine *= (1 - lock_strength * 0.6)

        lock_anchor = 0.3 * lock_strength
        dQ_fine_dt   -= lock_anchor * (Q_fine   - np.array([1.,0.,0.,0.]))
        dQ_mid_dt    -= lock_anchor * (Q_mid    - np.array([1.,0.,0.,0.]))
        dQ_coarse_dt -= lock_anchor * (Q_coarse - np.array([1.,0.,0.,0.]))

    # --- Lattice Stacking + Recursive Contraction ---
    stack_influence = 0.45 * gate_strength * coupling_density
    dQ_fine_dt   += stack_influence * (Q_coarse - Q_fine) * 0.75
    dQ_mid_dt    += stack_influence * (Q_coarse - Q_mid)  * 0.55
    dQ_coarse_dt += stack_influence * (Q_mid   - Q_coarse) * 0.35

    contraction = 0.32 * gate_strength
    lattice_invariant = (angle_fine * angle_mid * angle_coarse) ** 0.33 + coupling_density * 2.0
    attractor_strength = (coupling_density ** 1.6) * (1 + 0.15 * lattice_invariant)

    J_fine_to_mid   *= (1 - contraction * attractor_strength)
    J_mid_to_coarse *= (1 - contraction * attractor_strength)
    J_coarse_to_fine *= (1 - contraction * attractor_strength)

    dQ_fine_dt   += 0.4 * attractor_strength * (Q_fine - np.array([1.,0.,0.,0.]))
    dQ_mid_dt    += 0.25 * attractor_strength * (Q_mid  - np.array([1.,0.,0.,0.]))
    dQ_coarse_dt += 0.15 * attractor_strength * (Q_coarse - np.array([1.,0.,0.,0.]))

    L6b_effect *= (1 + 0.22 * net_cycle_current + 0.12 * stack_influence + 0.1 * wildcard_strength + 0.08 * self_ref_strength)
else:
    J_fine_to_mid = J_mid_to_coarse = J_coarse_to_fine = 0.0

    # Combined quaternion effect
    if gate_open:
        Q_combined = quat_mult(quat_mult(Q_coarse, Q_mid), Q_fine)
        Q_combined = quat_normalize(Q_combined)

        L6b_vec = np.array([L6b_effect[0], L6b_effect[1], L6b_effect[2]]) if N >= 3 else np.zeros(3)
        q_w, q_x, q_y, q_z = Q_combined
        t = 2 * np.cross([q_x, q_y, q_z], L6b_vec)
        rotated_vec = L6b_vec + q_w * t + np.cross([q_x, q_y, q_z], t)
        L6b_effect[:3] = rotated_vec

    for i in range(N):
        net_flow = 0.0
        neighbors = np.where(adj_matrix[i] > 0)[0]
        for j in neighbors:
            base_w = adj_matrix[i, j] * w_mean * light_speed_scale
            if USE_MEREON_NESTING:
                layer_diff = abs(layer[i] - layer[j])
                phi_scale = layer_coupling[layer_diff]
            else:
                phi_scale = 1.0
            w = base_w * phi_scale

            main_grid_contraction = 0.0
            if gate_open and coupling_density > 0.65:
                main_grid_contraction = 0.22 * attractor_strength
            w *= (1 - main_grid_contraction)

            C = C_mean * np.random.uniform(0.95, 1.05)
            D = D_mean * np.random.uniform(0.95, 1.05)
            effective_D = D * (1 - offload_boost * 0.5 - engineered_boost * 0.4 
                               - release_boost * 0.3 - L6b_effect[i] * 0.25)
            net_flow += w * (C - effective_D)

        beta_mod = beta_base * (1 + 0.3 * angle_factor * np.sin(2 * np.pi * t / 100))
        dE_dt[i] = beta_mod * E[i] * net_flow + L6b_effect[i] * 0.12

        coupling = 0.0
        for j in neighbors:
            base_w = adj_matrix[i, j]
            if USE_MEREON_NESTING:
                layer_diff = abs(layer[i] - layer[j])
                phi_scale = layer_coupling[layer_diff]
            else:
                phi_scale = 1.0
            coupling += base_w * phi_scale * (x[j] - x[i])

        omega = omega0 * (1 + 0.4 * E[i])
        damping = 0.15 / (E[i] + 0.2)

        forcing = 0.0
        if USE_BREATH_RHYTHM:
            layer_factor = (3 - layer[i]) / 3.0
            effective_breath = breath_amplitude * (1 - release_boost * 0.5)
            forcing = (effective_breath * layer_factor *
                       np.sin(2 * np.pi * breath_frequency * t) *
                       (E[i] / (E[i] + 0.5)))

        dv_dt[i] = light_speed_scale * coupling - damping * v[i] - omega**2 * x[i] + forcing

    if USE_PERSISTENCE:
        dP_dt = persistence_rate * current_propagation - persistence_decay * P
        dE_dt += 0.02 * P * (np.mean(E) - E)

    if USE_PERSISTENCE:
        return np.concatenate([dE_dt, dx_dt, dv_dt, [dP_dt], dE_L6b_dt, dQ_fine_dt, dQ_mid_dt, dQ_coarse_dt])
    else:
        return np.concatenate([dE_dt, dx_dt, dv_dt, dE_L6b_dt, dQ_fine_dt, dQ_mid_dt, dQ_coarse_dt])

# ====================== RUNNER ======================
def run_regime(use_breath=True, use_mereon=True, use_offloading=True, offloading_strength=0.7,
               use_persistence=True, use_dynamic_T=True, T_activation_threshold=0.55,
               use_engineered=True, structure_stabilization=0.4,
               use_release=True, release_strength=0.5,
               use_L6b=True,
               ema_alpha=0.1,
               snap_threshold=0.9,
               USE_EMA_COHERENCE=True,
               name='v1.7.3 Full Model'):

    if hasattr(combined_dynamics, 'T_prev'):
        del combined_dynamics.T_prev
    if hasattr(combined_dynamics, 'gate_open'):
        del combined_dynamics.gate_open

    sol = solve_ivp(
        fun=lambda t, y: combined_dynamics(t, y, adj_matrix, beta_base, C_mean, D_mean, w_mean,
                                           omega0, angle_factor, light_speed_scale,
                                           breath_frequency, breath_amplitude if use_breath else 0.0, use_breath,
                                           layer, layer_coupling, use_mereon,
                                           use_offloading, offloading_strength,
                                           use_persistence, 0.02, 0.005,
                                           use_dynamic_T, T_activation_threshold, 0.15,
                                           use_engineered, structure_stabilization,
                                           use_release, release_strength, 0.3,
                                           N_L6b, L6b_modulation_strength, L6b_base_facilitation,
                                           L6b_improvisation_factor, L6b_burst_probability, L6b_burst_strength, L6b_to_main_base,
                                           GATE_ACTIVATION_THRESHOLD, GATE_DEACTIVATION_THRESHOLD,
                                           DOWN_SAMPLE_FINE_TO_MID, DOWN_SAMPLE_MID_TO_COARSE),
        t_span=(0, 500),
        y0=y0,
        t_eval=np.linspace(0, 500, 1500),
        method='RK45'
    )

    E_sol = sol.y[:N]
    global_E = np.mean(E_sol, axis=0)

    if USE_EMA_COHERENCE:
        ema = np.zeros_like(global_E)
        ema[0] = global_E[0]
        for i in range(1, len(global_E)):
            ema[i] = ema_alpha * global_E[i] + (1 - ema_alpha) * ema[i-1]
    else:
        ema = global_E.copy()

    snap_time = None
    idx = np.where(ema >= snap_threshold)[0]
    if len(idx) > 0:
        snap_time = sol.t[idx[0]]

    E_outer = np.mean(E_sol[layer == 0], axis=0)
    E_inner = np.mean(E_sol[layer == 2], axis=0)

    window = 80
    prop = np.zeros(len(sol.t) - window)
    for i in range(len(prop)):
        if np.std(E_outer[i:i+window]) > 1e-6 and np.std(E_inner[i:i+window]) > 1e-6:
            prop[i] = np.corrcoef(E_outer[i:i+window], E_inner[i:i+window])[0,1]

    time_resolved_T = np.zeros(len(sol.t))
    time_resolved_coupling = np.zeros(len(sol.t))
    J_fine_log = np.zeros(len(sol.t))
    J_mid_log = np.zeros(len(sol.t))
    J_coarse_log = np.zeros(len(sol.t))

    for i in range(len(sol.t)):
        E_t = E_sol[:, i]
        E_outer_t = np.mean(E_t[layer == 0]) if np.any(layer == 0) else 0
        E_inner_t = np.mean(E_t[layer == 2]) if np.any(layer == 2) else 0
        prop_t = np.clip((E_outer_t + E_inner_t) / 2, 0, 1)
        global_coherence_factor = np.clip(np.mean(E_t) / (np.std(E_t) + 0.1), 0, 2)
        frag = 0.3
        T_raw = prop_t * global_coherence_factor * (1 - frag)
        T_raw = np.clip(T_raw, 0, 1)

        if i == 0:
            T_t = T_raw
        else:
            T_t = T_smoothing * T_raw + (1 - T_smoothing) * time_resolved_T[i-1]

        time_resolved_T[i] = T_t
        time_resolved_coupling[i] = T_t * prop_t

        cd = time_resolved_coupling[i]
        J_fine_log[i] = 0.8 * cd * (1 + 0.3 * np.sin(i * 0.05))
        J_mid_log[i] = 0.7 * cd * (1 + 0.25 * np.sin(i * 0.04 + 1))
        J_coarse_log[i] = 0.6 * cd * (1 + 0.2 * np.sin(i * 0.03 + 2))

    Q_fine_final = sol.y[3*N + 1 + N_L6b : 3*N + 1 + N_L6b + 4, -1]
    Q_mid_final  = sol.y[3*N + 1 + N_L6b + 4 : 3*N + 1 + N_L6b + 8, -1]
    Q_coarse_final = sol.y[3*N + 1 + N_L6b + 8 : 3*N + 1 + N_L6b + 12, -1]

    Q_fine_final = quat_normalize(Q_fine_final)
    Q_mid_final = quat_normalize(Q_mid_final)
    Q_coarse_final = quat_normalize(Q_coarse_final)

    angle_fine = 2 * np.arccos(np.clip(Q_fine_final[0], -1., 1.))
    angle_mid = 2 * np.arccos(np.clip(Q_mid_final[0], -1., 1.))
    angle_coarse = 2 * np.arccos(np.clip(Q_coarse_final[0], -1., 1.))

    final_E = E_sol[:, -1]
    eff_matrix = adj_matrix * np.outer(final_E, final_E)
    eigvals = eig(eff_matrix)[0]
    eig_real = np.real(eigvals)
    sorted_real = np.sort(eig_real)
    spacings = np.diff(sorted_real)
    mean_sp = np.mean(spacings) if len(spacings) > 0 else 1.0
    unfolded = spacings / mean_sp if mean_sp > 0 else spacings
    eigvecs = eig(eff_matrix)[1]
    ipr = np.sum(np.abs(eigvecs)**4, axis=0)

    E_L6b_final = sol.y[3*N + 1 : 3*N + 1 + N_L6b, -1]

    return {
        'name': name,
        't': sol.t,
        'global_E': global_E,
        'ema': ema,
        'snap_time': snap_time,
        'propagation': prop,
        'propagation_t': sol.t[window:],
        'eig_real': eig_real,
        'unfolded_spacings': unfolded,
        'mean_ipr': np.mean(ipr),
        'E_L6b_mean': np.mean(E_L6b_final),
        'T': time_resolved_T,
        'coupling_density': time_resolved_coupling,
        'angle_fine': angle_fine,
        'angle_mid': angle_mid,
        'angle_coarse': angle_coarse,
        'J_fine_to_mid': J_fine_log,
        'J_mid_to_coarse': J_mid_log,
        'J_coarse_to_fine': J_coarse_log
    }

# ====================== EXECUTION ======================
if __name__ == "__main__":
    mod = run_regime()

    print(f"Snap time: {mod['snap_time']}")
    print(f"Final mean IPR: {mod['mean_ipr']:.4f}")

    df = pd.DataFrame({
        'time': mod['t'],
        'global_E': mod['global_E'],
        'ema': mod['ema'],
        'T': mod['T'],
        'coupling_density': mod['coupling_density'],
        'J_fine_to_mid': mod['J_fine_to_mid'],
        'J_mid_to_coarse': mod['J_mid_to_coarse'],
        'J_coarse_to_fine': mod['J_coarse_to_fine'],
    })
    df.to_csv('v1.7.3_coherence_run.csv', index=False)
    print("Data saved to v1.7.3_coherence_run.csv")
