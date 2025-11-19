# calculate adiabatic flame tempeature of methane and oxygen
import numpy as np
import pandas as pd
from scipy import interpolate
import matplotlib.pyplot as plt
import scipy as sp

# specific heats in Kj/Kmol K

class CP:
    def __init__(self):

        # calculate specific heat of methane
        df_methane = pd.read_csv('methane_cp.csv')
        ch4_T = df_methane['t'].to_numpy()
        ch4_cp = df_methane['cp'].to_numpy() / 16.04246
        self.temp_cp_ch4 = interpolate.make_splrep(ch4_T, ch4_cp, s=0)

        # calculate specific heat of o2
        df_o2 = pd.read_csv('oxygen_cp.csv')
        o2_t = df_o2['t'].to_numpy()
        o2_cp = df_o2['cp'].to_numpy()
        self.temp_cp_o2 = interpolate.make_splrep(o2_t, o2_cp, s=0)

        # calculate specific heat of co2
        df_co2 = pd.read_csv('co2_cp.csv')
        co2_t = df_co2['t'].to_numpy()
        co2_cp = df_co2['cp'].to_numpy()/44.0095
        self.temp_cp_co2 = interpolate.make_splrep(co2_t, co2_cp, s=0)

        # calculate specific heat of h2o
        df_h2o = pd.read_csv('h2o_cp.csv')
        h2o_t = df_h2o['t'].to_numpy()
        h2o_cp = df_h2o['cp'].to_numpy()
        self.temp_cp_h2o = interpolate.make_splrep(h2o_t, h2o_cp, s=0)


    def ch4(self, T):
        """return the cp of methane"""
        return interpolate.splev(T, self.temp_cp_ch4, der=0)

    def o2(self, T):
        """return the cp of o2"""
        return interpolate.splev(T, self.temp_cp_o2, der=0)
    
    def co2(self, T):
        """return the cp of co2"""
        return interpolate.splev(T, self.temp_cp_co2, der=0)

    def h2o(self, T):
        """return the cp of co2"""
        return interpolate.splev(T, self.temp_cp_h2o, der=0)


cp = CP()


# for 1 kmol of everything (kg/kmol * n kmol)
mass_ch4 = 16.04246     *1.0
mass_o2 = 15.999        *2.0
mass_co2 = 44.0095      *1.0
mass_h2o = 18.01528     *2.0

# kj/mol * 1000 mol/1 kmol * N kmol
H_methane = -74.6*1000.0 * 1.0
H_oxygen = 0.0*1000      * 2.0
H_co2 = -394.39*1000     * 1.0
H_water = -241.8*1000    * 2.0
H_formation = -H_methane - H_oxygen + H_co2 + H_water

def absorbed_energy(T):
    # Integrate cp(T) dT for products from 298 K to T
    H_co2 = mass_co2 * sp.integrate.quad(cp.co2, 298.0, T)[0] # kJ
    H_h2o = mass_h2o * sp.integrate.quad(cp.h2o, 298.0, T)[0] # kJ
    return H_co2 + H_h2o

print(f'H_f: {H_formation}')
F = lambda T: np.abs(H_formation + absorbed_energy(T))**2


res = sp.optimize.minimize(F, 3000.0, method="CG")
print(f'minimization function {'success' if res.fun**2<0.01 else 'failed'} ({res.fun:.2f})\n'
      f'temperature: {res.x} K')

# root solver gets same solution as minimizing the error in the equality
res = sp.optimize.root_scalar(lambda T: H_formation + absorbed_energy(T), bracket=[2000, 5500], method='brentq')
print(res)




