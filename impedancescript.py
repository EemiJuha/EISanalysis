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
import numpy as np
from impedance.validation import linKK




R0 = 0.01
R1 = 0.01
Wo1 = 0.003

def fitting(axs, dataSetDict):
    freq = dataSetDict["f"]
    Z = dataSetDict["Z"]
    R0 = float(min(np.real(Z)))
    R1 = 1000
    C1 = 1e-11
    CPEC = 1e-11
    CPEx = 1
#    RandlesObj = Randles(CPE=False,initial_guess=[R0, R1, Wo1,C1])
    RandlesObjCPE = Randles(CPE=True,initial_guess=[R0, R1, Wo1, CPEC, CPEx])
    LB = [0, 0, 0,]
    UB = []
    fitobj = RandlesObjCPE.fit(freq,Z,)    
#M, mu, Z_linKK, res_real, res_imag = linKK(freqs, Z, c=0.5, max_M=100, fit_type='complex', add_cap=True)

fitobj = RandlesObjCPE.fit()