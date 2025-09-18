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

def fitting(dataSetDict):
    freq = dataSetDict["f"]
    Z = dataSetDict["Z"]
    scale = dataSetDict['scale']
    Z = Z/scale
    R0 = float(min(np.real(Z)))
    R1 = (float(max(np.real(Z))-R0))/2
    C1 = 1e-11
    CPEC = 1e-8*scale
    CPEx = 1
    tau = 15
#    RandlesObj = Randles(CPE=False,initial_guess=[R0, R1, Wo1,C1])
    RandlesObjCPE = Randles(CPE=True,initial_guess=[R0, R1, Wo1, tau, CPEC, CPEx])
    CustomCircObj = CustomCircuit(circuit='R0-p(CPE1,R1)',initial_guess=[R0,CPEC,CPEx,R1])
    LB = [0, 0, 0, 0, 0, 0.7]
    UB = [np.inf,np.inf,np.inf,1e3,np.inf,1]
    bounds = (LB,UB)
    UBC = [0,0,0.7,0]
    LBC = [np.inf,np.inf,1,np.inf]
    boundsc = (UBC,LBC)
    mask = (freq <= 1e6)
    for x in range(15):
        fitobj = CustomCircObj.fit(freq[mask],Z[mask],boundsc)
        CustomCircObj.initial_guess = list(fitobj.parameters_)
    return fitobj    
#M, mu, Z_linKK, res_real, res_imag = linKK(freqs, Z, c=0.5, max_M=100, fit_type='complex', add_cap=True)
