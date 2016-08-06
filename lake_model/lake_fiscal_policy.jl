#=
Compute and plot welfare, employment, unemployment, and tax revenue as a
function of the unemployment compensation rate in the lake model.
=#

using QuantEcon
using Distributions
using Roots
using Plots
pyplot()

include("lake_model.jl")
include("../mccall/mccall_bellman_iteration.jl")
include("../mccall/compute_reservation_wage.jl")

# Some global variables that will stay constant
alpha = 0.013
alpha_q = (1-(1-alpha)^3)
b = 0.0124
d = 0.00822
beta = 0.98
gamma = 1.0
sigma = 2.0

# The default wage distribution: a discretized log normal
log_wage_mean, wage_grid_size, max_wage = 20, 200, 170
w_vec = linspace(1e-3, max_wage, wage_grid_size + 1)
logw_dist = Normal(log(log_wage_mean), 1)
cdf_logw = cdf(logw_dist, log(w_vec))
pdf_logw = cdf_logw[2:end] - cdf_logw[1:end-1]
p_vec = pdf_logw ./ sum(pdf_logw)
w_vec = (w_vec[1:end-1] + w_vec[2:end]) / 2

function compute_optimal_quantities(c::Float64, tau::Float64)
  """
  Compute the reservation wage, job finding rate and value functions of the
  workers given c and tau.

  """

  mcm = McCallModel(alpha_q,
                    beta,
                    gamma,
                    c-tau,           # post-tax compensation
                    sigma,
                    collect(w_vec-tau),   # post-tax wages
                    p_vec)


  w_bar, V, U = compute_reservation_wage(mcm, return_values=true)
  lmda = gamma * sum(p_vec[w_vec-tau .> w_bar])

  return w_bar, lmda, V, U
end


function compute_steady_state_quantities(c::Float64, tau::Float64)
  """
  Compute the steady state unemployment rate given c and tau using optimal
  quantities from the McCall model and computing corresponding steady state
  quantities

  """

  w_bar, lmda, V, U = compute_optimal_quantities(c, tau)

  # Compute steady state employment and unemployment rates
  lm = LakeModel(lambda=lmda, alpha=alpha_q, b=b, d=d)
  x = rate_steady_state(lm)
  e_rate, u_rate = x

  # Compute steady state welfare
  w = sum(V .* p_vec .* (w_vec - tau .> w_bar)) / sum(p_vec .* (w_vec - tau .> w_bar))
  welfare = e_rate .* w + u_rate .* U

  return e_rate, u_rate, welfare
end


function find_balanced_budget_tax(c::Float64)
  """
  Find tax level that will induce a balanced budget.

  """

  function steady_state_budget(t::Float64)
    e_rate, u_rate, w = compute_steady_state_quantities(c, t)
    return t - u_rate * c
  end

  tau = fzero(steady_state_budget, 0.0, 0.9 * c)

  return tau
end

# Levels of unemployment insurance we wish to study
c_vec = linspace(5.0, 140.0, 60)

tax_vec = []
unempl_vec = []
empl_vec = []
welfare_vec = []

for c in c_vec
  t = find_balanced_budget_tax(c)
  e_rate, u_rate, welfare = compute_steady_state_quantities(c, t)
  push!(tax_vec, t)
  push!(unempl_vec, u_rate)
  push!(empl_vec, e_rate)
  push!(welfare_vec, welfare)
end

titles = ["Unemployment" "Employment" "Tax" "Welfare"]
plot(c_vec, [unempl_vec empl_vec tax_vec welfare_vec],
    color=:blue, lw=2, alpha=0.7, title=titles, legend=:none, layout=(2,2))
