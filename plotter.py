# -*- coding: utf-8 -*-
"""
Created on Wed Jul 30 15:15:15 2025

@author: nieminen
"""

# Functions to simply plot CV and EIS data

import pandas as pd
import tkinter as tk
import tkinter.filedialog
from filetodf import filetoDF
import matplotlib.pyplot as plt

def bring_to_front():
    root.attributes('-topmost', True)
    root.attributes('-topmost', False)

root = tk.Tk()
root.withdraw()
root.attributes('-topmost',True)
start_folder = r'C:\Users\nieminen\Desktop\Datat verkkolevyltä\SMS-horiba2025'
fileNameList = tkinter.filedialog.askopenfilenames(title='Select Files For Plotting', initialdir=start_folder)
root.destroy()
dummyFile = 'C:/Users/eemin/OneDrive/Tiedostot/Python Scripts/SMS-horiba2025/20250429-CV-measurements-1mMRuHex-again both directions/CVOx200mVs.txt'
exampleFile = dummyFile
DFlist = list()
for file in fileNameList:
    if '.txt' in file:
        df, isCV = filetoDF(file)
        DFlist.append(df)
        DFlist.append(isCV)
    else:
        continue

#exampleTab, isCV = filetoDF(dummyFile)
#figure = plt.subplot()
#plt.plot(exampleTab.iloc[:,0],exampleTab.iloc[:,1])

