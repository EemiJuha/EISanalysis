# -*- coding: utf-8 -*-
"""
Created on Wed May  6 18:35:33 2026
New main file... again
@author: nieminen
"""


from ImpedanceClass import ImpedanceData, ElementHandler
import tkinter.filedialog
import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import getroot
from pathlib import Path


#start_folder = r'C:\Users\nieminen\Desktop\Datat verkkolevyltä\SMS-horiba2026'
start_folder = getroot.get_data_root()
root = tk.Tk()
root.withdraw()
root.attributes('-topmost',True)

fileNameList = tkinter.filedialog.askopenfilenames(title='Select files for EIS analysis', initialdir=start_folder)
root.destroy()
objList = []
legends = [] #amplitudes
xvals = [] #amplitudes as floats
for file in fileNameList:
    try:
       dataObj = ImpedanceData.from_file(file)
       objList.append(dataObj)
       amplitude = dataObj.metadata['Amp']
       legends.append(str(amplitude)+" mV")
       xvals.append(amplitude)
    except:
         continue

muvals = []
Mvals = []
#for item in objList:
#    item.linKK_validation()
#    muvals.append(item.Validation[1])
#    Mvals.append(item.Validation[0])
    

# ax  = objList[0].plot_linKK()
# Validationlist = objList[0].Validation

# fig, ax = plt.subplots(2,1,figsize=(11,15),constrained_layout=True)
# ax[0].plot(xvals,muvals)
# ax[1].plot(xvals,Mvals)
# fig.suptitle(legends[0])

#Fitting
ax = None
bodeexists = False
for item in objList:
    trimmedobj = item.select_frequency_range_by_ind(10, len(objList[0])-1)
    trimmedobj.fit_to_Capacitor()
    if ax == None:
        ax = trimmedobj.plot_nyquist()
    else:
        ax = trimmedobj.plot_nyquist(ax=ax)
    
    if bodeexists == False:
        bodeexists = True
        axbode = trimmedobj.plot_bode()
    else:
        axbode = trimmedobj.plot_bode(ax=axbode)
    #ax = objList[0].plot_nyquist(ax)
    item.FitParams = trimmedobj.FitParams

EHobject = ElementHandler(objList)
EHobject.createX(variable='Amp')
EHobject.plotelems()
ax.set_xlim(0.125,0.240)