# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 14:08:16 2026

Tool for processing and plotting Cyclic Voltammetry data

@author: nieminen
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class CVtool:
    def __init__(self, potential, current, Area = None):
        self.metadata = None
        self.E = potential
        self.i = current
        self.Area = Area*1e-8 if Area is not None else None
        
    def plotCV(self, ax = None):
        if ax == None:
            fig, ax = plt.subplots()
        
        current = self.i/self.Area if self.Area is not None else self.i
        current = current*1e9 if self.Area is None else current
        ax.plot(self.E,current)
        
        return ax
    
    @classmethod
    def from_file(cls, filePath, Area = None):
        isCV = False
        
        if not filePath.lower().endswith(".txt"):
            raise ValueError("The file is not a .txt file")

        FileName = None
        InitE = None
        HighE = None
        LowE = None
        initPN = None
        ScanRate = None
        Segment = None
        SInterval = None
        Qtime = None
        
        with open(filePath,encoding='utf-8') as file:
            my_data = file.readlines()
            for line in my_data:
                if line == 'Cyclic Voltammetry\n':
                    isCV = True
                    continue
                elif "File:" in line:
                    FileName = line[line.find(":")+2:-1]
                elif "Init E (V) = " in line:
                    InitE = float(line[line.find("=")+2:-1])
                elif "High E (V)" in line:
                    HighE = float(line[line.find("=")+2:-1])
                # elif "Low Frequency" in line:
                elif "Low E (V) =" in line:
                    LowE = float(line[line.find("=")+2:-1])
                elif "Quiet Time" in line:
                    Qtime = float(line[line.find("=")+2:-1])
                elif "Init P" in line:
                    initPN = line[line.find("=")+2:-1]
                elif "Scan Rate" in line:
                    ScanRate = float(line[line.find("=")+2:-1])
                elif "Segment =" in line:
                    Segment = int(line[line.find("=")+2:-1])
                elif "Sample Interval" in line:
                    SInterval = float(line[line.find("=")+2:-1])
                else:
                    continue
        metadata = {"FileName": None,
                    "InitE": None,
                    "HighE": None,
                    "LowE": None,
                    "initPN": None,
                    "ScanRate": None,
                    "Segment": None,
                    "SInterval": None,
                    "Qtime": None
            }
        
        if isCV == True:
            dataDF = pd.read_csv(filePath,on_bad_lines='skip',names=['Potential','Current'])
            #the dataDF now needs to be trimmed
            #Find the start of the actual data: cell in the Freq column that contains "Potential/V"
            Index = dataDF.index[dataDF.Potential == 'Potential/V']
            #the first index of the data is at rangeind.stop
            dataDF = dataDF.loc[Index[0]+1 : , : ].reset_index(drop=True)
            dataDF = dataDF.apply(pd.to_numeric,errors='coerce').dropna()
            dataObj = cls(np.asarray(dataDF.Potential,dtype=float),np.asarray(dataDF.Current, dtype=float),Area=Area)
            metadata["FileName"] = FileName
            metadata["InitE"] = InitE
            metadata["HighE"] = HighE
            metadata['LowE'] = LowE
            metadata['initPN'] = initPN
            metadata['ScanRate'] = ScanRate
            metadata['Segment'] = Segment
            metadata['SInterval'] = SInterval #Sampling interval
            metadata['Qtime'] = Qtime
            dataObj.metadata = metadata
            return dataObj
        # FileName = None
        # InitE = None
        # HighE = None
        # LowE = None
        # initPN = None
        # ScanRate = None
        # Segment = None
        # SInterval = None
        # Qtime = None
        else:
            raise ValueError("The file is not an EIS data file")

        