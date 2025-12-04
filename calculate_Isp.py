import cantera as ct
import numpy as np

# OVERALL GOAL: GET THE SPECIFIC IMPULSE (see bottom of code)
def calc_delta_h(T2, T1, p2=101325.0, p1=101325.0):
    # can generally assume that cp ≠ f(p) and get good results, so set arbitrary pressures for now
    # DO NOT assume perfect gas behavior, as T can be very high. Assume cp = f(T)
    # assume the gas is made of the following species: 1 mol co2 and 2 mol h2o
    # assume constituents do not liquify
    # write code here
    
    # Create gas object with CO2 and H2O
    gas = ct.Solution('gri30.yaml')
    
    # Set composition: 1 mol CO2, 2 mol H2O (mole fractions)
    gas.X = {'CO2': 1.0/3.0, 'H2O': 2.0/3.0}
    
    # Calculate specific enthalpy at state 1
    gas.TP = T1, p1
    h1 = gas.enthalpy_mass  # J/kg
    
    # Calculate specific enthalpy at state 2
    gas.TP = T2, p2
    h2 = gas.enthalpy_mass  # J/kg
    
    # Return specific enthalpy change in J/kg
    delta_h = h2 - h1  # J/kg
    
    return delta_h


def calculate_adiabatic_flame_temp(T0=300, P0=400*101325):
    fuel = {'CH4': 1}
    oxidizer = {'O2': 1}

    # Create gas object using GRI-Mech 3.0 (good for methane combustion)
    gas = ct.Solution('gri30.yaml')
    # Set initial state
    gas.TP = T0, P0
    
    # Set the equivalence ratio and mixture composition
    gas.set_equivalence_ratio(1, fuel, oxidizer)
    
    # Store initial enthalpy and density for different cases
    h0 = gas.h  # specific enthalpy
    rho0 = gas.density
    
    # Calculate adiabatic flame temperature at constant pressure
    gas_hp = ct.Solution('gri30.yaml')
    gas_hp.TPX = T0, P0, gas.X
    gas_hp.equilibrate('HP')  # Hold enthalpy and pressure constant
    T_ad_HP = gas_hp.T # constant-volume combustion
    
    # need to assume constant pressure since reactants are injected into the combustion chamber at the same 
    # pressure that the combustion occurs at
    # furthermore, open nozzle allows for expansion
    return T_ad_HP


k = 1.1386 # https://cearun.grc.nasa.gov/cgi-bin/CEARUN/donecea3.cgi
p_ex = 101325.0 # atmospheric ambient pressure
p_comb = p_ex * 400.0 # max attainable pressure rise in turbopumps
T_comb = calculate_adiabatic_flame_temp() # assume optimal combustion
T_ex = T_comb * (p_ex / p_comb)**((k-1)/k)  # T_ex = exit temperature
delta_h = calc_delta_h(T_comb, T_ex)
v_e = np.sqrt(2*delta_h) # adiabatic approximation
g0 = 9.8066 # m/sec^2
Isp = v_e / g0 # https://en.wikipedia.org/wiki/Rocket_engine#Types_of_rocket_engines

print(f'{Isp=:.2f}')
