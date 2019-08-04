import csv
import matplotlib.pyplot as plt
import os
import numpy as np
import matplotlib.patches as mpatches
#
#
#
# Takes in folder directory of randomly sampled gaia dr2 sources as csv files
# Requires number of observations is in line[1], mean magnitude in line[2] and
# mean mag error in line[3] and flux over error in line[8]
#
#
bashCommand = "find . -name '.DS_Store' -type f -delete"
os.system(bashCommand)
file_dir = str(input("Input dr2 files directory: "))
sigma_rat = 100
sig_count = 1
to_plot_x = []
to_plot_y = []
count = 0
sub_count = 0
colors = []
c = 25.68836

s = []
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
      flux = float(line[2])
      theo_err = abs(f_v_2 - f_v_1)/2
      theo_err_m = np.sqrt(((theo_err**2)*(int(line[1])-1) + (flux**2))/(float(line[1])))
      theo_err = theo_err/(np.sqrt(float(line[1])))
      err_agg = float(line[3])
      rat = err_agg/theo_err
      if err_agg>theo_err_m:
        to_plot_x.append(rat)
        to_plot_y.append(float(line[8]))
        sub_count = sub_count + 1
        print(sub_count)
        colors.append('r')
      elif (count%10000==0):
        to_plot_x.append(rat)
        to_plot_y.append(float(line[8]))
        colors.append('b')
      count = count +1 
          
red = 'Error is Above Microlensing Threshold'
blue = 'Not Microlensing'
red_patch = mpatches.Patch(color='red', label=red)
blue_patch = mpatches.Patch(color='blue', label=blue)

print('processing graph')
print(count)
print(sub_count)
plt.scatter(to_plot_x, to_plot_y,color = colors, s = s)
plt.xlabel("Exp/Theo Error")
plt.ylabel("Flux/Error")
plt.title("Flux/Error vs Exp/Theo Error (1/10000 Non-Microlensed)")
ax = plt.gca()
ax.set_yscale('log')
ax.set_xscale('log')
plt.legend(handles=[red_patch,blue_patch])
plt.show()