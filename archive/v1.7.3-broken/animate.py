import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

df = pd.read_csv('v1.7.3_coherence_run.csv')

fig, axs = plt.subplots(3, 1, figsize=(13, 9), sharex=True)
fig.suptitle('Coherence Pump — Graph Flow Dynamics', fontsize=16, fontweight='bold')

# Coupling Density
line_coupling, = axs[0].plot([], [], color='#3b82f6', linewidth=2.2, label='Coupling Density')
axs[0].axhline(y=0.55, color='#64748b', linestyle='--', alpha=0.7, label='Gate Threshold')
axs[0].set_ylabel('Coupling Density')
axs[0].legend(loc='upper right', fontsize=9)
axs[0].grid(True, alpha=0.2)
axs[0].set_ylim(0, 1.08)

# Quaternion Angles
line_fine, = axs[1].plot([], [], color='#ef4444', linewidth=2, label='Fine')
line_mid, = axs[1].plot([], [], color='#22c55e', linewidth=2, label='Mid')
line_coarse, = axs[1].plot([], [], color='#3b82f6', linewidth=2, label='Coarse')
axs[1].set_ylabel('Quaternion Angles')
axs[1].legend(loc='upper right', fontsize=9)
axs[1].grid(True, alpha=0.2)

# Graph Currents
line_j1, = axs[2].plot([], [], color='#06b6d4', linewidth=2, label='J Fine → Mid')
line_j2, = axs[2].plot([], [], color='#a855f7', linewidth=2, label='J Mid → Coarse')
line_j3, = axs[2].plot([], [], color='#eab308', linewidth=2, label='J Coarse → Fine')
axs[2].set_xlabel('Time')
axs[2].set_ylabel('Graph Currents')
axs[2].legend(loc='upper right', fontsize=9)
axs[2].grid(True, alpha=0.2)

def init():
    for line in [line_coupling, line_fine, line_mid, line_coarse, line_j1, line_j2, line_j3]:
        line.set_data([], [])
    return line_coupling, line_fine, line_mid, line_coarse, line_j1, line_j2, line_j3

def update(frame):
    x = df['time'].values[:frame + 1]
    line_coupling.set_data(x, df['coupling_density'].values[:frame + 1])
    line_fine.set_data(x, df['angle_fine'].values[:frame + 1])
    line_mid.set_data(x, df['angle_mid'].values[:frame + 1])
    line_coarse.set_data(x, df['angle_coarse'].values[:frame + 1])
    line_j1.set_data(x, df['J_fine_to_mid'].values[:frame + 1])
    line_j2.set_data(x, df['J_mid_to_coarse'].values[:frame + 1])
    line_j3.set_data(x, df['J_coarse_to_fine'].values[:frame + 1])

    if len(x) > 1:
        for ax in axs:
            ax.set_xlim(x[0], x[-1])
    return line_coupling, line_fine, line_mid, line_coarse, line_j1, line_j2, line_j3

ani = FuncAnimation(fig, update, frames=len(df), init_func=init, interval=20, blit=True)
plt.tight_layout()
plt.show()
