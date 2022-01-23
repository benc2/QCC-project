import json
from multiprocessing import Pool
import os
from time import sleep

import numpy as np
from matplotlib import pyplot as plt

plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams.update({'font.size': 14})
# plt.subplots_adjust(left=0.1, right=0.985, top=0.98, bottom=0.12)
# plt.subplots_adjust(left=0.1, right=0.985, top=0.9, bottom=0.12)

def prepare_network_at_given_link_fidelity(link_fidelity,gate_fidelity=1):
    fidelity_parameter = (4 * link_fidelity - 1) / 3
    # Load the networl.yaml and the template file
    fin = open("network_template.yaml", "rt")
    fout = open("network.yaml", "wt")

    # Update the fidelity in network.yaml
    for line in fin:
        # read replace the string and write to output file
        fout.write(line.replace('    fidelity: 1.0', '    fidelity: ' + str(fidelity_parameter)).replace('    gate_fidelity: 1', '    gate_fidelity: '+str(gate_fidelity)))
    fin.close()
    fout.close()


def n_attempts_with_given_fidelity(n, fidelity,gate_fidelity=1):
    prepare_network_at_given_link_fidelity(fidelity,gate_fidelity)

    # Run netqasm simulation and store the result as an array
    pool = Pool(processes=n)
    rg = range(n)
    while True:
        try:
            output, dummy = zip(*pool.map(attempt_purification, rg))

            break
        except IndexError:
            print("Retry")
        except ValueError:
            print("Retry")
    return output


def attempt_purification(i=0):
    sleep(i / 3)
    d = os.popen('netqasm simulate --formalism dm --log-to-files FALSE').read().split("\n")
    print(f"Attempt {i} finished with fidelity {d[2]}")
    return d[0] == "True", float(d[2])


def determine_required_purification_tree_length(start_fidelity, target_fidelity):
    output_fidelity = start_fidelity
    fidelities = [start_fidelity]
    while output_fidelity < target_fidelity:
        prepare_network_at_given_link_fidelity(output_fidelity)
        succeeded = False
        while not succeeded:
            attempt = attempt_purification()
            succeeded = attempt[0]
        output_fidelity = attempt[1]
        fidelities.append(output_fidelity)

    return fidelities


def plot_probability_of_success_from_files(gate_fidelity,fit=False,marker=".", color="black",label="Unknown",sample_size = None):
    measurements = []
    filename_start = "data_success_rate_at_fidelity_"
    folder = "data"
    filelist= os.listdir(folder)
    filelist.sort()
    for filename in filelist:
        if filename.startswith(filename_start) and filename.endswith(f"_and_gate_fidelity_{gate_fidelity}.json"):
            file = open(f"{folder}/{filename}", "r")
            contents = json.loads(file.read())
            measurements.append(
                [float(filename.replace(filename_start, "").replace(f"_and_gate_fidelity_{gate_fidelity}.json", "")), np.mean(contents[:sample_size]), np.std(contents[:sample_size])])
            file.close()

    measurements = np.array(measurements).T
    print(measurements)

    plt.plot(measurements[0], measurements[1],marker,markersize=2,color=color,label=label)
    if fit:
        plt.plot(measurements[0],np.poly1d(np.polyfit(measurements[0],measurements[1],2))(measurements[0]),linestyle="dashed",linewidth=1,color=color)
    plt.xlabel("Link fidelity")
    plt.ylabel("Rate of success")
    # plt.title("Protocol success rate as function of link fidelity")
    plt.grid()
    # plt.show()
    return


def gate_fidelity_plot(gate_fidelity = 0.98):
    filename_start = "data_min_fidelity_at_gate_fidelity_"
    folder = "bbpssw2/data"
    file = open(f"{folder}/{filename_start}{gate_fidelity}.json")
    measurements = json.loads(file.read())
    file.close()

    # Convert the measurements to an np array
    measurements = np.array(measurements)
    np.sort(measurements)
    # Create data for analytical solution
    p = np.arange(0.0, 1, 0.001)
    analytical_fraction = lambda x: (x ** 2 + 1 / 9 * (1 - x) ** 2) / (
            x ** 2 + 2 / 3 * x * (1 - x) + 5 / 9 * (1 - x) ** 2)
    fid4 = lambda p: 1/16 + 15/16*p
    fid2 = lambda p: 0.25 + 0.75*p
    fid1 = lambda p: 0.5 + 0.5*p
    par4 = lambda fid: (16 * fid - 1) / 15
    par2 = lambda fid: (4 * fid - 1) / 3
    par1 = lambda fid: (2 * fid - 1) /1



    plt.figure()
    # Plot the analytical solution
    # plt.plot(fid(p), fid(par(analytical_fraction(fid(p * gate_fidelity **MM))))/fid(p), ":", label="Analytical solution for perfect gates")
    # plt.plot(fid(p), analytical_fraction(fid(par(fid1(par1(fid(p))*gate_fidelity))*gate_fidelity**2))/fid(p), ":", label="Analytical solution for perfect gates")
    # plt.plot(fid2(p), analytical_fraction(fid2(par2(fid2(par2(fid2(p))*gate_fidelity**0))*gate_fidelity**2))/fid2(p), ":", label="Analytical solution for perfect gates")
    # Plot the results
    plt.plot(measurements[:, 0], measurements[:, 1] / measurements[:, 0], label=f"Gate fidelity: {gate_fidelity}")

    # plt.title("The fraction $F_{out}/F_{in}$ upon success as function of $F_{in}$")
    plt.xlabel("$F_{in}$")
    plt.ylabel("$F_{out}/F_{in}$")

    # gate_fidelity += delta_gate_fidelity


    plt.axhline(1, linestyle='-', color='k')  # horizontal line at 1
    plt.grid()
    plt.legend()
    # plt.show()

