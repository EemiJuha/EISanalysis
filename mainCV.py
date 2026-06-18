# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 15:12:03 2026
main script for the CV plotting
@author: nieminen
"""

from CVtools import CVtool
import tkinter.filedialog
import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import getroot
from pathlib import Path
from drsizecalculator import calculateArea



#start_folder = r'C:\Users\nieminen\Desktop\Datat verkkolevyltä\SMS-horiba2026'
start_folder = getroot.get_data_root()
root = tk.Tk()
root.withdraw()
root.attributes('-topmost',True)

fileNameList = tkinter.filedialog.askopenfilenames(title='Select files for CV analysis', initialdir=start_folder)
root.destroy()
objList = []
legends = [] #amplitudes
xvals = [] #amplitudes as floats
for file in fileNameList:
    try:
       if objList == []:
           dataObj = CVtool.from_file(file)
           dataObj.updateArea()
       else:
           dataObj = CVtool.from_file(file)
           dataObj.Area = objList[0].Area
       objList.append(dataObj)
    except:
         continue
axes = None
for obj in objList:
    if axes == None:
        fig, axes = obj.plotCV()
    else:
        obj.ax = axes
        obj.fig = fig
        fig, axes = obj.plotCV()  
        
objList[len(objList)-1].ax.legend()
#objList[0].updateLegend("n/a", legon=False)
#objList[len(objList)-1].saveAs()
