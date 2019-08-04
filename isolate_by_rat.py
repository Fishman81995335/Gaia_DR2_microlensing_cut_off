import csv
import os
import numpy as np
#
#
#
# Takes in folder directory of randomly sampled gaia dr2 sources as csv files
# Takes in float value of theoretical/exp ratio max value
# Requires number of observations is in line[1], mean magnitude in line[2] and
# mean mag error in line[3]
# Returns text file of source_id's of sources that are outside ratio value
#
file_dir = str(input("Input dr2 files directory: "))
rat_lim = float(input("Input max ratio of theoretical/exp error: "))
to_write = []
c = 25.68836
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
      theo_err = abs(f_v_2 - f_v_1)/(2*np.sqrt(float(line[1])))
      err_agg = float(line[3])
      rat = err_agg/theo_err
      if rat > rat_lim:
        print(str(line[0]))