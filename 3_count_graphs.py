import csv
import matplotlib.pyplot as plt
import os
import numpy as np
#
#
#
# Takes in folder directory of randomly sampled gaia dr2 sources as csv files
# Requires number of observations is in line[1], mean magnitude in line[2] and
# mean mag error in line[3]
# Returns 3 Graphs of counts
#
#
file_dir = str(input("Input dr2 files directory: "))
sigma_rat = 100
sig_count = .0001
to_plot_total = []
to_plot_var = []
to_plot_spec_var = []
to_plot_x = []
count = 0
c = 25.68836

theo = []
err = []
var = []
spec_var = []
for file_name in os.listdir(file_dir):
  print('processing file ' + str(file_name) + ' \U0001f44d')
  line_num = 0
  file_path = file_dir + '/' + file_name
  with open(file_path, 'r') as fil:
    fil_reader = csv.reader(fil)
    for line in fil_reader:
      if line_num == 0:
        line_num = line_num + 1
        continue
      z = max([10.**((0.4)*(12 - 15)), 10.**((0.4)*(float(line[4]) - 15))])
      mag_theo_err = (.001*(((0.04895 * z**2) + (1.8633 * z) + 0.0001985)**(1/2)))
      val_1 = float(line[4]) + mag_theo_err
      val_2 = float(line[4]) - mag_theo_err
      f_v_1 = 10**((c-val_1)/2.5)
      f_v_2 = 10**((c-val_2)/2.5)
      theo_err = abs(f_v_2 - f_v_1)/2
      err_agg = float(line[3])
      theo.append(theo_err/np.sqrt(float(line[1])))
      err.append(err_agg)
      if str(line[5]) == "VARIABLE":
        var.append(True)
      else:
        var.append(False)

      if str(line[6]) != '':
        spec_var.append(True)
      else:
        spec_var.append(False)
      count = count + 1
      if(count%1000000 == 0):
        print(count)

tf = True
print('processing graph')
while sigma_rat > 0:
  if tf and sig_count/count > .00034375:
    print(sig_count/count)
    print(sigma_rat)
    tf = False
  sig_count = 0
  var_count = 0
  spec_var_count = 0
  for n in range(count):
    if theo[n]*sigma_rat <= err[n]:
      sig_count = sig_count + 1
      if var[n]:
        var_count = var_count + 1
      if spec_var[n]:
        spec_var_count = spec_var_count + 1
  to_plot_x = to_plot_x + [sigma_rat]
  to_plot_total = to_plot_total + [sig_count]
  to_plot_var = to_plot_var + [var_count]
  to_plot_spec_var = to_plot_spec_var + [spec_var_count]
  sigma_rat = sigma_rat - .5

print(count)

plt.close()
fig = plt.figure()

ax1 = plt.subplot(311)
ax1.plot(to_plot_x, to_plot_total)
ax1.set_ylabel("Points within ratio")
ax1.set_title("Gaia Magnitude Error vs Theoretical")

ax2 = plt.subplot(312)
ax2.plot(to_plot_x, to_plot_var, 'b')
ax2.plot(to_plot_x, to_plot_spec_var, 'r')
ax2.set_ylim([0,25])
ax3 = plt.subplot(313)
ax3.plot(to_plot_x, to_plot_spec_var)
ax3.set_xlabel("maximum ratio err/theoretical_err")
ax3.plot(to_plot_x, to_plot_total, 'g')
ax3.plot(to_plot_x, to_plot_var, 'b')
ax3.plot(to_plot_x, to_plot_spec_var, 'r')
ax3.set_yscale('log')

plt.show()