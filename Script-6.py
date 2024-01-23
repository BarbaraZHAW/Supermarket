# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 14:16:17 2023

@author: Basia
"""

import ipywidgets as wd
import matplotlib.pyplot as plt
import cool_1 as cc
import psychro as psy
import pandas as pd

plt.rcParams["figure.figsize"] = (10, 7.7)
font = {'size': 16}
plt.rc('font', **font)

# constants
c = 1.013e3         # J/kg K, air specific heat
l = 2496e3          # J/kg, latent heat
ρ = 1.293           # kg/m3, density

# Building dimensions SUPERMARKET
length = 41.66   # m
width = 30     # m
height = 3    # m
persons = 48  # m

sens_heat_person = 50     # W / person
latent_heat_person = 20    # W / person
load_m2 = 10        # W/m2
solar_m2 = 150      # W/m2 of window area
ACH = 1             # Air Chnages per Hour
U_wall = 0.4        # W/K, overall heat transfer coeff. walls
U_window = 3.5      # W/K, overall heat transfer coeff. windows

θo, φo = 0.108, 0.8    # outdoor temperature & relative humidity
θI, φI = 19, 0.5    # indoor temperature & relative humidity
wo = psy.w(θo, φo)
wI = psy.w(θI, φI)

floor_area = 1250   #m2
surface_floor = 2 * (length + width) * height + floor_area
surface_wall = 0.9 * surface_floor
surface_window = surface_floor - surface_wall

UA = U_wall * surface_wall + U_window * surface_window
mi = ACH * surface_floor * height / 3600 * ρ

#Manuel's formulas inputs #kW
Qbuild = -14.791736296296296  #kW
Qinf = -4.905838907917072 
Qlight = 12.5
Qcust = 3.36 
Qintern = 2 
QM1_storage = 4.080815094339623 
QL1_storage = 4.271142857142857 
Q_mobile = 2.148192063 
Q_M1VC = 11.77539325 
Q_L1VC = 7.016484381 
Q_M1VO = 0  # for big supermarket = 0

Qscab = 23.010006734482477  #kW
Qlcab = 6.282020907  #kW
Qsaux = -5.1975752042133685  #kW
Qlaux = 3.3600000000000003  #kW


#In supermarket θs 
θS = θI - 15        # °C supply air temperature
m = Qsaux/ c / (θI - θS) 
#m = 5
print(f'QsTZ = {Qsaux:.0f} W, QlTZ = {Qlaux:.0f} W')
print(f'UA = {UA:.0f} W/K, mi = {mi:.2f} kg/s,\
      Qsa = {Qscab:.0f} W, Qla = {Qlcab:.0f} W')
print(f'm = {m:.3f} kg/s')

Kθ, Kw = 1e10, 0     # Kw can be 0
β = 0.2              # by-pass factor
m, mo = 3.5, 1.      # kg/s, mass flow rate: supply & outdoor (fresh) air
θo, φo = 0.108, 0.8   # outdoor conditions
θIsp, φIsp = 19., 0.5  # set point for indoor condition

#mi = 1.5           # kg/s, mass flow rate of infiltration air
mi = 0.13792        # Data from expert
UA = 675.            # W/K, overall heat coefficient of the building

parameters = m, mo, β, Kθ, Kw
inputs = θo, φo, θI, wI, θIsp, φIsp, mi, UA, Qscab, Qlcab, Qsaux, Qlaux



cool5 = cc.MxCcRhTzBl(parameters, inputs)
x = cool5.solve_lin(20.0)
β, Kw = 0.2, 1e10
cool5.actual[[2, 4]] = β, Kw
wd.interact(cool5.CAV_wd, θo=(0, 15), φo=(0.4, 1), θI=(19, 33), wI=(0.5, 1), θIsp=(20, 28), φIsp=(0.4, 1),
           mi=(0.5, 3, 0.1), UA=(500, 800, 10), Qsaux=(0, 50_000, 400), Qlaux=(0, 10_000, 200), Qscab=(0, 60_000, 500), Qlcab=(0, 20_000, 500));


#wd.interact(cool5.CAV_wd, θo=(0, 15), φo=(0.4, 1), θI=(19, 33), wI=(0.5, 1), θIsp=(20, 28), φIsp=(0.4, 1),
#            mi=(0.5, 3, 0.1), UA=(500, 800, 10), Qsaux=(0, 50_000, 25000), Qlaux=(0, 10_000, 3360), Qscab=(0, 60_000, 23000), Qlcab=(0, 20_000, 6280));


#To implement ambient Temperature from excel (winter + summer)

def read_temperature_data(file_path, sheet_name='Weather_Data-Zurich'):
    try:
        # Read the Excel file into a pandas DataFrame
        df = pd.read_excel(file_path, sheet_name=sheet_name)

        # Assuming the column with temperature data is named 'Temperature'
        temperatures = df['T_amb_mean [°C]'].tolist()

        return temperatures

    except Exception as e:
        print(f"Error reading temperature data from Excel: {e}")
        return None

# Example usage:
file_path = r'C:\Users\hp\Documents\Project 1\Weather_data.xlsx'
temperature_data = read_temperature_data(file_path)

if temperature_data:
    print("Temperature data:", temperature_data)
else:
    print("Failed to read temperature data.")
θo = temperature_data

