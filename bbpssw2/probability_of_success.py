import json
from report_functions import n_attempts_with_given_fidelity, plot_probability_of_success_from_files
import numpy as np
gate_fidelity = 0.8
fidelity = 0.25
delta_fidelity = 0.01
number_of_measurements_per_fidelity_value = 1000
measurements = []
while fidelity <=1 + 0.5*delta_fidelity:
  if fidelity > 1:
    fidelity = 1
  if fidelity > 0.3301:
    new_measurement = n_attempts_with_given_fidelity(number_of_measurements_per_fidelity_value,fidelity,gate_fidelity)
    file = open(f"data/data_success_rate_at_fidelity_{fidelity}_and_gate_fidelity_{gate_fidelity}.json","w")
    file.write(json.dumps(new_measurement))
    file.close()
    # measurements.append([fidelity,np.mean(new_measurement), np.std(new_measurement)])
  fidelity += delta_fidelity

# measurements = np.array(measurements).T
# print(measurements)
# plt.plot(measurements[0],measurements[1])
# plt.show()

# plot_probability_of_success_from_files()