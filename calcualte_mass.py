import numpy as np
import scipy as sp
import matplotlib.pyplot as plt


delta_v_req = 8.159e3 # m/sec
burn_time_cases = [30, 128, 300]
plt.ylabel(r'$\Delta v$')
plt.xlabel(f'burn time')
mass_fractions = [0.07, 0.05, 0.03]
plt.plot([0, burn_time_cases[-1]], [delta_v_req, delta_v_req])
legends = [r'$\Delta v$ requirement']

for f in mass_fractions:
    delta_vs = []
    for burn_time in burn_time_cases:
        print(f'CASE: {burn_time=} seconds. {f=}')
        g = 9.8 # estimate for entire flight
        m_dry_guess = 5000 # kg
        m_fuel = m_dry_guess / f
        m0 = m_dry_guess + m_fuel # kgs
        m_dot = (m_fuel)/burn_time # kg/se, averaged
        m = lambda t: m0 - m_dot*t
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
        print(f'mass flow avg: {m_dot}')
    else:
        print(f'\n')


    plt.plot(burn_time_cases, delta_vs)
    legends.append(f'burn time vs Δv - f={f}')

plt.legend(legends)
plt.show()
