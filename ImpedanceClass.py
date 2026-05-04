# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 16:51:09 2026

@author: nieminen
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from impedance.validation import linKK
from impedance.models.circuits import Randles, CustomCircuit
from matplotlib.ticker import EngFormatter, LogLocator

DataFile = "droplet1-fteis400mV.txt"
WrongDataFile = 'd1CV.txt'

class ImpedanceData:
    def __init__(self, Freq, Zreal, Zimag, Area=None):
        self.Freq = Freq
        self.Zreal = Zreal #Ohm
        self.Zimag = Zimag #Ohm
        if Area:
            self.Area = Area*(1e-4)**2 #cm2
        else:
            self.Area = None
        self.fitobjRand = None
        self.fitobjCap = None
        self.Zfit = None
        self.FitParams = None
        self.Validation = None

    def __len__(self):
        return len(self.Freq)
    
    def __iter__(self):
        for f, zr, zi in zip(self.Freq, self.Zreal, self.Zimag):
            yield f, zr, zi
    
    def _find_nearest_index(self,value):
        return np.abs(self.Freq-value).argmin()

    
    def select_frequency_range(self, f_min, f_max):
        idx_min = self._find_nearest_index(f_min)
        idx_max = self._find_nearest_index(f_max)
        
        if idx_min > idx_max:
            idx_max, idx_min = idx_min, idx_max
        
        return ImpedanceData(self.Freq[idx_min : idx_max + 1], self.Zreal[idx_min:idx_max+1],self.Zimag[idx_min:idx_max + 1])
    
    def plot_nyquist(self, ax = None,plotfits = True):
        if ax is None:
            fig, ax = plt.subplots()
            
        
        ax.plot(self.Zreal/1e6,-self.Zimag/1e6, marker = 'o')
        ax.set_title('Nyquist-plot')
        ax.set_xlabel(r'$Z_{real}\ ($M$\Omega)$')
        ax.set_ylabel(r'-$Z_{imag}\ ($M$\Omega)$')            
    
        if plotfits and isinstance(self.Zfit, np.ndarray):
            ax.plot(np.real(self.Zfit)/1e6,-np.imag(self.Zfit)/1e6)
    def plot_bode(self, ax = None, plotfits = True):
        if ax is None:
            fig, ax = plt.subplots(2,2, figsize=(9,6),constrained_layout=True)
            
        ax[0,0].loglog(self.Freq,self.Zreal)
        ax[0,1].loglog(self.Freq,-self.Zimag)
        ax[1,0].semilogx(self.Freq,self.phase)
        ax[1,1].loglog(self.Freq,self.magnitude)
        ax[0,0].set_title(r'Bode, $Z^\prime$') 
        ax[0,1].set_title(r'Bode, $-Z^{\prime \prime}$') 
        ax[1,0].set_title(r'Bode, $\phi$') 
        ax[1,1].set_title(r'Bode, $|Z|$') 
#        ax[0,0].yscale()
        for axi in ax:
            for axj in axi:
                axj.set_xlabel(r'$f$ (Hz)')
                axj.grid(True,which="both")
                axj.set_xscale('log')
                if axj is not ax[1,0]:
                    axj.yaxis.set_major_formatter(EngFormatter(r'$\Omega$'))
                    axj.yaxis.set_minor_formatter(EngFormatter(r'$\Omega$'))
                    axj.tick_params(axis='both',which='minor',labelsize=0)
        
        #ax[0:,0:].set_xlabel(r'$f$ (Hz)')
        #ax[0:,0:].set_ylabel(r'($\Omega$)')
        ax[1,0].set_ylabel(r'$\phi$ ($^\circ$)')          
        ax[1,0].set_yscale('linear')
        if plotfits and isinstance(self.Zfit,np.ndarray):
            ax[0,0].plot(self.Freq,np.real(self.Zfit))
            ax[0,1].plot(self.Freq,-np.imag(self.Zfit))
            ax[1,0].plot(self.Freq,np.angle(self.Zfit,deg=True))
            ax[1,1].plot(self.Freq,np.abs(self.Zfit))
            
        
        
    def linKK_validation(self, fittype = 'complex'):
        M, mu, Z_linKK, res_real, res_imag = linKK(self.Freq,self.impedance,c=.5, max_M=100, fit_type=fittype,add_cap=True)
        self.Validation = [M, mu, Z_linKK, res_real, res_imag]

    def fit_to_Randles(self,InitGuess=[.01, .005, .001, 200, .1, .9], CPE=True):
        if not CPE:
            InitGuess.pop(5)
        InitGuess[0] = min(self.Zreal)
        #Scaling should be considered
        ScaledImpedance = self.impedance/1000000
        RandObj = Randles(initial_guess= InitGuess,CPE=CPE)
        RandObj.fit(self.Freq,ScaledImpedance)
        self.fitobjRand = RandObj
        self.Zfit = RandObj.predict(self.Freq)*1000000
        self.FitParams = RandObj.parameters_
        
        
    def fit_to_Capacitor(self,InitGuess=[.01, .1, .9],CPE=True):
        if not CPE:
            InitGuess.pop(2)
            circuit = 'R_0-C_1'
        else:
            circuit = 'R_0-CPE_1'
        ScaledImpedance = self.impedance/1000000
        CapObj = CustomCircuit(initial_guess=[.1, .1, 0.9], circuit=circuit)
        CapObj.fit(self.Freq,ScaledImpedance)
        self.fitobjCap = CapObj
        self.Zfit = CapObj.predict(self.Freq)*1000000
        self.FitParams = CapObj.parameters_
        
    @property
    def Zdensity(self):
        if not self.Area:
            raise ValueError('Area not defined')
        return self.impedance/self.Area
    
    @property
    def impedance(self):
        return self.Zreal + 1j*self.Zimag
    
    @property
    def phase(self):
        return np.angle(self.impedance, deg=True)
    
    @property
    def magnitude(self):
        return np.abs(self.impedance)
        

    @classmethod
    def from_file(cls,FilePath,Area=None):
        isEIS = False
        
        if not FilePath.lower().endswith(".txt"):
            raise ValueError("The file is not a .txt file")

        with open(FilePath,encoding='utf-8') as file:
            my_data = file.readlines()
            for line in my_data:
                if line == 'A.C. Impedance\n':
                    isEIS = True
                    break
                else:
                    continue
        
        if isEIS:
            dataDF = pd.read_csv(FilePath,on_bad_lines='skip',names=['Freq','Zreal','Zimag','Zabs','Phase'])
            #the dataDF now needs to be trimmed
            #Find the start of the actual data: cell in the Freq column that contains "Freq/Hz"
            Index = dataDF.index[dataDF.Freq == 'Freq/Hz']
            #the first index of the data is at rangeind.stop
            dataDF = dataDF.loc[Index[0]+1 : , : ].reset_index(drop=True)
            dataDF = dataDF.apply(pd.to_numeric,errors='coerce').dropna()
            return cls(dataDF.Freq,dataDF.Zreal,dataDF.Zimag,Area=Area)
        else:
            raise ValueError("The file is not an EIS data file")
            
dataObj = ImpedanceData.from_file(DataFile)
dataObj.plot_bode()

dataObj.fit_to_Capacitor()
fitobj = dataObj.fitobjCap
dataObj.plot_bode()
dataObj.plot_nyquist()