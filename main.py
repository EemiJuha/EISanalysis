# -*- coding: utf-8 -*-
"""
Created on Thu Aug 28 14:07:42 2025

@author: nieminen
"""

from plotmodule import make_panel
from impedance import preprocessing
import tkinter.filedialog
import tkinter as tk
import matplotlib.pyplot as plt
import itertools
import os
import numpy as np
import fittingmodule

start_folder = r'C:\Users\nieminen\Desktop\Datat verkkolevyltä\SMS-horiba2025'
root = tk.Tk()
root.withdraw()
root.attributes('-topmost',True)

fileNameList = tkinter.filedialog.askopenfilenames(title='Select files for EIS analysis', initialdir=start_folder)
root.destroy()
testEISFile = 'C:/Users/nieminen/Desktop/Datat verkkolevyltä/SMS-horiba2025/20250729-1mMRuHex different droplet sizes/droplet1-fteis0mV.txt'

dictlist = list()

#function for deciding whether the inserted file is a readable EIS file
def isEISfile(file):
    answer = False
    if ".txt" in file:
        with open(file,'r') as f:
            for line in f:
                if 'A.C. Impedance' in line:
                    answer = True
                    break
    return answer
fig, (ax_nyq, ax_zre, ax_zim, ax_phase) = make_panel()
fig.tight_layout(rect=[0, 0.1, 1, 1])
ax_nyq.set_title('Nyquist')
ax_zre.set_title(r'Bode ($Z_{re}$)')
ax_zim.set_title('Bode ($Z_{im}$)')
ax_phase.set_title('Bode ($\phi$)')
#log scale for the bode plots
ax_zre.set_xscale('log')
ax_zim.set_xscale('log')
ax_phase.set_xscale('log')
colors = plt.cm.tab10.colors
color_cycle = itertools.cycle(colors)
file_colors = {file: next(color_cycle) for file in fileNameList if file.endswith('.txt')}
fitfreq = np.logspace(2, 5, 50)
#plotter that plots the given data into the defined subplots
def plotter(freq,Z):
    Zar = np.array(Z)
    freqsar = np.array(freq)
    ax_nyq.plot(Zar.real,-Zar.imag, label=fileName, color=file_colors[file])
    ax_zre.plot(freqsar,Zar.real,label=fileName, color=file_colors[file])
    ax_zim.plot(freqsar,Zar.imag,label=fileName, color=file_colors[file])
    ax_phase.plot(freqsar,np.angle(Zar, deg=True),label=fileName, color=file_colors[file])

for file in fileNameList:
    if isEISfile(file):
        fileName = os.path.basename(file)
        freqs, Z = preprocessing.readCHInstruments(file)
        plotter(freqs,Z)
        # Zar = np.array(Z)
        # freqsar = np.array(freqs)
        # ax_nyq.plot(Zar.real,-Zar.imag, label=fileName, color=file_colors[file])
        # ax_zre.plot(freqsar,Zar.real,label=fileName, color=file_colors[file])
        # ax_zim.plot(freqsar,Zar.imag,label=fileName, color=file_colors[file])
        # ax_phase.plot(freqsar,np.angle(Zar, deg=True),label=fileName, color=file_colors[file])
        freqs, Z = preprocessing.readCHInstruments(file)
        data = {
                'file': file,
                "f": freqs,
                "Z": Z
                }
        fitObj = fittingmodule.fitting(data)
        fitObj.predict(fitfreq)
        dictlist.append(data)
    else:
        continue
    
