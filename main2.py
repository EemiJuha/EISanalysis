# -*- coding: utf-8 -*-
"""
Created on Wed May  6 18:35:33 2026
New main file... again
@author: nieminen
"""


from ImpedanceClass import ImpedanceData
import tkinter.filedialog
import tkinter as tk

start_folder = r'C:\Users\nieminen\Desktop\Datat verkkolevyltä\SMS-horiba2026'
root = tk.Tk()
root.withdraw()
root.attributes('-topmost',True)

fileNameList = tkinter.filedialog.askopenfilenames(title='Select files for EIS analysis', initialdir=start_folder)
root.destroy()
objList = []
for file in fileNameList:
    try:
       dataObj = ImpedanceData.from_file(file)
       objList.append(dataObj)
    except:
         continue
     