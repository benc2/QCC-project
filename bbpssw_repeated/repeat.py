import json
from multiprocessing import Pool
import os
from time import sleep

import numpy as np
from matplotlib import pyplot as plt

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams.update({'font.size': 14})
# plt.subplots_adjust(left=0.1, right=0.985, top=0.98, bottom=0.12)
plt.subplots_adjust(left=0.1, right=0.985, top=0.9, bottom=0.12)

def prepare_network_at_given_link_fidelity(link_fidelity):
    fidelity_parameter = (4 * link_fidelity - 1) / 3
    # Load the networl.yaml and the template file
    fin = open("network_with_qubits_template.yaml", "rt")
    fout = open("network.yaml", "wt")

    # Update the fidelity in network.yaml
    for line in fin:
        # read replace the string and write to output file
        fout.write(line.replace('    fidelity: 1.0', '    fidelity: ' + str(fidelity_parameter)))
    fin.close()
    fout.close()


def n_attempts_with_given_fidelity(n, fidelity):
    # prepare_network_at_given_link_fidelity(fidelity)

    # Run netqasm simulation and store the result as an array
    pool = Pool(processes=n)
    rg = range(n)
    while True:
        try:
            pool.map(attempt_purification, rg)

            break
        except IndexError:
            print("Retry")
        except ValueError:
            print("Retry")
    return


def attempt_purification(i=0):
    sleep(i / 1)
    d = os.popen('netqasm simulate --log-to-files FALSE').read()
    # print(f"Attempt {i} finished with fidelity {d[2]}")
    # return d[0] == "True", float(d[2])
    # print(d)
    print(i)


# n_attempts_with_given_fidelity(100,1)

def calculate_average_dm_and_fidelity(depth,link_fidelity,run_simulations = True):
    if run_simulations:
        set_yamls_for_alice_and_bob(depth,link_fidelity)
        prepare_network_at_given_link_fidelity(link_fidelity)
        n_attempts_with_given_fidelity(100,link_fidelity)
    file = open(f"outputs_{link_fidelity}_{depth}.json",'r')
    dm = np.zeros((4,4),dtype=np.complex_)
    N = 0
    for line in file:
        # print(line)
        input = json.loads(line.replace("\n",""))
        if input[0]:
            dm += np.array(input[2]) + 1j* np.array(input[3])
            N += 1

    file.close()
    phi = np.array([1,0,0,1]) / np.sqrt(2)
    fidelity = phi.T @ dm/N @ phi

    print(fidelity)
    print(dm/N)


def set_yamls_for_alice_and_bob(depth,fidelity):
    file = open("alice.yaml","w")
    file.write(f"depth: {depth}\nlink_fidelity: {fidelity}")
    file.close()
    file = open("bob.yaml","w")
    file.write(f"depth: {depth}")
    file.close()


calculate_average_dm_and_fidelity(2,0.90)
calculate_average_dm_and_fidelity(1,0.90,False)
calculate_average_dm_and_fidelity(2,0.90,False)
