import os
import csv
# import matplotlib.pyplot as plt
import numpy as np
import yamltools


def get_output_fidelity():
    d = os.popen("netqasm simulate --formalism dm").read().split("\n")
    x = float(d[-2])
    print(x)
    return x


def get_fidelity_ratio(gate_fidelity, link_fidelity):
    yamltools.change_gate_fidelity(gate_fidelity)
    yamltools.change_link_fidelity(link_fidelity)
    while True:
        cmd_out = os.popen("netqasm simulate --formalism dm --log-to-files FALSE").read()
        d = cmd_out.split("\n")
        last_line_split = d[-2].split()
        # print(last_line_split)
        success = int(last_line_split[0])
        F_in = float(last_line_split[1])
        F_out = float(last_line_split[2])
        if success:
            break

    return F_out/F_in

# def find_min_fidelity(gate_fidelity, n_iter=6, file=None):
#     # find minimum link fidelity such that fidelity improves under DEJMPS given gate fidelity
#     # make sure N=1 in app_sender!
#     yamltools.change_gate_fidelity(gate_fidelity)
#     min_input_fidelity = 0
#     max_input_fidelity = 1
#     for i in range(n_iter):
#         current_input_fidelity = (min_input_fidelity + max_input_fidelity)/2
#         yamltools.change_link_fidelity(current_input_fidelity)
#         output_fidelity = get_output_fidelity()
#         if output_fidelity > current_input_fidelity:
#             max_input_fidelity = current_input_fidelity
#         else:
#             min_input_fidelity = current_input_fidelity
#
#     return (min_input_fidelity + max_input_fidelity)/2

print(get_fidelity_ratio(0.919, 0.41))
quit()

# to fix: lf 0.41, gf 0.918
# somewhere in gf 0.927
filename = "gate_fidelity_data.csv"
gate_fidelities = [0.927, 0.969]  # np.arange(0.945, 1.00001, 0.001)
link_fidelities = np.arange(0, 1.00001, 0.01)
# with open(filename, 'a') as file:
#     writer = csv.writer(file, delimiter=',')
#     writer.writerow(np.append([-1], link_fidelities))  #-1 just to make it square
#     print("written")


for f_gate in gate_fidelities:
    print(f"f_gate: {f_gate}")
    f_ratios = []
    for n,f_link in enumerate(link_fidelities):
        f_ratios.append(get_fidelity_ratio(f_gate, f_link))
        print(f"\r{n+1:0>3}/101", end='')
    # f_ratios = [get_fidelity_ratio(f_gate, f_link) for f_link in link_fidelities]
    with open(filename, 'a') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow([f_gate] + f_ratios)
        print("\nwritten")

# x_axis = np.linspace(0,1, 3)
# y = [find_min_fidelity(float(x), n_iter=2) for x in x_axis]
# print(y)
# plt.plot(x_axis, y)


