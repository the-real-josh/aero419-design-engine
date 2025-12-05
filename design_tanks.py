import calculate_Isp

# physics be like
rho_meth = 422.6 # kg/m3
rho_o2 = 1.141e3 # kg/m3
phi = calculate_Isp.phi
from calculate_flight import m_propellant 


mol_meth = 1*phi    # get 1 mol methane times eq ratio
mol_o2 = 2          # 2 mol o2


# get the stoich mass of each
#           mm (kg/kmol)     kmol        
kg_meth =   16.04       *  mol_meth
kg_o2 =     31.998    *  mol_o2

# the mass fraction of o2 and methane
kg_total = kg_meth + kg_o2
f_o2 = kg_o2/kg_total
f_meth = kg_meth/kg_total


kg_meth = m_propellant * f_meth
kg_o2 = m_propellant * f_o2

vol_meth = kg_meth/rho_meth
vol_o2 = kg_o2/rho_o2

print(f'volume of methane tank: {vol_meth} m3\n'
    f'volume of o2 tank: {vol_o2} m3\n\n'
    f'mole ratio: {mol_meth} moles of methane for every {mol_o2} of oxygen\n'
    f'mass ratio: {kg_meth/kg_o2} kg of methane for every 1 kg of oxygen\n'
    f'{f_o2}% oxygen, and {f_meth}% methane\n'
    f'{kg_meth} kg of methane and {kg_o2} kg of oxygen\n')

# came up with a nice-shaped rocket here https://www.desmos.com/calculator/qpvwabeppx
# radius of tanks - 1.2 m
# height of tanks - 50 m
