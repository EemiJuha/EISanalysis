# -*- coding: utf-8 -*-
"""
Created on Mon Aug  4 17:17:32 2025

@author: eemin
"""

import pandas as pd

def filetoDF(fileName):
    startrow = 0
    isCV = False
    with open(fileName, mode='r') as file:
        for num, line in enumerate(file, 1):
            if 'Potential/V, Current/A' in line:
                startrow = num
                isCV = True
                break
            elif 'Freq/Hz, ' in line:
                startrow = num
                break
    dataFrame = pd.read_table(fileName, sep=',', skiprows=startrow)
    return dataFrame, isCV
