import numpy as np
import matplotlib.pyplot as plt

@np.vectorize
def p_succ_theoretical(f):

    f_conj = (1-f)/3
    return f**2 + 2*f*f_conj + 5*f_conj**2

@np.vectorize
def p_succ_fail(f):
    return (8*f**2 - 4*f + 5)/9

filename = "prob99backup.csv"

data = np.genfromtxt(filename, delimiter=',')
f_in = data[:, 1]
p_succ = data[:,4]
p_theory = p_succ_theoretical(f_in)

plt.plot(f_in, p_succ, '.')
plt.plot(f_in, p_theory)
plt.plot(f_in, p_succ_fail(f_in))
plt.show()