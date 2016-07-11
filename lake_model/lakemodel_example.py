# -*- coding: utf-8 -*-
"""
Created on Fri Feb 27 18:08:44 2015

Author: David Evans

Example Usage of LakeModel in lake
"""
import numpy as np
import matplotlib.pyplot as plt
from lake import LakeModel, LakeModelAgent, LakeModel_Equilibrium
from scipy.stats import norm
#Use Matplotlib to Adjust style#
import matplotlib
matplotlib.style.use('ggplot')

#Initialize Parameters
alpha = 0.013
lamb = 0.283
b = 0.0124
d = 0.00822
g = b-d
N0 = 150.
e0 = 0.92
u0 = 1-e0
T = 5000


# using quaterly data
alpha_q = (1-(1-alpha)**3)   # alpha is monthly and alpha_q is quarterly
gamma = 1

logw_dist = norm(np.log(20), 1)
w = np.linspace(0, 175, 201)# wage grid

# compute probability of each wage level 
cdf = logw_dist.cdf(np.log(w))
pdf = cdf[1:]-cdf[:-1]
pdf /= pdf.sum()
w = (w[1:] + w[:-1])/2

#Find the quilibirum
LME = LakeModel_Equilibrium(alpha_q, gamma, 0.99, 2.00, pdf, w)

#possible levels of unemployment insurance
cvec = np.linspace(5, 135 ,25)
T, W, U, EV, pi = map(np.vstack,zip(* [LME.find_steady_state_tax(c) for c in cvec]))
W = W[:]
T = T[:]
U = U[:]
EV = EV[:]
i_max = np.argmax(W)

plt.plot(cvec,W)
plt.xlabel(r'$c$')
plt.title(r'Welfare' )
plt.vlines(cvec[i_max],axes.get_ylim()[0],max(W),'k','-.')

plt.plot(cvec,T)
plt.vlines(cvec[i_max],axes.get_ylim()[0],T[i_max],'k','-.')
plt.xlabel(r'$c$')
plt.title(r'Taxes' )


plt.plot(cvec,pi[:,0])
plt.vlines(cvec[i_max],axes.get_ylim()[0],pi[i_max,0],'k','-.')
plt.xlabel(r'$c$')
plt.title(r'Employment Rate' )

plt.plot(cvec,pi[:,1])
plt.vlines(cvec[i_max],axes.get_ylim()[0],pi[i_max,1],'k','-.')
plt.xlabel(r'$c$')
plt.title(r'Unemployment Rate' )
plt.tight_layout()
