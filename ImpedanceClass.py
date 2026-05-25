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
#import math 
#DataFile = "droplet1-fteis400mV.txt"
#WrongDataFile = 'd1CV.txt'

class ElementHandler:
    def __init__(self,ImpDataList):
        self.ImpDataList = ImpDataList
        self.parameterlist = []
        self.x =[]
        self.xlabel = None
        self.parameterdict = None
        self.parameterdf = pd.DataFrame()
        self.collectparameters()
        
    def appendtolist(self,NewList):
        self.ImpDataList.append(NewList)
    
    def collectparameters(self):
        nrelem = len(self.ImpDataList[0].FitParams)
        elemlist = list(range(1,nrelem+1))
        eldict = {}
        elitems = []
        for x in elemlist:
            item = "El"+str(x)
            elitems.append(item)
            eldict.update({item: []})
        i = 0
        while i<len(elemlist):
            elemlist[i]=elemlist[i]-1
            i += 1
            
        for el,x in zip(elitems,elemlist):
            for exp  in self.ImpDataList:
                parameterlist = exp.FitParams
                eldict[el].append(parameterlist[x])
                
        for item in eldict:
            eldict[item] = np.array(eldict[item])
        for item in self.ImpDataList:
            parameterlist = item.FitParams
            self.parameterlist.append(parameterlist)
            
        self.parameterdict = eldict
        self.parameterdf = pd.DataFrame(eldict)
            
    def createX(self,variable="E"):
        '''
        At the moment variable can be "E" or "Amp"
        '''
        Xvar = []
        self.xlabel = variable
        match variable:
            case "E":
                for item in self.ImpDataList:
                    metadata = item.metadata
                    Xvar.append(metadata['InitE'])
            case "Amp":
                for item in self.ImpDataList:
                    metadata = item.metadata
                    Xvar.append(metadata['Amp'])
        self.parameterdict.update({variable: np.array(Xvar)})
        self.parameterdf = pd.DataFrame(self.parameterdict)
    
    def plotelems(self):
        #first, create a subplot that has as many axes as there are plottable elements
        if self.xlabel is None:
            raise ValueError("Cannot plot, X array is missing")
        nrel  = len(self.parameterlist[0])
        cols = nrel//2 + nrel%2
        rows = 2
        fig, ax = plt.subplots(rows,cols)
        
        rowlist = range(rows)
        collist = range(cols)
        axlist = []
        for r in rowlist:
            for c in collist:
                axlist.append(ax[r,c])
        axi = 0
        for item in self.parameterdict:
            if item == self.xlabel:
                continue
            
            self.parameterdf.plot(ax=axlist[axi],x=self.xlabel,y=item)
            axi +=1

            
        
#    def plotelements(self)

