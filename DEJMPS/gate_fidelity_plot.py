import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

fidelity_ratios = np.genfromtxt("gate_fidelity_data.csv", delimiter=',')
# print(fidelity_ratios.shape)
# quit()

x = np.arange(0.9, 1.00001, 0.01)
y = np.arange(0, 1.00001, 0.1)
X, Y = np.meshgrid(x, y)
ax.plot_surface(X, Y, fidelity_ratios)
fig.show()

plt.contour(X, Y, fidelity_ratios, [0.9, 1.0, 1.1])
plt.show()