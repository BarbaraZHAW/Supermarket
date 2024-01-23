import matplotlib.pyplot as plt

# Given data
Qbuild = -14.791736296296296
Qinf = -4.905838907917072
Qcust = 3.3600000000000003
Qlight = 12.5
Qintern = 2
QM1_storage = 4.080815094339623
QL1_storage = 4.271142857142857
Q_mobile_value = 2.148192059
Q_M1VC_value = 11.77539325
Q_L1VC_value = 7.016484381
Q_M1VO_value = 0
Qstore_1h = 27.45445243726911
Q_mobile = 2.148192059
Qscab = 23.010006734482477
Qlcab = 6.282020907
Qsaux = -5.1975752042133685
Qlaux_value = 3.3600000000000003
Qlcab_value = 6.282020907
Ql_total = 9.642020907

# Calculate latent heat
Ql = Qlcab_value + Qlaux_value

# Plotting
labels = ['Qbuild', 'Qinf', 'Qcust', 'Qlight', 'Qintern', 'QM1_storage', 'QL1_storage',
          'Q_mobile', 'Q_M1VC', 'Q_L1VC', 'Q_M1VO', 'Qstore_1h', 'Qscab', 'Qlcab', 'Qsaux', 'Qlaux', 'Ql_total']

values = [Qbuild, Qinf, Qcust, Qlight, Qintern, QM1_storage, QL1_storage,
          Q_mobile_value, Q_M1VC_value, Q_L1VC_value, Q_M1VO_value, Qstore_1h, Qscab, Qlcab, Qsaux, Qlaux_value, Ql_total]

plt.bar(labels, values, color=['blue', 'green', 'orange', 'yellow', 'cyan', 'lightblue', 'lightgreen',
                               'lightcoral', 'darkgreen', 'darkorange', 'indianred', 'lightgrey', 'skyblue', 'lightpink', 'coral', 'lavender', 'pink'])
plt.xlabel('Heat Sources and Sinks')
plt.ylabel('Heat in Thermal Zone [kW]')
plt.title('Heat Flows Including Latent Heat')
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
plt.show()