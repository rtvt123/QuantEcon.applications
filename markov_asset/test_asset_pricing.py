"""
Filename: test_asset_pricing.py
Authors: Spencer Lyon
Date: 2014-07-30

Tests for quantecon.asset_pricing module


"""
import numpy as np
import quantecon as qe
from asset_pricing import *

# parameters for object
n = 5
P = 0.0125 * np.ones((n, n))
P += np.diag(0.95 - 0.0125 * np.ones(5))
s = np.array([1.05, 1.025, 1.0, 0.975, 0.95])  # state values
mc = qe.MarkovChain(P, state_values=s)

gamma = 2.0
beta = 0.94
zeta = 1.0
p_s = 150.0


apm = AssetPriceModel(beta, mc, gamma)

print(tree_price(apm))

print(consol_price(apm, zeta))

print(call_option(apm, zeta, p_s))

