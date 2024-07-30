# -*- coding: utf-8 -*-
"""

@author: Basia
"""
import ipywidgets as widgets
from ipywidgets import interact
import ipywidgets as wd
import matplotlib.pyplot as plt
import cool_new as cc
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
latent_heat_person = 20    # W / person #data from Christian Ghiaus paper
load_m2 = 10        # W/m2
solar_m2 = 150      # W/m2 of window area
ACH = 1             # Air Chnages per Hour
U_wall = 0.4        # W/K, overall heat transfer coeff. walls
U_window = 3.5      # W/K, overall heat transfer coeff. windows


θo, φo = -3.7, 0.7    # outdoor temperature & relative humidity
θI, φI = 24, 0.55    # indoor temperature & relative humidity
wo = psy.w(θo, φo)
wI = psy.w(θI, φI)

floor_area = 1250   #m2
surface_floor = 2 * (length + width) * height + floor_area
surface_wall = 0.9 * surface_floor
surface_window = surface_floor - surface_wall

UA = U_wall * surface_wall + U_window * surface_window
mi = ACH * surface_floor * height / 3600 * ρ

Qsaux = 6124 #kW
Qlaux = 7440  #kW
Qscab = -60509 #kW
Qlcab = -39537 #kW

#In supermarket θs 
θS = θI - 15        # °C supply air temperature
m = Qsaux/ c / (θI - θS) 
#m = 5
print(f'QsTZ = {Qsaux:.0f} W, QlTZ = {Qlaux:.0f} W')
print(f'UA = {UA:.0f} W/K, mi = {mi:.2f} kg/s,\
      Qsa = {Qscab:.0f} W, Qla = {Qlcab:.0f} W')
print(f'm = {m:.3f} kg/s')

Kθ, Kw = 1e10, 0     # Kw can be 0
β = 0.7              # by-pass factor
m, mo = 1.601, 0.1601    # kg/s, mass flow rate: supply & outdoor (fresh) air
#θo, φo = 0.108, 0.8   # outdoor conditions
θIsp, φIsp = 24, 0.55  # set point for indoor condition

#mi = 1.5           # kg/s, mass flow rate of infiltration air
mi = 0.13792        # Data from expert kg/s
UA = 675.           # W/K, overall heat coefficient of the building

parameters = m, mo, β, Kθ, Kw
inputs = θo, φo, θI, wI, θIsp, φIsp, mi, UA, Qscab, Qlcab, Qsaux, Qlaux



cool5 = cc.MxCcRhTzBl(parameters, inputs)
x = cool5.solve_lin(20.0)
β, Kw = 0.7, 1e10
cool5.actual[[2, 4]] = β, Kw
wd.interact(cool5.CAV_wd, θo=(-5, 15), φo=(0.4, 1), θ3=(20, 28), φ3=(0.4, 1), θIsp=(20, 28), φIsp=(0.4, 1),
           mi=(0.06, 3, 0.1), UA=(500, 800, 10), Qsaux=(0, 50_000, 400), Qlaux=(0, 10_000, 200), Qscab=(-70_000, 60_000, 500), Qlcab=(-40_000, 20_000, 500));


