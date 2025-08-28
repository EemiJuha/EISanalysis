# -*- coding: utf-8 -*-
"""
Created on Thu Aug 28 14:07:42 2025

@author: nieminen
"""

from plotmodule import make_panel
from impedance import preprocessing
import tkinter.filedialog
import tkinter as tk

start_folder = r'C:\Users\nieminen\Desktop\Datat verkkolevyltä\SMS-horiba2025'
root = tk.Tk()
root.withdraw()
root.attributes('-topmost',True)

fileNameList = tkinter.filedialog.askopenfilenames(title='Select files for EIS analysis', initialdir=start_folder)
root.destroy()
testEISFile = 'C:/Users/nieminen/Desktop/Datat verkkolevyltä/SMS-horiba2025/20250729-1mMRuHex different droplet sizes/droplet1-fteis0mV.txt'

dictlist = list

#function for deciding whether the inserted file is a readable EIS file
def isEISfile(file):
    answer = False
    if ".txt" in file:
        for line in file:
            if 'A.C. Impedance' in line:
                answer = True
                break
    return answer

for file in fileNameList:
    if isEISfile(file):    
        freqs, Z = preprocessing.readCHInstruments(file)
        data = {
                "f": freqs,
                "Z": Z
                }
        dictlist.append(data)
    else:
        continue
    
