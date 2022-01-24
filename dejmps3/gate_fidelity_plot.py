import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

data = np.genfromtxt("gate_fidelity_data_duplicate.csv", delimiter=',')


# print(fidelity_ratios.shape)
# quit()

link_fidelities = data[0, 1:]
gate_fidelities = data[1:, 0]
fidelity_ratios = data[1:, 1:]
X, Y = np.meshgrid(link_fidelities, gate_fidelities)
ax.plot_surface(X, Y, fidelity_ratios)
fig.show()
# plt.pcolormesh(X, Y, fidelity_ratios, cmap='bwr', shading='gouraud')
# plt.contour(X, Y, fidelity_ratios, [0.8, 0.9, 1], colors='black')
plt.show()