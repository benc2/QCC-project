import json
import os

import numpy as np

filename_start = "data_min_fidelity_at_gate_fidelity_"
measurements = []
folder = "bbpssw2/data"
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

# levels = [0.8,0.85,0.875,0.9,0.925,0.95,0.975,1,1.025,1.05,1.075,1.1]
# styles = []
# for level in levels:
#     if level == 1:
#         styles.append("solid")
#     else:
#         styles.append("dotted")
# cs = plt.contour(gate_fidelities,link_fidelities,measurements, linewidths = 1,levels=levels,linestyles = styles, colors="k", label="BBPSSW")
# plt.clabel(cs)
# plt.xlim(gate_fidelities[0,0],1)
# plt.ylim(link_fidelities[0,0],1)
# # plt.title("The fraction $F_{out}/F_{in}$ upon success as function of $F_{in}$")
# plt.xlabel("Gate fidelity parameter")
# plt.ylabel("Link fidelity")
contour_measurements = measurements



filename_start = "success_rate_data_at_fidelity_"
folder = "bbpssw2/data"
filelist= os.listdir(folder)
filelist.sort()
sample_size = None

gate_fidelity = 0.99
measurements = []
for filename in filelist:
    if filename.startswith(filename_start) and filename.endswith(f"_and_gate_fidelity_{gate_fidelity}.json"):
        file = open(f"{folder}/{filename}", "r")
        contents = json.loads(file.read())
        measurements.append(
            [float(filename.replace(filename_start, "").replace(f"_and_gate_fidelity_{gate_fidelity}.json", "")), np.mean(contents[:sample_size]), np.std(contents[:sample_size])])
        file.close()

measurements = np.array(measurements).T
measurements = measurements[:,np.argsort(measurements[0])]

# print(measurements)

p_succ_099 =  measurements[1]

gate_fidelity = 1
measurements = []
for filename in filelist:
    if filename.startswith(filename_start) and filename.endswith(f"_and_gate_fidelity_{gate_fidelity}.json"):
        file = open(f"{folder}/{filename}", "r")
        contents = json.loads(file.read())
        measurements.append(
            [float(filename.replace(filename_start, "").replace(f"_and_gate_fidelity_{gate_fidelity}.json", "")), np.mean(contents[:sample_size]), np.std(contents[:sample_size])])
        file.close()

measurements = np.array(measurements).T
measurements = measurements[:,np.argsort(measurements[0])]

# print(measurements)


p_succ_100 =  measurements[1]

bbpssw_contour_data = [gate_fidelities.T,link_fidelities.T,contour_measurements.T]
bbpssw_p_success_data = [measurements[0],p_succ_099,p_succ_100]