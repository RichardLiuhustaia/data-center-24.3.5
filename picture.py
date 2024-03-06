import matplotlib.pyplot as plt
import seaborn as sns
from model import A_BW_t_res,A_IW_t_res,A_R_t_res,L_BW_t_res,L_IW_t_res,P_res_t_res,P_grid_t_res
from parameters import *
'''
print(L_BW_t_res)
plt.plot(predicted_BWs)
plt.plot(L_BW_t_res)
plt.show()
'''


plt.plot(P_res_max-P_res_t_res)
plt.show()

print(sum(P_res_t_res))