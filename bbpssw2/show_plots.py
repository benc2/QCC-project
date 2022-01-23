from report_functions import gate_fidelity_contour_plot, plot_probability_of_success_from_files, plot_theoretical_probability_of_success
import matplotlib.pyplot as plt

# gate_fidelity_contour_plot()
# plt.figure()
plot_probability_of_success_from_files(0.99,**{'marker':"o",'color' : "red", 'label': f"Gate fidelity: 0.99"})
plot_probability_of_success_from_files(1,**{'marker':"s", 'color': "blue",'label': f"Gate fidelity: 1"})
plot_probability_of_success_from_files(0.8,**{'marker':"x", 'color': "green",'label': f"Gate fidelity: 0.8"})
plot_theoretical_probability_of_success()
plt.subplots_adjust(left=0.1, right=0.985, top=0.98, bottom=0.12)

plt.legend()
plt.show()