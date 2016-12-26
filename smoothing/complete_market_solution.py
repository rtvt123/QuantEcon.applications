import numpy as np

def consumption_complete(beta, P, y, b0):
    """
    This function takes
        beta : discount factor
        P    : 2x2 transition matrix
        y    : list containing the two income levels
        b0   : debt in period 0 (= state_1 debt level)
    
    and returns 
        c_bar : constant consumption
        b1    : rolled over b0
        b2    : debt in state_2
        
    associated with the price system 
        Q = beta * P
    
    """
    
    y1, y2 = y          # extract income levels
    b1 = b0             # b1 is known to be equal to b0
    Q = beta * P        # assumed price system
    
    # Using equation (7) calculate b2
    b2 = (y2 - y1 - (Q[0, 0] - Q[1, 0] - 1) * b1)/(Q[0, 1] + 1 - Q[1, 1])
    
    # Using equation (5) calculae c_bar 
    c_bar = y1 - b0 + Q[0, :] @ np.asarray([b1, b2])
    
    return c_bar, b1, b2
