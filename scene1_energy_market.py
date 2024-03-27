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
P_grid_t=model.addVars(24,lb=-GRB.INFINITY,ub=GRB.INFINITY,vtype=GRB.CONTINUOUS,name='P_grid_t')
#constraints
#power balance constraint:DC's power supply comes from utility grid and PV generation
model.addConstrs(1/1000*(P_idle+0.75*P_peak)*(A_BW_t[i]+A_IW_t[i]+A_R_t[i])+1/1000*(L_BW_t[i]+L_IW_t[i])*(P_peak-P_idle)/L_rate==P_grid_t[i]+P_res_t[i] for i in range(T))
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
model.addConstrs(P_grid_t[i]<=P_grid_max for i in range(T))
model.addConstrs(P_grid_t[i]>=-P_grid_max for i in range(T))



model.setObjective(gp.quicksum(L_BW_t[i]*C_BW+L_IW_t[i]*C_IW for i in range(T))-gp.quicksum(P_grid_t[i]*electricity_price[i] for i in range(T))
                   -gp.quicksum(P_grid_t[i]*electricity_price[i] for i in range(T))
                   -C_RES*gp.quicksum(P_res_t[i] for i in range(T))
                   ,GRB.MAXIMIZE)
model.optimize()
'''
A_BW_t=A_BW_t.X
A_IW_t=A_IW_t.X
A_R_t=A_R_t.X
L_BW_t=L_BW_t.X
L_IW_t=L_IW_t.X
P_res_t=P_res_t.X
P_grid_t=P_grid_t.X
'''
A_BW_t_res=np.array([A_BW_t[i].X for i in range(T)])
A_IW_t_res=np.array([A_IW_t[i].X for i in range(T)])
A_R_t_res=np.array([A_R_t[i].X for i in range(T)])
L_BW_t_res=np.array([L_BW_t[i].X for i in range(T)])
L_IW_t_res=np.array([L_IW_t[i].X for i in range(T)])
P_res_t_res=np.array([P_res_t[i].X for i in range(T)])
P_grid_t_res=np.array([P_grid_t[i].X for i in range(T)])

P_res_t_res=np.array([P_res_t[i].X for i in range(T)])


plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

plt.plot(L_IW_t_res,marker='o',color='r',label="交互式负荷处理能力")
plt.plot(L_BW_t_res,marker='o',color='g',label="批处理负荷处理能力")
plt.title("交互式负荷、批处理负荷处理能力(场景1)")
plt.xlabel("时间/小时")
plt.ylabel("数据处理能力")
plt.legend()
plt.show()


print(sum(P_res_t_res)/sum(P_res_max))
print(sum(L_BW_t_res[i]*C_BW+L_IW_t_res[i]*C_IW for i in range(T)))
print(sum(P_grid_t_res[i]*electricity_price[i] for i in range(T)))
print(C_RES*sum(P_res_t_res[i] for i in range(T)))
#plt.plot(L_BW_t_res)
#plt.show()