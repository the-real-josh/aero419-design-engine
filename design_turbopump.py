import numpy as np
sqrt = np.sqrt


from design_tanks import kg_meth, kg_o2
from calculate_flight import burn_time

m_dot_meth = kg_meth/burn_time
m_dot_o2 = kg_o2/burn_time

max_tip_speed = 655 # m/s

p_tank = 1.1e5
p_comb = 4.4e7
p_ratio = p_comb/p_tank
# use two individual turbopumps

# design of lox pump
rho_o2 = 1142 #Kg/m3
w_dot_o2 = m_dot_o2*(p_comb-p_tank)/rho_o2
u_lox = sqrt(2*(p_comb - p_tank)/rho_o2)


# design of methane pump
rho_methane = 422 # kg/m3
w_dot_meth = m_dot_meth*(p_comb - p_tank)/rho_methane
u_meth = sqrt(2*(p_comb - p_tank)/rho_methane)

total_work = w_dot_o2 + w_dot_meth

if __name__ == '__main__':
    print(f'mass flow rate of methane: {m_dot_meth} kg/sec\n'
          f'mass flow rate of oxygen: {m_dot_o2} kg/sec\n'
          f'work required: [METH]{w_dot_meth:.2e} + [LOX]{w_dot_o2:.2e} = {total_work:.2e}\n'
          f'Required tip speed for [METH]{u_meth:.2f}, [LOX]{u_lox:.2f}')
