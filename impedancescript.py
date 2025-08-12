# -*- coding: utf-8 -*-
"""
Created on Tue Aug  5 14:51:49 2025

@author: nieminen
"""

#The actual eis analysis tool

from impedance import preprocessing
from impedance.visualization import plot_nyquist
from impedance.models.circuits import CustomCircuit, Randles
import tkinter.filedialog
import tkinter as tk
import matplotlib.pyplot as plt

start_folder = r'C:\Users\nieminen\Desktop\Datat verkkolevyltä\SMS-horiba2025'
root = tk.Tk()
root.withdraw()
root.attributes('-topmost',True)

fileNameList = tkinter.filedialog.askopenfilenames(title='Select files for EIS analysis', initialdir=start_folder)
root.destroy()
testEISFile = 'C:/Users/nieminen/Desktop/Datat verkkolevyltä/SMS-horiba2025/20250729-1mMRuHex different droplet sizes/droplet1-fteis0mV.txt'
R0 = 0.01
R1 = 0.01
Wo1 = 0.003
C1 = 0.001
CPEC = 0.001
CPEx = 1

RandlesObj = Randles(CPE=False,initial_guess=[R0, R1, Wo1,C1])
RandlesObjCPE = Randles(CPE=True,initial_guess=[R0, R1, Wo1, CPEC, CPEx])
freqs, Z = preprocessing.readCHInstruments(testEISFile)

#fitting for CPE Randles circuit

fitobj = RandlesObjCPE.fit()