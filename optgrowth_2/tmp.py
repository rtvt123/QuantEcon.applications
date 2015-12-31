from growth_models import *
val_functions = []
alphas = [0.5, 0.55, 0.6, 0.65]
for alpha in alphas:
    gm = LogLinearGrowthModel(alpha=alpha)
    vstar = gm.compute_value_function()
    val_functions.append(gm)
