import numpy as np
import pandas as pd
import gurobipy as gp
from gurobipy import GRB 

#parameter configuration
#unit:kW
P_idle=0.4
P_peak=0.75
eta=1.75

P_grid_max=30

L_rate=4
C_DT=0.32
A_max=3.5e4
T=24
C_RES=28
C_reduce_max=1
C_reduce_min=0
C_BW=2/1e2
C_IW=1.8/3e2
C_GC=24
C_punish=250
redundant_ratio=0.01

#unit:MWh
kk=2.5
delta_W_res_fix=30*kk
W_res_fix=176*kk
W_res_max=206*kk

s_reg=0.987
R_mil=2.92

P_res_max=np.array([0,0,0,0,0,0,10,14,18,20,22,24,25,23,20,17,13,0,0,0,0,0,0,0])*kk
electricity_price=np.array([29,26,23,23,24,25,31,30,32,33,34,35,37,41,44,52,62,50,40,36,38,34,32,30])
reserve_price=np.array([10,8,7,6,7,6,12,6,6,6,7,6,8,10,13,22,31,21,13,10,12,8,10,9])
reg_cap_price=np.array([12,14,11,11,14,24,35,32,26,42,29,31,42,39,33,59,34,38,37,15,37,40,36,22])
reg_mil_price=np.array([2,3,2,3,2,4,6,5,4,3,2,3,2,2,2,2,2,2,1.5,2,2,3,3,2])
predicted_IWs=1e4*np.array([0.75,1.2,1.6,2.2,2.75,3.2,3.4,3.5,3.45,3.2,3.0,2.9,
                                        2.9,3.0,3.2,3.4,3.5,3.4,3.2,2.8,2.2,1.6,1.1,0.7])/1.5
predicted_BWs=1e3*np.array([1.3,2,3.7,4,5.7,5.7,6,6.8,6.8,6,5.7,5.7,5.7,5.7,6,6.8,6.8,6.8,6,5.7,4,3.7,2])*2

alpha=np.array([-0.6,-0.6,-0.8,-0.3,-0.3,-0.2,0,0.25,0.25,0.5,0.5,0.5,0.5,0.5,0.8,0.8,0.7,0.5,0.5,0.5,0.93,0.2,0.1,0])
beta=np.array([-0.25,-0.12,0.2,-0.05,-0.1,-0.15,0.2,-0.45,0.2,-0.1,0,0.1,0,-0.12,0.05,0.1,-0.15,-0.13,0.25,0,-0.2,0.25,0.1,-0.1])
print(alpha.size)
