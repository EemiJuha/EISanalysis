#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 22 11:49:53 2026

@author: eeminieminen
"""

from pathlib import Path

POSSIBLE_ROOTS = [
    Path(r'C:\Users\nieminen\Desktop\Datat verkkolevyltä\SMS-horiba2026'),
    Path("/Users/eeminieminen/Desktop/SMSHoriba" )
]

def get_data_root():
    for path in POSSIBLE_ROOTS:
        if path.exists():
            return path

    raise FileNotFoundError("No valid EIS data root folder found")