import numpy as np
import pandas as pd
import gurobipy as gp
from gurobipy import GRB 

#parameter configuration
#unit:kW
P_idle=0.4
P_peak=0.75
eta=1.75

P_grid_max=50

L_rate=4
C_DT=0.32
A_max=3.5e4
T=24
C_reduce_max=1
C_reduce_min=0
C_BW=2
C_IW=1.8
C_GC=100
C_punish=250
redundant_ratio=0.1

#unit:MWh
delta_W_res_fix=30
W_res_fix=150
W_res_max=173

P_res_max=np.array([0,0,0,0,0,0,10,14,18,20,22,24,25,23,20,17,13,0,0,0,0,0,0,0])
electricity_price=1e3*np.array([0.35,0.35,0.35,0.35,0.35,0.35,0.35,0.35,0.85,0.85,0.85,0.35,0.35,
                            0.85,0.85,0.85,0.85,0.85,0.85,1.05,1.05,0.85,0.35,0.35])
predicted_IWs=1e4*np.array([0.75,1.2,1.6,2.2,2.75,3.2,3.4,3.5,3.45,3.2,3.0,2.9,
                                        2.9,3.0,3.2,3.4,3.5,3.4,3.2,2.8,2.2,1.6,1.1,0.7])/2
predicted_BWs=1e3*np.array([1.3,2,3.7,4,5.7,5.7,6,6.8,6.8,6,5.7,5.7,5.7,5.7,6,6.8,6.8,6.8,6,5.7,4,3.7,2])