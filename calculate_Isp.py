import cantera as ct
import numpy as np

def calculate_rocket_performance(T0=300, P0=400*101325, equivalence_ratio=1.4):
    # Create gas object
    gas = ct.Solution('gri30.yaml')
    
    # Set initial state and mixture (fuel-rich for better performance)
    gas.TP = T0, P0
    gas.set_equivalence_ratio(equivalence_ratio, {'CH4': 1}, {'O2': 1})
    
    # Calculate adiabatic flame temperature
    gas.equilibrate('HP')
    T_comb = gas.T
    
    # Store combustion products composition
    X_products = gas.X
    
    # Now expand isentropically to exit pressure
    p_ex = 101325.0  # atmospheric
    s_comb = gas.s  # entropy at combustion
    
    # Isentropic expansion to exit pressure
    gas.SP = s_comb, p_ex
    T_ex = gas.T
    h_ex = gas.enthalpy_mass
    
    # Get enthalpy at combustion conditions
    gas.TP = T_comb, P0
    gas.X = X_products  # Use actual products
    h_comb = gas.enthalpy_mass
    
    # Calculate exit velocity
    delta_h = h_comb - h_ex
    v_e = np.sqrt(2 * delta_h) * 0.95  # velocity correction factor
    
    # Specific impulse
    g0 = 9.8066
    Isp = v_e / g0
    
    return Isp, v_e, T_comb, T_ex

# Run with fuel-rich mixture

Isp, v_e, T_comb, T_ex = calculate_rocket_performance(equivalence_ratio=1.373)

# optimizer gets an equivalence ratio of 1.373
# import scipy as sp
# F = lambda eq: -calculate_rocket_performance(equivalence_ratio=eq)[0]
# res = sp.optimize.minimize(F, 1.0, method='CG')
# print(res)

if __name__ == '__main__':
    print(f'Specific Impulse: {Isp:.2f} s')
    print(f'Exit velocity: {v_e/1000:.2f} km/s')
    print(f'Chamber temperature: {int(T_comb)} K')
    print(f'Exit temperature: {int(T_ex)} K')