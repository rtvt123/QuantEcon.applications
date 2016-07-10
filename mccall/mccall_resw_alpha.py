"""
Plots reservation wage against the job separation rate

"""

import numpy as np
import matplotlib.pyplot as plt
from mccall_bellman_iteration import McCallModel, solve_mccall_model
from compute_reservation_wage import compute_reservation_wage


grid_size = 25  
alpha_vals = np.linspace(0.05, 0.5, grid_size)  
w_bar_vals = np.empty_like(alpha_vals)

mcm = McCallModel()

fig, ax = plt.subplots()

for i, alpha in enumerate(alpha_vals):
    mcm.alpha = alpha
    w_bar = compute_reservation_wage(mcm)
    w_bar_vals[i] = w_bar

ax.set_xlabel('job separation rate')
ax.set_ylabel('reservation wage')
ax.set_xlim(alpha_vals.min(), alpha_vals.max())
txt = r'$\bar w$ as a function of $\alpha$'
ax.plot(alpha_vals, w_bar_vals, 'b-', lw=2, alpha=0.7, label=txt)
ax.legend(loc='upper right')
ax.grid()

plt.show()
