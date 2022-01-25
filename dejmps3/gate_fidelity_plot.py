import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

data = np.genfromtxt("gate_fidelity_data_duplicate.csv", delimiter=',')


# print(fidelity_ratios.shape)
# quit()

link_fidelities = data[0, 1:]
gate_fidelities = data[1:, 0]
fidelity_ratios = data[1:, 1:]
X, Y = np.meshgrid(link_fidelities, gate_fidelities)
# ax.plot_surface(X, Y, fidelity_ratios)
# fig.show()

levels = [0.75, 0.8, 0.85, 0.9, 0.95, 1] #[0.8, 0.9, 1]
fig, ax = plt.subplots()
CS = ax.contour(X, Y, fidelity_ratios, levels=levels, colors='black')
ax.clabel(CS, inline=1, fontsize=10)
# ax.colormesh(X, Y, fidelity_ratios, cmap='bwr', shading='gouraud')
# fig.show()
plt.pcolormesh(X, Y, fidelity_ratios, cmap='viridis', shading='gouraud')
# plt.contour(X, Y, fidelity_ratios, levels, colors='black')
# plt.clabel(levels)
plt.show()