#=

Provides a class that simulates the dynamics of unemployment and employment in
the lake model. 

=#


type LakeModel
    lambda :: Float64  # job finding rate
    alpha :: Float64   # dismissal rate 
    b :: Float64       # entry rate into labor force
    d :: Float64       # exit rate from labor force
    g :: Float64       # net entry rate 
    A :: Matrix{Float64}       # Updates stock
    A_hat :: Matrix{Float64}   # Updates rate
end 


function LakeModel(;lambda=0.283, alpha=0.013, b=0.0124, d=0.00822)

    g = b - d
    A = [ (1-d) * (1-alpha)  (1-d) * lambda;
          (1-d) * alpha + b (1-lambda) * (1-d) + b]
    A_hat = A / (1 + g)

    return LakeModel(lambda, alpha, b, d, g, A, A_hat)
end
        
r"""
Finds the steady state of the system :math:`x_{t+1} = \hat A x_{t}`

Returns
--------
xbar : steady state vector of employment and unemployment rates
"""
function rate_steady_state(lm::LakeModel, tol=1e-6)
    x = 0.5 * ones(2)
    error = tol + 1
    while (error > tol)
        new_x = lm.A_hat * x
        error = maximum(abs(new_x - x))
        x = new_x
    end
    return x
end
        
r"""
Simulates the the sequence of Employment and Unemployent stocks

Parameters
------------
X0 : Array 
    Contains initial values (E0, U0)
T : Int
    Number of periods to simulate

Returns
--------- 
X : Matrix
    Contains sequence of employment and unemployment stocks
"""

function simulate_stock_path(lm::LakeModel, X0::Array{Float64}, T::Int)
    X_path = Array(Float64, 2, T)
    X = reshape(X0, 2, 1)
    for t in 1:T
        X_path[:, t] = X
        X = lm.A * X
    end
    return X_path
end
            
r"""
Simulates the the sequence of employment and unemployent rates.

Parameters
------------
x0 : Array 
    Contains initial values (e0,u0)
T : Int
    Number of periods to simulate

Returns
---------
x : Matrix
    Contains sequence of employment and unemployment rates

"""
function simulate_rate_path(lm::LakeModel, x0::Array{Float64}, T::Int)
    x_path = Array(Float64, 2, T)
    x = reshape(x0, 2, 1)
    for t in 1:T
        x_path[:, t] = x
        x = lm.A_hat * x
    end
    return x_path
end

