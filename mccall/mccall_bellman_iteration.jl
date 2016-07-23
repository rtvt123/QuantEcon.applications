"""
Implements iteration on the Bellman equations to solve the McCall growth model

"""

from quantecon.distributions import BetaBinomial

# A default utility function

function u(c, sigma)
    if c > 0
        return (c^(1 - sigma) - 1) / (1 - sigma)
    else
        return -10e6
    end
end    

# default wage vector with probabilities

n = 60  # number of possible outcomes for wage
default_w_vec = np.linspace(10, 20, n)     # wages between 10 and 20
a, b = 600, 400  # shape parameters
dist = BetaBinomial(n-1, a, b)
default_p_vec = dist.pdf()  


type McCallModel
    alpha :: Float64        # Job separation rate
    beta :: Float64         # Discount rate
    gamma :: Float64        # Job offer rate
    c :: Float64            # Unemployment compensation
    sigma :: Float64        # Utility parameter
    w_vec :: Array{Float64} # Possible wage values
    p_vec :: Array{Float64} # Probabilities over w_vec
end

function McCallModel(; alpha=0.2,
                       beta=0.98,
                       gamma=0.7,
                       c=6.0,   
                       sigma=2.0,
                       w_vec=none,  # Possible wage values
                       p_vec=none): # Probabilities over w_vec

        if w_vec is None:
            n = 60  # number of possible outcomes for wage
            self.w_vec = np.linspace(10, 20, n)     # wages between 10 and 20
            a, b = 600, 400  # shape parameters
            dist = BetaBinomial(n-1, a, b)
            self.p_vec = dist.pdf()  
        else:
            self.w_vec = w_vec
            self.p_vec = p_vec

function update_bellman!(mcm, V, V_new, U):
    """
    A function to update the Bellman equations.  Note that V_new is
    modified in place (i.e, modified by this function).  The new value of U is
    returned.

    """
    # Simplify notation
    alpha, beta, sigma, c, gamma = mcm.alpha, mcm.beta, mcm.sigma, mcm.gamma

    for w_idx, w in enumerate(mcm.w_vec):
        # w_idx indexes the vector of possible wages
        V_new[w_idx] = u(w, sigma) + beta * ((1 - alpha) * V[w_idx] + alpha * U)
        U_new = u(c, sigma) + beta * (1 - gamma) * U + 
                    beta * gamma * np.sum(np.maximum(U, V) * mcm.p_vec)

    return U_new
end


function solve_mccall_model(mcm, tol=1e-5, max_iter=2000):
    """
    Iterates to convergence on the Bellman equations 
    
    Parameters
    ----------
    mcm : an instance of McCallModel
    tol : float
        error tolerance
    max_iter : int
        the maximum number of iterations
    """

    V = np.ones(len(mcm.w_vec))  # Initial guess of V
    V_new = np.empty_like(V)     # To store updates to V
    U = 1                        # Initial guess of U
    i = 0
    error = tol + 1

    while error > tol and i < max_iter:
        U_new = _update_bellman(mcm.alpha, mcm.beta, mcm.gamma, 
                mcm.c, mcm.sigma, mcm.w_vec, mcm.p_vec, V, V_new, U)
        error_1 = np.max(np.abs(V_new - V))
        error_2 = np.abs(U_new - U)
        error = max(error_1, error_2)
        V[:] = V_new
        U = U_new
        i += 1

    return V, U

