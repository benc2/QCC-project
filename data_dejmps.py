import numpy as np
import matplotlib.pyplot as plt


@np.vectorize
def p_succ_theoretical(f):
    f_conj = (1 - f) / 3
    return f ** 2 + 2 * f * f_conj + 5 * f_conj ** 2


@np.vectorize
def p_succ_fail(f):
    return (8 * f ** 2 - 4 * f + 5) / 9


filename = "dejmps3/probabilities99_full.csv"

data = np.genfromtxt(filename, delimiter=',')
f_in = data[:, 1]
p_succ_099 = data[:, 4]
p_theory = p_succ_theoretical(f_in)

filename = "dejmps3/probabilities100_2.csv"

data = np.genfromtxt(filename, delimiter=',')
f_in = data[:, 1]
p_succ_100 = data[:, 4]
p_theory = p_succ_theoretical(f_in)

# plt.plot(f_in, p_succ, '.')
# plt.plot(f_in, p_theory)
# plt.plot(f_in, p_succ_fail(f_in))
# plt.show()


data = np.genfromtxt("dejmps3/gate_fidelity_data_duplicate.csv", delimiter=',')

# print(fidelity_ratios.shape)
# quit()

link_fidelities = data[0, 1:]
gate_fidelities = data[1:, 0]
fidelity_ratios = data[1:, 1:]
X, Y = np.meshgrid(link_fidelities, gate_fidelities)
# ax.plot_surface(X, Y, fidelity_ratios)
# fig.show()

# levels = [0.75, 0.8, 0.85, 0.9, 0.95, 1] #[0.8, 0.9, 1]
# fig, ax = plt.subplots()
# CS = ax.contour(X, Y, fidelity_ratios, levels=levels, colors='black')
# ax.clabel(CS, inline=1, fontsize=10)
# # ax.colormesh(X, Y, fidelity_ratios, cmap='bwr', shading='gouraud')
# # fig.show()
# plt.pcolormesh(X, Y, fidelity_ratios, cmap='viridis', shading='gouraud')
# # plt.contour(X, Y, fidelity_ratios, levels, colors='black')
# # plt.clabel(levels)
# plt.show()

dejmps_p_success_data = [f_in, p_succ_099, p_succ_100]
dejmps_contour_data = [Y,0.25 + 0.75*X, fidelity_ratios]