# gate_fidelity_plot()


def gate_fidelity_contour_plot():
    filename_start = "data_min_fidelity_at_gate_fidelity_"
    measurements = []
    folder = "data"
    filelist = os.listdir(folder)
    filelist.sort()
    gate_fidelities = []
    link_fidelities = []
    for filename in filelist:

        if filename.startswith(filename_start):
            gate_fidelities.append( float(filename.replace(filename_start,"").replace(".json","")))
            file = open(f"{folder}/{filename}", "r")
            contents = json.loads(file.read())
            contents = np.array(contents).T
            measurements.append((contents[1]/contents[0]))
            link_fidelities = contents[0].tolist()
            file.close()


    # Convert the measurements to an np array
    measurements = np.vstack(measurements).T



    gate_fidelities = np.array(gate_fidelities)
    link_fidelities = np.array(link_fidelities)
    gate_fidelities, link_fidelities = np.meshgrid(gate_fidelities,link_fidelities)


    cs = plt.contour(gate_fidelities,link_fidelities,measurements, levels=[0.8,0.85,0.875,0.9,0.925,0.95,0.975,1,1.025,1.05,1.075,1.1], colors="k", linestyles="solid", label="BBPSSW")
    plt.clabel(cs)
    plt.xlim(gate_fidelities[0,0],1)
    plt.ylim(link_fidelities[0,0],1)
    # plt.title("The fraction $F_{out}/F_{in}$ upon success as function of $F_{in}$")
    plt.xlabel("Gate fidelity")
    plt.ylabel("Link fidelity")
    # plt.title("Output fidelity as fraction of link fidelity")

    # gate_fidelity += delta_gate_fidelity


    plt.axhline(1, linestyle='-', color='k')  # horizontal line at 1
    plt.grid()
    plt.legend(["BBPSSW"],loc="upper center")
    plt.subplots_adjust(left=0.1, right=0.973, top=0.98, bottom=0.12)

    # plt.show()

# gate_fidelity_surface_plot()





def do_simulations_for_contour_plot():
    # The number with which the fidelity is increased in network.yaml
    delta_gate_fidelity = 0.001
    delta_fidelity = 0.01
    # The starting gate-fidelity for the network.yaml file
    gate_fidelity = 0.9
    # Loop over the fidelity
    while gate_fidelity <1+delta_gate_fidelity*0.5:
        if gate_fidelity >1:
            gate_fidelity = 1.0
        # An empty array to store the output values in
        measurements = []
        # The starting fidelity for the network.yaml file
        fidelity = 0.0

        while fidelity <1+0.5*delta_fidelity:
            if fidelity >1:
                fidelity =1.0
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

        file = open(f"data/data_min_fidelity_at_gate_fidelity_{gate_fidelity}.json","w")
        file.write(json.dumps(measurements))
        file.close()

        # # Convert the measurements to an np array
        # measurements = np.array(measurements)
        #
        # # Plot the results
        # plt.plot(measurements[:, 0], measurements[:, 1] / measurements[:, 0], label=f"Gate fidelity: {gate_fidelity}")
        #
        # plt.title("The fraction $F_{out}/F_{in}$ upon success as function of $F_{in}$")
        # plt.xlabel("$F_{in}$")
        # plt.ylabel("$F_{out}/F_{in}$")


        gate_fidelity += delta_gate_fidelity

def plot_theoretical_probability_of_success():
    F_in = 0.25 + 0.75 * np.arange(0,1.0001,0.001)
    p_succ = F_in**2 + 2*F_in*(1-F_in)/3+ 5*(1-F_in)**2/9

    plt.plot(F_in,p_succ,"k:",label="Theoretical probability of success")
