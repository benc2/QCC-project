import os
import numpy as np
import matplotlib.pyplot as plt
import json

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams.update({'font.size': 14})
# plt.subplots_adjust(left=0.1, right=0.985, top=0.98, bottom=0.12)
plt.subplots_adjust(left=0.1, right=0.985, top=0.9, bottom=0.12)

# The number with which the fidelity is increased in network.yaml
delta_gate_fidelity = 0.002
delta_fidelity = 0.02

# Create data for analytical solution
x = np.arange(0.25, 1, 0.001)
analytical_fraction = lambda x: (x ** 2 + 1 / 9 * (1 - x) ** 2) / (
        x ** 2 + 2 / 3 * x * (1 - x) + 5 / 9 * (1 - x) ** 2) / x
# Plot the analytical solution
plt.plot(x, analytical_fraction(x), ":", label="Analytical solution for perfect gates")

# The starting gate-fidelity for the network.yaml file
gate_fidelity = 0.95
# Loop over the fidelity
while gate_fidelity <=1:
    # An empty array to store the output values in
    measurements = []
    # The starting fidelity for the network.yaml file
    fidelity = 0.34

    while fidelity <=1:
        # Load the networl.yaml and the template file
        fin = open("network_template.yaml", "rt")
        fout = open("network.yaml", "wt")

        # Update the fidelity in network.yaml
        for line in fin:
            # read replace the string and write to output file
            fout.write(line.replace('    fidelity: 1.0', '    fidelity: '+str(fidelity)).replace('    gate_fidelity: 1', '    gate_fidelity: '+str(gate_fidelity)))
        fin.close()
        fout.close()

        # Run netqasm simulation and store the result as an array
        d = os.popen('netqasm simulate --formalism dm --log-to-files FALSE').read().split("\n")

        # Upon success, store the measurement and increase the fidelity parameter
        if d[0]=="True":
            measurements.append([float(d[1]),float(d[2])])
            fidelity += delta_fidelity

        print(gate_fidelity, d)

    file = open(f"data/data_min_fidelity_at_gate_fidelity_{gate_fidelity}.json")
    file.write(json.dumps(measurements))
    file.close()

    # Convert the measurements to an np array
    measurements = np.array(measurements)

    # Plot the results
    plt.plot(measurements[:, 0], measurements[:, 1] / measurements[:, 0], label=f"Gate fidelity: {gate_fidelity}")

    plt.title("The fraction $F_{out}/F_{in}$ upon success as function of $F_{in}$")
    plt.xlabel("$F_{in}$")
    plt.ylabel("$F_{out}/F_{in}$")


    gate_fidelity += delta_gate_fidelity

plt.axhline(1, linestyle='-', color='k')  # horizontal line at 1
plt.grid()
plt.legend()
plt.show()
