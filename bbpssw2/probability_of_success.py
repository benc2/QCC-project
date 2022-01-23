import json
import os.path

from report_functions import n_attempts_with_given_fidelity, plot_probability_of_success_from_files
gate_fidelity = 0.99
fidelity_param = 0
delta_fidelity = 0.01
number_of_measurements_per_fidelity_value = 1000
measurements = []
while fidelity_param <=1 + 0.5*delta_fidelity:
    if fidelity_param > 1:
        fidelity_param = 1
    fidelity = 0.25 + 0.75*fidelity_param
    # if fidelity > 0.287501:
    filename = f"data/success_rate_data_at_fidelity_{fidelity}_and_gate_fidelity_{gate_fidelity}.json"
    print(filename)
    if not os.path.isfile(filename):
        new_measurement = n_attempts_with_given_fidelity(number_of_measurements_per_fidelity_value,fidelity,gate_fidelity)
        file = open(filename,"w")
        file.write(json.dumps(new_measurement))
        file.close()
        # measurements.append([fidelity,np.mean(new_measurement), np.std(new_measurement)])
    fidelity_param += delta_fidelity

# measurements = np.array(measurements).T
# print(measurements)
# plt.plot(measurements[0],measurements[1])
# plt.show()

# plot_probability_of_success_from_files()