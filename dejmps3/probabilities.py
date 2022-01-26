import os
import multiprocessing
import csv
import numpy as np
import yamltools


def get_simulation_result():
    cmd_out = os.popen("netqasm simulate --formalism dm --log-to-files FALSE").read()
    d = cmd_out.split("\n")
    last_line_split = d[-2].split()
    # print(last_line_split)
    success = int(last_line_split[0])
    F_in = float(last_line_split[1])
    F_out = float(last_line_split[2])
    return [bool(success), F_in, F_out]


def get_success_fidelities():
    while True:
        success, f_in, f_out = get_simulation_result()
        if success:
            return f_in, f_out


def distillation_success(x):
    return get_simulation_result()[0]



N = 1000
gate_fidelity = 1
filename = f"probabilities{round(100*gate_fidelity)}.csv"

try:
    with open(filename, 'r') as file:
        data = np.genfromtxt(filename, delimiter=',')
        starting_point = round(data[-1, 0] + 0.01, 2)
except FileNotFoundError:
    starting_point = 0

# starting_point = 0.6 # temp override
f_links = np.arange(starting_point, 1.001, 0.01)


yamltools.change_gate_fidelity(gate_fidelity)
for link_fidelity in f_links:
    print(f"f_link: {link_fidelity}")
    yamltools.change_link_fidelity(link_fidelity)
    F_in, F_out = get_success_fidelities()
    pool = multiprocessing.Pool(None)
    tasks = range(N)
    results = []
    r = pool.map_async(distillation_success, tasks, callback=results.append)
    r.wait()  # Wait on the results
    successes = sum([int(s) for s in results[0]])
    with open(filename, 'a') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow([link_fidelity, F_in, F_out, successes, successes/N])
        print("\nwritten")