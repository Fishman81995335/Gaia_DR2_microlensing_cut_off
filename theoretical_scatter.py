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
line = np.linspace(3,20,100)
flux_error = []
flux_error_20 = []
flux_error_50 = []
flux_error_80 = []
exp_theo = []
exp_theo_20 = []
exp_theo_50 = []
exp_theo_80 = []
c = 25.68836

print('Calculating...')
test = 100
counter = 0
for el in line:
  z = max([10.**((0.4)*(12 - 15)), 10.**((0.4)*(el - 15))])
  mag_theo_err = (.001*(((0.04895 * z**2) + (1.8633 * z) + 0.0001985)**(1/2)))
  val_1 = el + mag_theo_err
  val_2 = el - mag_theo_err
  f_v_1 = 10**((c-val_1)/2.5)
  f_v_2 = 10**((c-val_2)/2.5)
  flux = 10**((c-el)/2.5)
  theo_err = abs(f_v_2 - f_v_1)/2
  err_20 = np.sqrt(((theo_err**2)*19 + ((flux)**2))/(20))
  err_50 = np.sqrt(((theo_err**2)*49 + ((flux)**2))/(50))
  err_80 = np.sqrt(((theo_err**2)*79 + ((flux)**2))/(80))
  exp_theo_20 = exp_theo_20 + [err_20/theo_err]
  exp_theo_50 = exp_theo_50 + [err_50/theo_err]
  exp_theo_80 = exp_theo_80 + [err_80/theo_err]
  flux_error_20 = flux_error_20 + [flux/err_20]
  flux_error_50 = flux_error_50 + [flux/err_50]
  flux_error_80 = flux_error_80 + [flux/err_80]
  counter = counter+1
  if counter<=test:
    print(el)
    print(flux)
    print(theo_err)
  if counter==test:
    print(exp_theo_20)
    print(flux_error_20)


blue = 'Microlensing 1 of 20 events'
red = 'Microlensing 1 of 50 events'
green = 'Microlensing 1 of 80 events'
blue_patch = mpatches.Patch(color='blue', label=blue)
red_patch = mpatches.Patch(color='red', label=red)
green_patch = mpatches.Patch(color='green', label=green)



print('processing graph')

plt.close()
fig = plt.figure()
tf = True
plt.plot(exp_theo_20, flux_error_20, color = 'b')
plt.plot(exp_theo_50, flux_error_50, color = 'r')
plt.plot(exp_theo_80, flux_error_80, color = 'g')
plt.legend(bbox_transform=plt.gcf().transFigure, bbox_to_anchor = (1,1),handles=[blue_patch, red_patch, green_patch])
plt.title("Theoretical Flux Error Change in Magnitude and N Observations")
plt.ylabel("Flux/Error")
plt.xlabel("Exp/Theo Error")

ax = plt.gca()
#ax.set_yscale('log')
#ax.set_xlim([-.1,1.1])
#ax.set_xscale('log')
plt.show()