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
import matplotlib.pyplot as plt


#fileNameList = tkinter.filedialog.askopenfilenames()
testEISFile = 'C:/Users/nieminen/Desktop/Datat verkkolevyltä/SMS-horiba2025/20250729-1mMRuHex different droplet sizes/droplet1-fteis0mV.txt'
R0 = 0.01
R1 = 0.01
Wo1 = 0.003
C1 = 0.001
CPEC = 0.001
CPEx = 1

RandlesObj = Randles(initial_guess=[R0, R1, Wo1,C1])
RandlesObjCPE = Randles(initial_guess=[R0, R1, Wo1, CPEC, CPEx])
freqs, Z = preprocessing.readCHInstruments(testEISFile)