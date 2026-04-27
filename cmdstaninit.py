# -*- coding: utf-8 -*-
"""
Created on Fri Feb 27 15:02:17 2026
initialization of cmdstan
@author: nieminen
"""

import cmdstanpy
cmdstanpy.install_cmdstan()

from cmdstanpy import set_make_env
set_make_env("mingw32-make.exe")

import os
from cmdstanpy import cmdstan_path, CmdStanModel

bernoulli_stan = os.path.join(cmdstan_path(),'examples','bernoulli','bernoulli.stan')
bernoulli_model = CmdStanModel(stan_file=bernoulli_stan)
bernoulli_model.name
bernoulli_model.stan_file
bernoulli_model.exe_file
bernoulli_model.code()
