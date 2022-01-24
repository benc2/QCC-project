from report_functions import gate_fidelity_contour_plot, plot_probability_of_success_from_files, \
    plot_theoretical_probability_of_success, gate_fidelity_plot, plot_expected_relative_increase
import matplotlib.pyplot as plt

gate_fidelity_contour_plot()
plt.figure()
input_fidelities, probs099 = plot_probability_of_success_from_files(0.99, **{'marker': "o", 'color': "red",
                                                                             'label': f"Gate fidelity 0.99"})
input_fidelities, probs100 = plot_probability_of_success_from_files(1, **{'marker': "s", 'color': "blue",
                                                                          'label': f"Gate fidelity 1"})
# plot_probability_of_success_from_files(0.8,**{'marker':"x", 'color': "green",'label': f"Gate fidelity: 0.8"})
plot_theoretical_probability_of_success()
plt.subplots_adjust(left=0.1, right=0.985, top=0.98, bottom=0.12)
plt.grid()
plt.legend()

plt.figure()
# input_fidelities, fractions099  = gate_fidelity_plot(0.9900000000000001,prefix="temp_")
input_fidelities, fractions099 = gate_fidelity_plot(0.99, color="red" , prefix="temp_")

input_fidelities, fractions100 = gate_fidelity_plot(1.0, color="blue", prefix="temp_")
plt.subplots_adjust(left=0.12, right=0.985, top=0.98, bottom=0.12)
plt.grid()
plt.legend()
plt.figure()
input_fidelities099, expectation099 = plot_expected_relative_increase(input_fidelities, fractions099, probs099, 2,label="Gate fidelity 0.99", color="red")
input_fidelities100, expectation100 = plot_expected_relative_increase(input_fidelities, fractions100, probs100, 2,label="Gate fidelity 1.0",color="blue")
plt.subplots_adjust(left=0.15, right=0.985, top=0.98, bottom=0.12)
plt.grid()
plt.legend()
plt.show()
