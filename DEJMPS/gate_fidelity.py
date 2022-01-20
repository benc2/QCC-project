import os
import csv
import yaml
import numpy as np
import yamltools



def get_output_fidelity():
    if os.name == 'nt':
        print("yeah")
        command = "wsl cd /mnt/c/users/benja/Programming/PycharmProjects/QCC-project/DEJMPS & wsl netqasm simulate --formalism dm"
    else:
        command = "netqasm simulate --formalism dm"
    d = os.popen(command).read().split("\n")[-1]


print(get_output_fidelity())
quit()

def find_min_fidelity(gate_fidelity, n_iter=6, file=None):
    # find minimum link fidelity such that fidelity improves under DEJMPS given gate fidelity
    # make sure N=1 in app_sender!
    yamltools.change_gate_fidelity(gate_fidelity)
    min_input_fidelity = 0
    max_input_fidelity = 1
    for i in range(n_iter):
        current_input_fidelity = (min_input_fidelity + max_input_fidelity)/2
        yamltools.change_link_fidelity(current_input_fidelity)
        output_fidelity = get_fidelity()
        if output_fidelity > current_input_fidelity:
            max_input_fidelity = current_input_fidelity
        else:
            min_input_fidelity = current_input_fidelity

    return (min_input_fidelity + max_input_fidelity)/2




x_axis = np.linspace()


