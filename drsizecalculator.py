# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 13:33:05 2026
a short method for reading the area text file
format of the text  file should be:
1x1    points
0.5x0.5    points
0.1x0.1    points


@author: nieminen
"""
import tkinter as tk
import tkinter.filedialog
import pandas as pd
import getroot
#start_folder = r'C:\Users\nieminen\Desktop\Datat verkkolevyltä\SMS-horiba2026'

def calculateArea(startFolder = None):
    if startFolder == None:
        start_folder = getroot.get_data_root()
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost',True)
    else:
        start_folder = startFolder
            
    
    fileName = tkinter.filedialog.askopenfilename(title='Select the txt file containing the area measurements', initialdir=start_folder)
    
    with open(fileName, "r", encoding="utf-8") as file:
        #print(repr(file.readline()))
        df = pd.read_csv(file, header=None, sep=r"\s+", names=["meshsize","No. points"])
    
    reference = pd.DataFrame({'ref':[121,441,10201]})
    reference = 100/reference
    areas = pd.DataFrame(df["No. points"]*reference["ref"], columns=["area in um2"])
    newdf = df.join(areas)
    meanarea = newdf["area in um2"].mean()
    return meanarea

if __name__== "__main__":
    area = calculateArea()