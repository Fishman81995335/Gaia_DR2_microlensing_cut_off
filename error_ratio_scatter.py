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
var = []
spec_var = []
count = 0
color = []
c = 25.68836
var_c = 0
spec_var_c = 0
reg_c = 0
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
      theo_err = (abs(f_v_2 - f_v_1)/2)
      err_agg = float(line[3])
      rat = err_agg/theo_err
      if str(line[5]) != "VARIABLE":
        if reg_c%100 == 0:
          color.append('g')
          s.append(1)
          to_plot_x.append(rat)
          to_plot_y.append(float(line[8]))
        reg_c = reg_c + 1
      else:
        if str(line[6]) != '': 
#        spec_var = spec_var + [False]
#        var = var + [False]
#          spec_var = spec_var + [False]
#          var = var + [True]
          if spec_var_c%100 == 0:
            color.append('b')
            s.append(5)
            to_plot_x.append(rat)
            to_plot_y.append(float(line[8]))
          spec_var_c = spec_var_c + 1
        else:
#          spec_var = spec_var + [True]
#          var = var + [True]
          if var_c%100 == 0:
            color.append('r')
            s.append(5)
            to_plot_x.append(rat)
            to_plot_y.append(float(line[8]))
          var_c = var_c + 1
      count = count+1
      if(count%1000000 == 0):
        print(count)
      
print(reg_c)
print(var_c)
print(spec_var_c)
          
red = 'In Light Curves and has Classifier'
blue = 'In Light Curves, has no Classifier'
green = 'Not in Light Curves'
red_patch = mpatches.Patch(color='red', label=red)
blue_patch = mpatches.Patch(color='blue', label=blue)
green_patch = mpatches.Patch(color='green', label=green)   

print('processing graph')
print(count)
plt.scatter(to_plot_x, to_plot_y,color = color, s = s)
plt.xlabel("Exp/Theo Error")
plt.ylabel("Flux/Error")
plt.title("Flux/Error vs Exp/Theo Error")
ax = plt.gca()
ax.set_yscale('log')
ax.set_xscale('log')
plt.legend(handles=[red_patch,blue_patch,green_patch])
plt.show()