from three_to_one_data import F_in_list, ratio_list_1, p_suc_list_099, p_suc_list_100
import matplotlib.pyplot as plt
import numpy as np

F_gate = np.arange(0.9,1.0001,0.001)
F_gate, F_in = np.meshgrid(F_gate,F_in_list)
ratio = np.reshape(ratio_list_1,F_gate.T.shape)

three_to_one_contour_data = [F_gate.T,F_in.T,ratio]
three_to_one_p_success_data = [F_in_list, p_suc_list_099, p_suc_list_100]

