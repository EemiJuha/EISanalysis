# -*- coding: utf-8 -*-
"""
Created on Wed Jul 30 15:15:15 2025

@author: nieminen
"""

# Functions to plot EIS data (for now) and doing the lin kk validation

import pandas as pd
import tkinter as tk
import tkinter.filedialog
from filetodf import filetoDF
import matplotlib.pyplot as plt
import os
from impedance.validation import linKK
import itertools


#GUI for selecting the files to be plotted
def bring_to_front():
    root.attributes('-topmost', True)
    root.attributes('-topmost', False)
root = tk.Tk()
root.withdraw()
root.attributes('-topmost',True)
start_folder = r'C:\Users\nieminen\Desktop\Datat verkkolevyltä\SMS-horiba2025'
fileNameList = tkinter.filedialog.askopenfilenames(title='Select Files For Plotting', initialdir=start_folder)
root.destroy()

#To be removed
dummyFile = 'C:/Users/eemin/OneDrive/Tiedostot/Python Scripts/SMS-horiba2025/20250429-CV-measurements-1mMRuHex-again both directions/CVOx200mVs.txt'
exampleFile = dummyFile
#initiation of the list of dataframes
DFlist = list()

#initializing the figures for the plots
plt.close('all')
#LaTeX interpreter
plt.rcParams['text.usetex'] = True #plt.figure(1)
#figure with subplots creation
fig, axs = plt.subplots(2,2,figsize=[12,9],constrained_layout=True)

ax_nyq, ax_zre, ax_zim, ax_phase = axs.ravel()
#titles
ax_nyq.set_title('Nyquist')
ax_zre.set_title(r'Bode ($Z_{re}$)')
ax_zim.set_title('Bode (Zim)')
ax_phase.set_title('Bode (phase)')
#log scale for the bode plots
ax_zre.set_xscale('log')
ax_zim.set_xscale('log')
ax_phase.set_xscale('log')

#manual colormap
colors = plt.cm.tab10.colors
color_cycle = itertools.cycle(colors)
file_colors = {file: next(color_cycle) for file in fileNameList if file.endswith('.txt')}
                          
for file in fileNameList:
    if '.txt' in file:
        df, isCV = filetoDF(file)
        fileName = os.path.basename(file)
        if not isCV:
            plt.subplot(2,2,1) #Nyquist
            ax_nyq.plot(df.iloc[:,1],-df.iloc[:,2],label=fileName, color=file_colors[file])
            ax_zre.plot(df.iloc[:,0],df.iloc[:,1],label=fileName, color=file_colors[file])
            ax_zim.plot(df.iloc[:,0],df.iloc[:,2],label=fileName, color=file_colors[file])
            ax_phase.plot(df.iloc[:,0],df.iloc[:,4],label=fileName, color=file_colors[file])
        DFlist.append(df)
        DFlist.append(isCV)
    else:
        continue

handles, labels = [],[]

for ax in (ax_nyq, ax_zre, ax_zim, ax_phase):
    h, l = ax.get_legend_handles_labels()
    handles.extend(h)
    labels.extend(l)

from collections import OrderedDict
by_label = OrderedDict(zip(labels, handles))

fig.legend(
    by_label.values(), by_label.keys(),
    loc='lower center',
    ncol=3,           # spread across columns
    bbox_to_anchor=(0.5, -0.0)  # centered below subplots
)

fig.tight_layout(rect=[0, 0.08, 1, 1])  # leave space at bottom for legend

plt.show()

#exampleTab, isCV = filetoDF(dummyFile)
#figure = plt.subplot()
#plt.plot(exampleTab.iloc[:,0],exampleTab.iloc[:,1])

