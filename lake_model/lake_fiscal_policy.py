"""
Plot welfare, employment, unemployment, and tax revenue as a function of the
unemployment compensation rate in the lake model.

For fixed parameters 

    alpha = job separation rate, 
    beta = discount rate, 
    gamma = job destruction rate
    w_vec, p_vec = possible wage values and their probabilities
    b, d = entry and exit rates for labor force

and a given utility function u,

"""

import numpy as np 
import matplotlib.pyplot as plt
from lake_model import LakeModel
from scipy.stats import norm
from scipy.optimize import newton

# What to do about these imports?  I'm currently using sym links...
from mccall_bellman_iteration import McCallModel  
from compute_reservation_wage import compute_reservation_wage 

# Some global variables that will stay constant

alpha  = 0.013               # monthly
alpha_q = (1-(1-alpha)**3)   # quarterly
b      = 0.0124
d      = 0.00822
beta   = 0.99                   
gamma  = 1

# Default utility function

sigma = 2
def u(c):
    return (c**(1 - sigma) - 1) / (1 - sigma)

# The default wage distribution --- a discretized lognormal

log_wage_mean, wage_grid_size, max_wage = 20, 200, 175
logw_dist = norm(np.log(log_wage_mean), 1)
w_vec = np.linspace(0, max_wage, wage_grid_size + 1) # wage grid
cdf = logw_dist.cdf(np.log(w_vec))
pdf = cdf[1:]-cdf[:-1]
p_vec = pdf / pdf.sum()
w_vec = (w_vec[1:] + w_vec[:-1])/2

# Levels of unemployment insurance we wish to study
c_vec = np.linspace(5, 135 ,25)

def compute_lambda(c, T):
    """
    Compute the job finding rate given c and T by first computing the
    reservation wage from the McCall model.

    """
    
    mcm = McCallModel(alpha=alpha, 
                     beta=beta, 
                     gamma=gamma, 
                     c=c-T,         # post tax compensation
                     u=u, 
                     w_vec=w_vec-T, # post tax wages
                     p_vec=p_vec)

    w_bar = compute_reservation_wage(mcm)
    lmda = np.sum(p_vec[w_vec > w_bar])
    return lmda


def compute_steady_state_unemployment(c, T):
    """
    Compute the steady state unemployment rate given c and T using lambda, the
    job finding rate, from the McCall model and then computing steady state
    unemployment corresponding to alpha, lambda, b, d.

    """
    lmda = compute_lambda(c, T)
    lm = LakeModel(alpha=alpha, lmda=lmda, b=0, d=0) 
    x = lm.rate_steady_state()
    e, u = x
    return u

     
def find_balanced_budget_tax(c):
    """
    Find the smallest tax that will induce a balanced budget

    """
    def steady_state_budget(t):
        u = compute_steady_state_unemployment(c, t)
        return t - u * c

    T = newton(steady_state_budget, 0.0001)
    return T


## Now step through all c values to be considered.  At each one, find budget
## balancing T, and then evaluate welfare, employment and unemployment at this
## pair (c, T).  Plot the values against c.




