# -*- coding: utf-8 -*-
"""
Created on Wed Jul 30 15:15:15 2025

@author: nieminen
"""

# Functions to simply plot CV and EIS data

import pandas as pd
import tkinter.filedialog
import matplotlib as mpl
fileNameList = tkinter.filedialog.askopenfilenames()

exampleFile = fileNameList[0]
startrow = 0
with open(exampleFile, mode='r') as file:
    for num, line in enumerate(file, 1):
        if 'Potential/V, Current/A' in line:
            startrow = num
            break

exampleTab = pd.read_table(exampleFile, sep=',', skiprows=startrow)