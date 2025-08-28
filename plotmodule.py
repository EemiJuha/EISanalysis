# -*- coding: utf-8 -*-
"""
Created on Thu Aug 28 13:51:15 2025
Module for plotting
@author: nieminen
"""

import matplotlib.pyplot as plt

def make_panel():
    fig, axs = plt.subplots(2,2,figsize=(12,9), constrained_layout=True)
    ax_nyq, ax_zre, ax_zim, ax_phase = axs.ravel()
    
    ax_nyq.set_title("Nyquist")
    ax_zre.set_title(r'Bode ($Z_{re}$)')
    ax_zim.set_title("Bode (Zim)")
    ax_phase.set_title("Bode (Phase)")

    return fig, (ax_nyq, ax_zre, ax_zim, ax_phase)
