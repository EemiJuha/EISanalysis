# -*- coding: utf-8 -*-
"""
Created on Wed Jul 30 15:15:15 2025

@author: nieminen
"""

# Functions to simply plot CV and EIS data

import pandas as pd
import tkinter.filedialog

import matplotlib.pyplot as plt
#fileNameList = tkinter.filedialog.askopenfilenames()
dummyFile = 'C:/Users/eemin/OneDrive/Tiedostot/Python Scripts/SMS-horiba2025/20250429-CV-measurements-1mMRuHex-again both directions/CVOx200mVs.txt'
exampleFile = dummyFile
startrow = 0
with open(exampleFile, mode='r') as file:
    for num, line in enumerate(file, 1):
        if 'Potential/V, Current/A' in line:
            startrow = num
            break

exampleTab = pd.read_table(exampleFile, sep=',', skiprows=startrow)

figure = plt.subplot()
plt.plot(exampleTab.ilog[:,0],exampleTab.iloc[:,1])

