import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

delta_v_req = 8.159e3 # m/sec
burn_time_cases = [10, 150, 300, 500]
delta_vs = []
for burn_time in burn_time_cases:
    print(f'BURN TIME CASE: {burn_time} seconds')
    g = 9.8 # estimate for entire flight
    m0_guess = 81000 # kgs
    m_dry = 5000 # kg
    m_fuel = m0_guess - m_dry
    m_dot = (m_fuel)/burn_time # kg/se, averaged
    m = lambda t: m0_guess - m_dot*t
    # from calculate_Isp import v_e
    v_e = 3.1e3 # m/s
    thrust = m_dot * v_e # newtons, ignores area-pressure term

    F_net = lambda t: thrust - m(t)*g # net force is thrust minus weight
    a = lambda t: F_net(t) / m(t)
    res = sp.integrate.quad(a, 0, burn_time-0.001)
    assert res[1] < 1e-2
    v = res[0]
    delta_vs.append(v)
    print(f'delta v: {v}')

plt.ylabel(f'delta_v')
plt.xlabel(f'burn time')
plt.plot([0, burn_time_cases[-1]], [delta_v_req, delta_v_req])
plt.plot(burn_time_cases, delta_vs)
plt.legend([f'burn time vs delta_v', f'minimum required delta_v'])
plt.show()
