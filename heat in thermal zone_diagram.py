# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 17:19:00 2024

@author: hp
"""

import matplotlib.pyplot as plt

# Given data

Qstore_1h = 27.45445243726911
Qscab = 23.010006734482477
Qlcab = 6.282020907
Qsaux = -5.1975752042133685
Qlaux_value = 3.3600000000000003
Qlcab_value = 6.282020907
Ql_total = 9.642020907

# Calculate latent heat
Ql = Qlcab_value + Qlaux_value

# Plotting
labels = ['Qstore_1h', 'Qscab', 'Qlcab', 'Qsaux', 'Qlaux', 'Ql_total']

values = [Qstore_1h, Qscab, Qlcab, Qsaux, Qlaux_value, Ql_total]

plt.bar(labels, values, color=['blue', 'green', 'orange', 'yellow', 'cyan', 'pink'])
plt.xlabel('Sensible and latent heats')
plt.ylabel('Heat in Thermal Zone [kW]')
plt.title('Heat in Thermal Zone')
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
plt.show()