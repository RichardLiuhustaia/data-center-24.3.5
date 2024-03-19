import numpy as np
import gurobipy as gp
from gurobipy import GRB
from parameters import *
import matplotlib.pyplot as plt

TD=4
model=gp.Model()
#variable declaration
A_BW_t=model.addVars(24,lb=0,ub=A_max,vtype=GRB.INTEGER,name='A_BW_t')
A_IW_t=model.addVars(24,lb=0,ub=A_max,vtype=GRB.INTEGER,name='A_IW_t')
A_R_t=model.addVars(24,lb=0,ub=A_max,vtype=GRB.INTEGER,name='A_R_t')
L_BW_t=model.addVars(24,lb=0,ub=GRB.INFINITY,vtype=GRB.CONTINUOUS,name='L_BW_t')
L_IW_t=model.addVars(24,lb=0,ub=GRB.INFINITY,vtype=GRB.CONTINUOUS,name='L_IW_t')
P_res_t=model.addVars(24,lb=0,ub=GRB.INFINITY,vtype=GRB.CONTINUOUS,name='P_res_t')
P_d_t=model.addVars(24,lb=-GRB.INFINITY,ub=GRB.INFINITY,vtype=GRB.CONTINUOUS,name='P_grid_t')
W_res=model.addVar(lb=0,ub=GRB.INFINITY,vtype=GRB.CONTINUOUS,name='W_res')
delta_W_res=model.addVar(lb=-GRB.INFINITY,ub=GRB.INFINITY,vtype=GRB.CONTINUOUS,name='delta_W_res')

#constraints
#power balance constraint:DC's power supply comes from utility grid and PV generation
model.addConstrs(1/1000*(P_idle+0.75*P_peak)*(A_BW_t[i]+A_IW_t[i])+1/1000*P_idle*A_R_t[i]+1/1000*(L_BW_t[i]+L_IW_t[i])*(P_peak-P_idle)/L_rate
                 ==P_d_t[i]+P_res_t[i] for i in range(T))

#QoS constraint of interactive loads
model.addConstrs(A_IW_t[i]>=L_IW_t[i]/(L_rate-1/C_DT) for i in range(T))
#interactive loads must be immediately satisfied
model.addConstrs(L_IW_t[i]>=predicted_IWs[i] for i in range(T))
#enough processing resource for batch loads
model.addConstrs(L_rate*A_BW_t[i]>=L_BW_t[i] for i in range(T))
#batch loads constraints
for j in range(T):
    model.addConstr(gp.quicksum(L_BW_t[i] for i in range(0,j))<=gp.quicksum(predicted_BWs[i] for i in range(0,j)))
#assume TD=4,further modification allowed
for j in range(T-TD):
    model.addConstr(gp.quicksum(L_BW_t[i] for i in range(0,j+TD))>=gp.quicksum(predicted_BWs[i] for i in range(0,j)))
for j in range(T-TD,T):
    model.addConstr(gp.quicksum(L_BW_t[i] for i in range(0,T))>=gp.quicksum(predicted_BWs[i] for i in range(0,j)))

model.addConstrs(A_R_t[i]>=redundant_ratio*A_max for i in range(T))
model.addConstrs(A_IW_t[i]+A_BW_t[i]+A_R_t[i]<=A_max for i in range(T))
#green certificate related constraints
model.addConstrs(P_res_t[i]<=P_res_max[i] for i in range(T))
model.addConstr(gp.quicksum(P_res_t[i] for i in range(T))==W_res)
model.addConstr(W_res<=W_res_max)
model.addConstr(delta_W_res==W_res_fix-W_res)
#auxiliary variable z
z=model.addVar(vtype=GRB.BINARY,name='z')
M=1e5
model.addConstr(delta_W_res<=delta_W_res_fix+M*z)
model.addConstr(delta_W_res>=delta_W_res_fix-M*(1-z))

model.setObjective(gp.quicksum(L_BW_t[i]*C_BW+L_IW_t[i]*C_IW for i in range(T))
                   -gp.quicksum(P_d_t[i]*electricity_price[i] for i in range(T))
                   -C_RES*gp.quicksum(P_res_t[i] for i in range(T))
                   -C_GC*delta_W_res-C_punish*(delta_W_res-delta_W_res_fix)*z,GRB.MAXIMIZE)
model.optimize()