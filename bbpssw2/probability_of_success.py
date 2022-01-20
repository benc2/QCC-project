import json
from report_functions import n_attempts_with_given_fidelity, plot_probability_of_success_from_files
import numpy as np

fidelity = 0.25
delta_fidelity = 0.005
number_of_measurements_per_fidelity_value = 400
measurements = []
while fidelity <=1:
  # if fidelity > 0.710001:
    new_measurement = n_attempts_with_given_fidelity(number_of_measurements_per_fidelity_value,fidelity)
    file = open(f"data/data_success_rate_at_fidelity_{fidelity}.json","w")
    file.write(json.dumps(new_measurement))
    file.close()
    measurements.append([fidelity,np.mean(new_measurement), np.std(new_measurement)])
    fidelity += delta_fidelity

# measurements = np.array(measurements).T
# print(measurements)
# plt.plot(measurements[0],measurements[1])
# plt.show()

plot_probability_of_success_from_files()