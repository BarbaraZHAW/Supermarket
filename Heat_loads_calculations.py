# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 13:01:07 2024

@author: hp
"""

import ipywidgets as wd
import matplotlib.pyplot as plt
import cool_1 as cc
import psychro as psy
import pandas as pd

θo, φo = 0.108, 0.8    # outdoor temperature & relative humidity
θI, φI = 19, 0.5       # indoor temperature & relative humidity
v = 15                 # m3/h per customer
n = 48                 # total amount of customers per h
rho = 2.404130497      # density of air in our case kg/m3
cpair = 1012.62486     # heat capacity air

#QHvac
# gives QHvac values depending on θo (Tamb) [kW]
def QHvac(θo, v, n, rho, cpair, θI):
    if 19 <= θo <= 24:
        QHvac = 0
        #print("QHvac = 0")
        print("QHvac =", QHvac)
    else:
        QHvac = v * n * rho * cpair * (θo - θI) * (1 / 3600) * (1 / 1000)
        print("QHvac =", QHvac)
    return QHvac
#display results in console
result = QHvac(θo, v, n, rho, cpair, θI)

#Store
Qd_hs = 21.14 #kW
Qd_cs = 8.61  #kW
#θo, φo = 5, 0.8
def Qbuild(Qd_hs, Qd_cs, θo):
    if θo < 19:
        Qbuild = (Qd_hs / (19-(-8))) * (θo - 19)
    elif 19 <= θo <= 24:
        Qbuild = 0
        
    elif θo > 24:
        Qbuild = (Qd_cs / (35-24)) * (θo - 24)    
    return Qbuild
result = Qbuild(Qd_hs, Qd_cs, θo)
print("Qbuild =", result)

#Infiltration
#n = 48           # number of customers per h
v_inf = 8         # infiltration volume per customer m3/Person
rho = 2.404130497 # density of air in our case kg/m3
cp = 1012.62486   # heat capacity air
def Qinf(n, v_inf, θI, θo, rho, cp):
    Qinf = n * v_inf * rho * cp * (θo - θI) * (1/3600) * (1/1000)  # kW
    return Qinf
result = Qinf(n, v_inf, θI, θo, rho, cp)
print("Qinf =", result)

#Customers
q_cust = 70/1000  # heat input /Person kW
 
def Qcust(n, q_cust):
    Qcust = n * q_cust  # kW
    return Qcust
result = Qcust(n, q_cust)
print("Qcust =", result)

#Light
A = 1250      #S area of shop m2
q_ligh = 10   # specific heat capacity of lighting [W/m2]
def Qlight(A, q_ligh):
    Qlight = A * q_ligh * (1/1000)  # kW
    return Qlight
result = Qlight(A, q_ligh)
print("Qlight =", result)

#Internal heat load

nload = 1      # load profile for internal heat loads % 
q_intern = 2   # max. heat capacity of the internal heat loads [kW]
def Qintern(nload, q_intern):
    Qintern = nload * q_intern  # kW
    return Qintern 
result = Qintern(nload, q_intern)
print("Qintern =", result)

#Waste heat from cooling / freezing storage
EER_M1 = 3.71  #average for winter
EER_L1 = 1.75  #average for winter 
QM1_storage_m = 8.036  #kW
QL1_storage_m = 6.795  #kW
QM1_cond = QM1_storage_m + QM1_storage_m/EER_M1 #kW
QL1_cond = QL1_storage_m + QL1_storage_m/EER_L1  #kW
QM1_storage = QM1_cond * 0.4           #for load profile 40%  
QL1_storage = QL1_cond * 0.4           #for load profile 40%
def QM1_storage(EER_M1, QM1_storage_m, QM1_cond):
    QM1_storage = QM1_cond * 0.4  # kW
    return QM1_storage 
result = QM1_storage(EER_M1, QM1_storage_m, QM1_cond)
print("QM1_storage =", result)

def QL1_storage(EER_L1, QL1_storage_m, QL1_cond):
    QL1_storage = QL1_cond * 0.4   # kW
    return QL1_storage 
result = QL1_storage(EER_L1, QL1_storage_m, QL1_cond)
print("QL1_storage =", result)

#Mobile cabinets
hTEC_real = 0.165245543 #taken from excel, no parameters enaugh 
n_mob = 13
Q_mobile = hTEC_real * n_mob #kW
def Q_mobile(hTEC_real, n_mob):
    Q_mobile = hTEC_real * n_mob  # kW
    return Q_mobile 
result = Q_mobile(hTEC_real, n_mob)
print("Q_mobile =", result)

#Heat Flow cabinets M1VC

Q_M1VC = 11.77539325 #kW
result = Q_M1VC
print("Q_M1VC =", result)

#Heat Flow cabinets L1VC

Q_L1VC = 7.016484381 #kW
result = Q_L1VC
print("Q_L1VC =", result)

#Heat Flow cabinets M1VO

Q_M1VO = 0      #For Big Supermarket type 0
result = Q_M1VO
print("Q_M1VO =", result)


#General Thermal energy balance

def Qstore_1h(Qbuild, Qinf, Qcust, Qlight, Qintern, QM1_storage, QL1_storage, Q_mobile, Q_M1VC, Q_L1VC, Q_M1VO):
    Qstore_1h = Qbuild + Qinf + Qcust + Qlight + Qintern + QM1_storage + QL1_storage + Q_mobile + Q_M1VC + Q_L1VC + Q_M1VO # kW
    return Qstore_1h
result = Qstore_1h(Qbuild(Qd_hs, Qd_cs, θo), Qinf(n, v_inf, θI, θo, rho, cp), Qcust(n, q_cust), 
                   Qlight(A, q_ligh), Qintern(nload, q_intern), QM1_storage(EER_M1, QM1_storage_m, QM1_cond), 
                   QL1_storage(EER_L1, QL1_storage_m, QL1_cond), Q_mobile(hTEC_real, n_mob), Q_M1VC, Q_L1VC, Q_M1VO)
print("Qstore_1h =", result)




#Qstore_1h() = Qscab + Qlcab + Qsaux + Qlaux
#Qlcab + Qlaux => mout in dehumidifier 
QM1_storage_value = QM1_storage(EER_M1, QM1_storage_m, QM1_cond)
QL1_storage_value = QL1_storage(EER_L1, QL1_storage_m, QL1_cond)
Q_M1VC_value = Q_M1VC
Q_L1VC_value = Q_L1VC
Q_M1VO_value = Q_M1VO
Q_mobile_value = Q_mobile(hTEC_real, n_mob)
Qbuild_value = Qbuild(Qd_hs, Qd_cs, θo)
Qinf_value = Qinf(n, v_inf, θI, θo, rho, cp)
Qintern_value = Qintern(nload, q_intern)
Qcust_value = Qcust(n, q_cust)
Qlight_value = Qlight(A, q_ligh)
# Calculations for supermarket model cool_1
Qscab = QM1_storage_value + QL1_storage_value + 0.7 * Q_M1VC_value + 0.7 * Q_L1VC_value + 0.7 * Q_M1VO_value + 0.7 * Q_mobile_value
def Qscab(QM1_storage_value, QL1_storage_value, Q_M1VC_value, Q_L1VC_value, Q_M1VO_value, Q_mobile_value):
    Qscab = QM1_storage_value + QL1_storage_value + 0.7 * Q_M1VC_value + 0.7 * Q_L1VC_value + 0.7 * Q_M1VO_value + 0.7 * Q_mobile_value
    return Qscab
result = Qscab(QM1_storage_value, QL1_storage_value, Q_M1VC_value, Q_L1VC_value, Q_M1VO_value, Q_mobile_value)
print("Qscab =", result)

#Qlcab = 0.3 * Qmobile + 0.3 * Qm1vc + 0.3 * Ql1vc + 0.3 * Qm1vo
Qlcab = 0.3 * Q_mobile_value + 0.3 * Q_M1VC_value + 0.3 * Q_L1VC_value + 0.3 * Q_M1VO_value
def Qlcab(Q_mobile_value, Q_M1VC_value, Q_L1VC_value, Q_M1VO_value):
    Qlcab = 0.3 * Q_mobile_value + 0.3 * Q_M1VC_value + 0.3 * Q_L1VC_value + 0.3 * Q_M1VO_value
    return Qlcab
result = Qlcab(Q_mobile_value, Q_M1VC_value, Q_L1VC_value, Q_M1VO_value)
print("Qlcab =", result)

#Qsaux = Qbuild + Qinf + Qlight + Qintern
Qsaux = Qbuild_value + Qinf_value + Qlight_value + Qintern_value
def Qsaux(Qbuild_value, Qinf_value, Qlight_value, Qintern_value):
    Qsaux = Qbuild_value + Qinf_value + Qlight_value + Qintern_value
    return Qsaux
result = Qsaux(Qbuild_value, Qinf_value, Qlight_value, Qintern_value)
print("Qsaux =", result)

#Qlaux
Qlaux = Qcust_value
def Qlaux(Qcust_value):
    Qlaux = Qcust_value
    return Qlaux
result = Qlaux(Qcust_value)
print("Qlaux =", result)

Qlaux_value = Qlaux(Qcust_value)
Qlcab_value = Qlcab(Q_mobile_value, Q_M1VC_value, Q_L1VC_value, Q_M1VO_value)

#Ql total latent heat
Ql = Qlaux_value + Qlcab_value
def Ql(Qlaux_value, Qlcab_value):
    Ql = Qlaux_value + Qlcab_value
    return Ql
result = Ql(Qlaux_value, Qlcab_value)
print ("Ql =", result)