class ImpedanceData:
    def __init__(self, Freq, Zreal, Zimag, Validation=None, Area=None):
        if not isinstance(Freq, np.ndarray) and not isinstance(Zreal, np.ndarray) and not isinstance(Zimag, np.ndarray):
            raise ValueError("Some of the data is not an array")
        if not (len(Freq)==len(Zreal)==len(Zimag)):
            raise ValueError("The arrays are not the same size")
        self.Freq = Freq
        self.Zreal = Zreal #Ohm
        self.Zimag = Zimag #Ohm
        # Notice the general syntax, good to know and intuititives
        # ... = Value if condition else alternativevalue
        # expected unit um^2 -> needs to be converted to cm^2
        self.Area = Area*(1e-4)**2 if Area is not None else None
        #if Area:
        #    self.Area = Area*(1e-4)**2 #cm2
        #else:
        #    self.Area = None
        self.fitobjRand = None
        self.fitobjCap = None
        self.Zfit = None
        self.FitParams = None
        self.Validation = Validation
        self.metadata = {
            'FileName': None,
            'InitE': None,
            'MaxF': None,
            'MinF': None,
            'Mode': None,
            'Amp': None,
            'Qtime': None            
             }
        self.plotcolor = None

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
        
        return ImpedanceData(self.Freq[idx_min : idx_max + 1], self.Zreal[idx_min:idx_max+1],self.Zimag[idx_min:idx_max + 1],self.Validation)
    
    def select_frequency_range_by_ind(self, minind, maxind):
        if minind > maxind:
            minind, maxind = maxind, minind
            
        return ImpedanceData((self.Freq[minind:maxind]), self.Zreal[minind:maxind], self.Zimag[minind:maxind])
    
    def plot_linKK(self, ax = None):
        if not self.Validation:
            raise ValueError('LinKK analysis has not been made')
        if ax is None:
            fig, ax = plt.subplots(2,1,figsize=(11,15),constrained_layout=True)
        
        ax[0].set_title('Nyquist')
        self.plot_nyquist(ax[0],plotfits=False)
        ax[0].plot(np.real(self.Validation[2])/1e6, -np.imag(self.Validation[2])/1e6)
        ax[1].set_title('Residuals')
        ax[1].plot(self.Freq,self.Validation[3])
        ax[1].plot(self.Freq,self.Validation[4])
        ax[1].set_xlabel(r'$f\ $(Hz)')
        ax[1].set_ylabel(r'$\Delta\ $(%)')
        #ax[0].set_aspect('equal')
        ##set_position([left,bottom,width,height])
        ax[0].set_position([0.3,0.3,0.4,0.4])
        ax[1].set_position([0.1,0.1,0.8,0.15])
        ax[1].set_ylim(-2,2)
        return ax
            
        
    def plot_nyquist(self, ax = None,plotfits = True):
        if ax is None:
            fig, ax = plt.subplots()
        Zreal = self.Zreal/1e6
        Zimag = self.Zimag/1e6
        
        if self.plotcolor is None:
            pl = ax.scatter(Zreal,-Zimag, marker = 'o')
            self.plotcolor = pl.get_facecolor()
        else:
            ax.scatter(Zreal,-Zimag, marker = 'o', color=self.plotcolor)
        ax.set_title('Nyquist-plot')
        ax.set_xlabel(r'$Z_{real}\ ($M$\Omega)$')
        ax.set_ylabel(r'-$Z_{imag}\ ($M$\Omega)$')            
    
        if plotfits and isinstance(self.Zfit, np.ndarray):
            ax.plot(np.real(self.Zfit)/1e6,-np.imag(self.Zfit)/1e6)
        
        #setting up limits of the axes
        #maxval = max(self.Zimag + self.Zreal)
        x_min = 0
        y_min = 0
        x_max = Zreal.max()
        y_max = Zimag.max()
        if x_max > y_max:
            y_max = x_max
            
        else:
            x_max = y_max
            
        pad = 0.05*x_max
        ax.set_xlim(x_min,x_max+pad)
        ax.set_ylim(y_min,y_max+pad)
        
        return ax
        
    def plot_bode(self, ax = None, plotfits = True):
        if ax is None:
            fig, ax = plt.subplots(2,2, figsize=(9,6),constrained_layout=True)
        if self.plotcolor is None:
            pl = ax[0,0].loglog(self.Freq,self.Zreal,linestyle='',marker='o')
        else:
            pl = ax[0,0].loglog(self.Freq,self.Zreal,linestyle='',marker='o',color=self.plotcolor)
        ax[0,1].loglog(self.Freq,-self.Zimag,linestyle='',marker='o',color=pl[0].get_color())
        ax[1,0].semilogx(self.Freq,self.phase,linestyle='',marker='o',color=pl[0].get_color())
        ax[1,1].loglog(self.Freq,self.magnitude,linestyle='',marker='o',color=pl[0].get_color())
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
            ax[0,0].plot(self.Freq,np.real(self.Zfit),color=pl[0].get_color())
            ax[0,1].plot(self.Freq,-np.imag(self.Zfit),color=pl[0].get_color())
            ax[1,0].plot(self.Freq,np.angle(self.Zfit,deg=True),color=pl[0].get_color())
            ax[1,1].plot(self.Freq,np.abs(self.Zfit),color=pl[0].get_color())
            
        return ax
        
    def linKK_validation(self, fittype = 'complex'):
        M, mu, Z_linKK, res_real, res_imag = linKK(self.Freq,self.impedance,c=.5, max_M=100, fit_type=fittype,add_cap=True)
        self.Validation = [M, mu, Z_linKK, res_real, res_imag]

    #Fitting methods to Randles and a capacitor
    def fit_to_Randles(self,InitGuess=[.01, .005, .001, 200, .1, .9], CPE=True):
        if not CPE:
            InitGuess.pop(5)
        InitGuess[0] = min(self.Zreal)
        #Scaling should be considered
        Scale = 1e6
        ScaledImpedance = self.impedance/Scale
        RandObj = Randles(initial_guess= InitGuess,CPE=CPE)
        RandObj.fit(self.Freq,ScaledImpedance)
        self.fitobjRand = RandObj
        self.Zfit = RandObj.predict(self.Freq)*Scale
        fitparams = RandObj.parameters_
        fitparams[0] = fitparams[0]*Scale
        fitparams[1] = fitparams[1]*Scale
        fitparams[2] = fitparams[2]*Scale
        fitparams[4] = fitparams[4]/Scale
        
        self.FitParams = RandObj.parameters_
        
        
    def fit_to_Capacitor(self,InitGuess=[.1, .0001, .9],CPE=True):
        if not CPE:
            InitGuess.pop(2)
            circuit = 'R_0-C_1'
        else:
            circuit = 'R_0-CPE_1'
        Scale = 1e6
        lower = [1e-12, 1e-12, 0.5]
        upper = [1e9,   1e3,   1]
        ScaledImpedance = self.impedance/Scale
        CapObj = CustomCircuit(initial_guess=[.1, .1, 0.9], circuit=circuit)
        CapObj.fit(self.Freq,ScaledImpedance,global_opt = False, bounds=(lower,upper))
        
        # n=0
        # while n < 10:
        #     newinit = CapObj.parameters_
        #     CapObj = CustomCircuit(initial_guess=newinit, circuit = circuit)
        #     CapObj.fit(self.Freq,ScaledImpedance,global_opt = True)
        #     n += 1
            
            
        self.fitobjCap = CapObj #this will not be needed probably
        
        
        
        self.Zfit = CapObj.predict(self.Freq)*Scale
        fitparams = CapObj.parameters_
        fitparams[0] = fitparams[0]*Scale
        fitparams[1] = fitparams[1]/Scale
        self.FitParams = fitparams
        
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

        FileName = None
        InitE = None
        MaxF = None
        MinF = None
        mode = None
        Amp = None
        Qtime = None
        
        with open(FilePath,encoding='utf-8') as file:
            my_data = file.readlines()
            for line in my_data:
                if line == 'A.C. Impedance\n':
                    isEIS = True
                    continue
                elif "File:" in line:
                    FileName = line[line.find(":")+2:-1]
                elif "Init E (V) = " in line:
                    InitE = float(line[line.find("=")+2:-1])
                elif "High Frequency" in line:
                    MaxF = float(line[line.find("=")+2:-1])
                # elif "Low Frequency" in line:
                    MinF = float(line[line.find("=")+2:-1])
                elif "Amplitude (V) =" in line:
                    Amp = float(line[line.find("=")+2:-1])
                elif "Quiet Time" in line:
                    Qtime = float(line[line.find("=")+2:-1])
                
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
            dataObj = cls(np.asarray(dataDF.Freq,dtype=float),np.asarray(dataDF.Zreal, dtype=float),np.asarray(dataDF.Zimag,dtype=float),Area=Area)
            dataObj.metadata["FileName"] = FileName
            dataObj.metadata["InitE"] = InitE
            dataObj.metadata["MaxF"] = MaxF
            dataObj.metadata['MinF'] = MinF
            dataObj.metadata['Mode'] = mode
            dataObj.metadata['Amp'] = Amp
            dataObj.metadata['Qtime'] = Qtime
            return dataObj
        else:
            raise ValueError("The file is not an EIS data file")
