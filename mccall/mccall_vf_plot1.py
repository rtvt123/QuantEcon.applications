"""
Generate plots of value of employment and unemployment in the McCall model.

"""

import numpy as np
import matplotlib.pyplot as plt

from mccall_bellman_iteration import McCallModel, solve_mccall_model

mcm = McCallModel()
V, U = solve_mccall_model(mcm)

fig, ax = plt.subplots()

ax.plot(mcm.w_vec, V, 'b-', lw=2, alpha=0.7, label='$V$')
ax.plot(mcm.w_vec, [U] *len(mcm.w_vec) , 'g-', lw=2, alpha=0.7, label='$U$')
ax.legend(loc='upper left')
ax.grid()

plt.show()
