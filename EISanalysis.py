# -*- coding: utf-8 -*-
"""


@author: nieminen
"""

from impedance import preprocessing
from impedance.validation import linKK
import tkinter.filedialog
import matplotlib.pyplot as plt
import numpy as np

from impedance.models.circuits import CustomCircuit
import tkinter.filedialog
import tkinter as tk
import sys

def square_data_limits(ax, pad=0.05):
    # Make x and y spans equal by expanding the smaller span.
    ax.relim()
    ax.autoscale_view()

    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()

    xspan = xmax - xmin
    yspan = ymax - ymin
    span = max(xspan, yspan)

    # center current limits
    xmid = 0.5 * (xmin + xmax)
    ymid = 0.5 * (ymin + ymax)

    # add padding
    span *= (1 + pad)

    ax.set_xlim(0, xmid + span/2)
    ax.set_ylim(0, ymid + span/2)

sys.path.append('../../../')


#fileNameList = tkinter.filedialog.askopenfilenames()

start_folder = r'C:\Users\nieminen\Desktop\Datat verkkolevyltä\SMS-horiba2025'
root = tk.Tk()
root.withdraw()
root.update()
root.focus_force()
root.lift()
root.attributes('-topmost',True)

fileNameList = tkinter.filedialog.askopenfilenames(title='Select files for EIS analysis', parent=root, initialdir=start_folder)
root.destroy()
#testFile = "C:/Users/nieminen/Documents/MATLAB/20251107-3MLiCl-MoS2 on gold/eis100mV.txt"
testFile = fileNameList[0]

freq, Z = preprocessing.readCHInstruments(testFile)
mask = 7
freq = freq[0:-mask]
Z = Z[0:-mask]
#making the linear KK analysis?
M, mu, Z_linKK, res_real, res_imag = linKK(freq,Z,c=.5, max_M=100, fit_type='complex',add_cap=True)

from impedance.visualization import plot_nyquist, plot_residuals
from matplotlib.ticker import MaxNLocator


fig = plt.figure(figsize=(5,8))
fig.suptitle(fileNameList[0])
gs = fig.add_gridspec(2, 1, height_ratios=[3.5, 1.5])
ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])

# plot original data
plot_nyquist(Z/1000000000, fmt='s', ax=ax1)
# plot measurement model
plot_nyquist(Z_linKK/1000000000, fmt='-', scale=1e3, units='G\Omega', ax=ax1)
plot_residuals(ax2, freq, res_real, res_imag, y_limits=(-2,2))

fig.canvas.draw()
ax1.set_aspect('equal',adjustable='box')
square_data_limits(ax1,pad=0.03)
ax1.xaxis.set_major_locator(MaxNLocator(nbins=5))
ax1.legend(['Data', 'Lin-KK model'], loc=2, fontsize=12)

ax1.relim()
ax1.autoscale_view()
ax1.margins(0.1)

plt.show()

# plot only the Residuals, also print out the 
fig2 = plt.figure(figsize=(5,8))
ax3 = fig2.add_subplot()

plot_residuals(ax3, freq, res_real, res_imag, y_limits=(-2,2))
ax3.relim()
ax3.margins(0.1)
plt.show()