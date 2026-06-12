# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 13:58:45 2026

@author: nieminen
"""


from EIStools import ImpedanceData, ElementHandler
import tkinter.filedialog
import tkinter as tk
#from tkinter import ttk
#import matplotlib.pyplot as plt
#import matplotlib as mpl
#import numpy as np
import getroot
from drsizecalculator import calculateArea
#from pathlib import Path


#start_folder = r'C:\Users\nieminen\Desktop\Datat verkkolevyltä\SMS-horiba2026'
def Winprompt():
    start_folder = getroot.get_data_root()

    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost',True)
    
    fileNameList = tkinter.filedialog.askopenfilenames(title='Select files for EIS analysis', initialdir=start_folder)
    root.destroy()
    return fileNameList

def Winprompt2():
    # First window
    root = tk.Tk()
    root.geometry("300x150")
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    root.title("Experiment Prompt")
    root.rowconfigure(1, weight=1)
    label = tk.Label(root,text="What is the x-variable in the data set?")
    label.grid(
    row=0,
    column=0,
    columnspan=4,
    pady=20
    )
    xVar = None
    def chooseE():
        nonlocal xVar
        xVar = "E"
        root.destroy()

    def chooseAmp():
        nonlocal xVar
        xVar = "Amp"
        root.destroy()
    button1 = tk.Button(root, command=chooseE, text="Potential")
    #button1.pack(padx=20, pady=10)
    button1.grid(row=1, column=0)
    button2 = tk.Button(root, command=chooseAmp, text="Amplitude")
    #button2.pack(padx=20, pady=10)    #root = tk.Tk()
    button2.grid(row=1,column=1)
   
    root.mainloop()
    return xVar
    # root.withdraw()
    # root.attributes('-topmost', True)
    #frm = ttk.Frame(root, padding=10)
    #frm.grid()
    #frm['width'] = '400p'
    #ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
    #ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
#    xvar = tkinter.messagebox
#    root.destroy()

def isOK():
    root = tk.Tk()
    root.geometry("300x150")
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    root.title("Experiment Prompt")
    root.rowconfigure(1, weight=1)
    label = tk.Label(root,text="Is the x-variable correct")
    label.grid(
    row=0,
    column=0,
    columnspan=4,
    pady=20
    )
    answer = None
    def Yes():
        nonlocal answer
        answer = True
        root.destroy()

    def No():
        nonlocal answer
        answer = False
        root.destroy()
    button1 = tk.Button(root, command=Yes, text="Yes")
    #button1.pack(padx=20, pady=10)
    button1.grid(row=1, column=0)
    button2 = tk.Button(root, command=No, text="No")
    #button2.pack(padx=20, pady=10)    #root = tk.Tk()
    button2.grid(row=1,column=1)
   
    root.mainloop()
    return answer

def SelectAndParse():
    objList = []
    legends = [] #amplitudes
    xvals = [] #amplitudes as floats
    #first file dialog window for selecting which files to read
    fileNameList = Winprompt()
    for file in fileNameList:
        try:
           dataObj = ImpedanceData.from_file(file)
           objList.append(dataObj)
           amplitude = dataObj.metadata['Amp']
           legends.append(str(amplitude)+" mV")
           xvals.append(amplitude)
        except:
             continue
    #Validation part
    muvals = []
    Mvals = []
    #Fitting
    ax = None
    bodeexists = False
    trimmedobjlist = []
    for item in objList:
        trimmedobj = item.select_frequency_range_by_ind(10, len(objList[0])-1)
        trimmedobj.fit_to_Capacitor()
        if ax == None:
            fig, ax = trimmedobj.plot_nyquist()
        else:
            fig, ax = trimmedobj.plot_nyquist(ax=(fig,ax))
        
        if bodeexists == False:
            bodeexists = True
            figbode, axbode = trimmedobj.plot_bode()
        else:
            figbode, axbode = trimmedobj.plot_bode(ax=(figbode,axbode))
        #ax = objList[0].plot_nyquist(ax)
        item.FitParams = trimmedobj.FitParams
        item.linKK_validation()
        muvals.append(item.Validation[0])
        Mvals.append(item.Validation[1])
        trimmedobj.filePath = item.filePath
        trimmedobjlist.append(trimmedobj)
    OK = False
    while OK == False:
        xVar = Winprompt2()
        if xVar == "E":
            for obj in trimmedobjlist:
                legend = str(obj.metadata['InitE'])+" V"
                obj.legend = legend
        elif xVar == "Amp":
            for obj in trimmedobjlist:
                legend = str(obj.metadata['Amp'])+" V"
                obj.legend = legend
        EHobject = ElementHandler(trimmedobjlist)
        EHobject.createX(variable=xVar)
        axelem = EHobject.plotelems()
        OK = isOK()
    #ax.set_xlim(0.125,0.240)
    return objList, trimmedobjlist

if __name__ == "__main__":
    objList, EHobject = SelectAndParse()