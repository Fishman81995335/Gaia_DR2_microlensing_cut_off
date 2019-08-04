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
# Returns CDF with respect to ratio of Theo/exp error
#
#
file_dir = str(input("Input dr2 files directory: "))
sigma_rat = 100
sig_count = .001
to_plot_x = []
to_plot_y = []
count = 0
c = 25.68836

theo = []
err = []
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
      theo = theo + [theo_err/np.sqrt(float(line[1]))]
      err = err + [err_agg]
      count = count + 1

tf = True
print('processing graph')
while sigma_rat > 0:
  if tf and sig_count/count > .00034375:
    print(sig_count/count)
    print(sigma_rat)
    tf = False
  sig_count = 0
  for n in range(count):
    if theo[n]*sigma_rat <= err[n]:
      sig_count = sig_count + 1
  to_plot_x = to_plot_x + [sigma_rat]
  to_plot_y = to_plot_y + [(sig_count/count)]
  if tf:
    sigma_rat = sigma_rat - .5
  else:
    sigma_rat = sigma_rat - .5

print(count)

plt.plot(to_plot_x, to_plot_y)
plt.xlabel("Maximum ratio err/theoretical_err")
plt.ylabel("Proportion of points within ratio")
plt.title("DR2 Sources within Experimental vs Theoretical Errors for " + str(count) + " Sources")
ax = plt.gca()
ax.set_yscale('log')
plt.show()