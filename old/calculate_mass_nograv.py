import numpy as np
sqrt = np.sqrt
exp = np.exp

r_earth = 6.357e6 # meters
altitude = 4.00e5 # meters
r_orbit = r_earth + altitude # meters

# calculate circular orbit
G_newt = 6.67e-11 # newton's gravitational constant
m_earth = 5.97e24 # mass of the earth, kg
a_orb = G_newt * m_earth / (r_earth**2)

# taking a_c = v^2/r
v_orbit = sqrt(r_orbit*a_orb)

# achooski rocket equation
from calculate_Isp import v_e # around 3.1 km/sec
f = exp(v_orbit / v_e)**-1 # mass fraction (mass of vehicle / mass of fuel)
m_dry = sum([
    1000, # payload (for sure). Assume it includes fairings
    3000, # rocket engine (??, based on rs25)
    2000, # fuel tank (should be a function of the amount of fuel), carbon fiber, idk
])
m_fuel = m_dry/f
m_total = m_dry + m_fuel

if __name__ == '__main__':
    print(f'orbital velocity for required altitude of {altitude} m: {v_orbit}')
    print(f'fuel mass fraction: {f}') # our rocket will be about 7% rocket
    print(f'{m_fuel=}')
    print(f'{m_total=}')
