"# EISanalysis" 
EIS analysis tool specifically for the CHI Instruments impedance data.

Based on the impedance module:
install from pip: 
conda install impedance
more information on the module:
https://impedancepy.readthedocs.io/en/latest/index.html

EIStools consists of two classes:
ImpedanceData: important properties
Freq: frequency data
Zimag and Zreal: Imaginary and real components of the impedance data
Area: should be given in um2
fitobjRand and fitobjCap: impedancepy objects for Randles and Capacitor circuits, respectively
Zfit: fitted impedance data

ElementHandler: a class that saves a list consisting of several ImpedanceData objecs that have been fitted