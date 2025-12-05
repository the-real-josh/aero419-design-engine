import numpy as np
import scipy as sp

# set by karp
delta_v_req = 8.159e3 # m/sec

# design choices
m_dry = sum([
    3000,   # 1 equivalently-sized rocket engine
    1000,   # 1 payload, including fairings
    6000    # mass of the fuel tanks and other hardware
])
burn_time = 128.67 # seconds
f = 0.05 # mass fraction - NEEDS to be below 0.07, neglecting gravity (see old\calculate_mass_nograv.py)
m_propellant = m_dry/f

g = 9.8 # estimate for entire flight
m0 = m_dry + m_propellant # kgs
m_dot = (m_propellant)/burn_time # kg/se, averaged
m = lambda t: m0 - m_dot*t
from calculate_Isp import v_e
thrust = m_dot * v_e # newtons, ignores area-pressure term
F_net = lambda t: thrust - m(t)*g # net force is thrust minus weight
a = lambda t: F_net(t) / m(t)
res = sp.integrate.quad(a, 0, burn_time-0.001)
assert res[1] < 1e-2
v = res[0]

if __name__ == '__main__':
    print(f'fuel mass: {m_propellant:.2f} kg')
    print(f'average mass flow: {m_dot:.2f} kg/sec')
    print(f'delta_v with current config: {v:.2f} which {'CAN' if v>delta_v_req else 'CANNOT'} get us to orbit')

#