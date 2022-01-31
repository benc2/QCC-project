from matplotlib import pyplot as plt
from matplotlib.lines import Line2D

import numpy as np

from data_dejmps import dejmps_contour_data,dejmps_p_success_data
from data_bbpssw import bbpssw_contour_data, bbpssw_p_success_data
from data_three_to_one import three_to_one_contour_data, three_to_one_p_success_data

plt.rcParams["font.family"] = "Stix Two Text"
plt.rcParams.update({'font.size': 14})

titles = []

colors = ["orange","blue","green"]


markers = ["o","v","D"]

labels = ["DEJMPS","BBPSSW","Three to one"]

dejmps_settings = {'colors': colors[0], 'color': colors[0], 'marker': markers[0],'label':labels[0]}
bbpssw_settings = {'colors': colors[1], 'color': colors[1], 'marker': markers[1],'label':labels[1]}
tto_settings = {'colors': colors[2], 'color': colors[2], 'marker': markers[2],'label':labels[2]}




def expected_relative_increase(input_fidelities, fractions,success_rate,input_pairs=2):
    expectation = (fractions-1)*success_rate/input_pairs
    # plt.plot(input_fidelities,expectation,label=label,color=color,linestyle=linestyle,linewidth=linewidth)
    # plt.grid()
    # plt.axhline(0, linestyle='-', color='k')  # horizontal line at 0
    # plt.xlabel("Input state fidelity")
    # plt.ylabel("Expected relative improvement")
    return input_fidelities, 100*expectation





titles.append("Contour plots")
plt.figure("Contour plots")
print(bbpssw_contour_data)
levels = np.arange(0.7,1.3,0.05)
styles = []
for level in levels:
    if abs(level - 1)<0.001:
        styles.append("solid")
    else:
        styles.append("dotted")

general_settings = {'levels': levels, 'linestyles': styles}



dempjs_contours = plt.contour(dejmps_contour_data[0][50:], dejmps_contour_data[1][50:],dejmps_contour_data[2][50:],**general_settings,**dejmps_settings)
bbpssw_contours = plt.contour(bbpssw_contour_data[0][50:],bbpssw_contour_data[1][50:],bbpssw_contour_data[2][50:],**general_settings,**bbpssw_settings)
threetoone_contours = plt.contour(three_to_one_contour_data[0][50:],three_to_one_contour_data[1][50:],three_to_one_contour_data[2][50:],**general_settings,**tto_settings)
plt.clabel(dempjs_contours,levels=levels[::2])
plt.clabel(bbpssw_contours,levels=levels[::2])
plt.clabel(threetoone_contours,levels=levels[::2])
plt.xlim([0.95,1])
plt.ylim([0.25,1])
plt.xlabel("Gate fidelity parameter")
plt.ylabel("Input state fidelity")
dejmps_patch = Line2D([0],[0],color=colors[0], label=labels[0])
bbpssw_patch = Line2D([0],[0],color=colors[1], label=labels[1])
tto_patch = Line2D([0],[0],color=colors[2], label=labels[2])
plt.grid()


plt.legend(handles=[dejmps_patch, bbpssw_patch, tto_patch],loc="upper left")
plt.subplots_adjust(0.095,0.112,0.97,0.98)

levels = np.arange(0.7,1.3,0.025)
styles = []
for level in levels:
    if abs(level - 1)<0.001:
        styles.append("solid")
    else:
        styles.append("dotted")

general_settings = {'levels': levels, 'linestyles': styles} #, 'colors': 'black'}


titles.append("Contour plot DEJMPS")
plt.figure("Contour plot DEJMPS")
contours = plt.contour(dejmps_contour_data[0][50:], dejmps_contour_data[1][50:],dejmps_contour_data[2][50:],**general_settings,**dejmps_settings)
plt.xlabel("Gate fidelity parameter")
plt.ylabel("Input state fidelity")

plt.xlim([0.95,1])
plt.ylim([0.25,1])
plt.clabel(contours)
plt.subplots_adjust(0.095,0.112,0.97,0.98)
plt.grid()


titles.append("Contour plot BBPSSW")
plt.figure("Contour plot BBPSSW")
contours = plt.contour(bbpssw_contour_data[0][50:], bbpssw_contour_data[1][50:],bbpssw_contour_data[2][50:],**general_settings,**bbpssw_settings)
plt.xlabel("Gate fidelity parameter")
plt.ylabel("Input state fidelity")

plt.xlim([0.95,1])
plt.ylim([0.25,1])
plt.clabel(contours)
plt.subplots_adjust(0.095,0.112,0.97,0.98)
plt.grid()


titles.append("Contour plot Three to one")
plt.figure("Contour plot Three to one")
contours = plt.contour(three_to_one_contour_data[0][50:], three_to_one_contour_data[1][50:],three_to_one_contour_data[2][50:],**general_settings,**tto_settings)
plt.xlabel("Gate fidelity parameter")
plt.ylabel("Input state fidelity")

plt.xlim([0.95,1])
plt.ylim([0.25,1])
plt.clabel(contours,levels[::2])
plt.subplots_adjust(0.095,0.112,0.97,0.98)
plt.grid()


ticks = np.arange(0.25,1.001,0.15)


titles.append("Success rate at gate fidelity p0.99")
plt.figure("Success rate at gate fidelity p0.99")

plt.plot(dejmps_p_success_data[0],dejmps_p_success_data[1], markers[0],markersize=2,color = colors[0],label=labels[0])
plt.plot(bbpssw_p_success_data[0],bbpssw_p_success_data[1], markers[1],markersize=2,color = colors[1],label=labels[1])
plt.plot(three_to_one_p_success_data[0],three_to_one_p_success_data[1], markers[2],markersize=2,color = colors[2],label=labels[2])
plt.legend()
plt.xlabel("Input state fidelity")
plt.ylabel("Protocol success rate")
plt.grid()
plt.xticks(ticks)
plt.subplots_adjust(0.095,0.112,0.995,0.995)


titles.append("Success rate at gate fidelity p1.00")
plt.figure("Success rate at gate fidelity p1.00")

plt.plot(dejmps_p_success_data[0],dejmps_p_success_data[2], markers[0],markersize=2,color = colors[0],label=labels[0])
plt.plot(bbpssw_p_success_data[0],bbpssw_p_success_data[2], markers[1],markersize=2,color = colors[1],label=labels[1])
plt.plot(three_to_one_p_success_data[0],three_to_one_p_success_data[2], markers[2],markersize=2,color = colors[2],label=labels[2])
plt.legend()
plt.grid()
plt.xlabel("Input state fidelity")
plt.ylabel("Protocol success rate")
plt.xticks(ticks)
plt.subplots_adjust(0.095,0.112,0.995,0.995)


titles.append("Ratio F_out F_in at p1.00")
plt.figure("Ratio F_out F_in at p1.00")
plt.axhline(1,color="black",linewidth=1)

plt.plot(dejmps_contour_data[1][0],dejmps_contour_data[2][100],markers[0],markersize=2,color=colors[0],label=labels[0])
plt.plot(bbpssw_contour_data[1][0],bbpssw_contour_data[2][100],markers[1],markersize=1,color=colors[1],label=labels[1],linewidth=1)
plt.plot(three_to_one_contour_data[1][0],three_to_one_contour_data[2][100],markers[2],markersize=2,color=colors[2],label=labels[2])
plt.grid()
plt.legend()
plt.xlabel("Input state fidelity")
plt.ylabel("Ratio of input and output state fidelity")
plt.xticks(ticks)
plt.subplots_adjust(0.11,0.112,0.995,0.995)


titles.append("Ratio F_out F_in at p0.99")
plt.figure("Ratio F_out F_in at p0.99")
plt.axhline(1,color="black",linewidth=1)
plt.plot(dejmps_contour_data[1][0],dejmps_contour_data[2][90],markers[0],markersize=2,color=colors[0],label=labels[0])
plt.plot(bbpssw_contour_data[1][0],bbpssw_contour_data[2][90],markers[1],markersize=2,color=colors[1],label=labels[1],linewidth=1)
plt.plot(three_to_one_contour_data[1][0],three_to_one_contour_data[2][90],markers[2],markersize=2,color=colors[2],label=labels[2])
plt.grid()
plt.legend()
plt.xlabel("Input state fidelity")
plt.ylabel("Ratio of input and output state fidelity")
plt.xticks(ticks)
plt.subplots_adjust(0.11,0.112,0.995,0.995)


titles.append("Expected increase at p100")
plt.figure("Expected increase at p100")
plt.axhline(0,color="black",linewidth=1)
plt.plot(*expected_relative_increase(dejmps_contour_data[1][0],dejmps_contour_data[2][100],dejmps_p_success_data[2],2),markers[0],markersize=2,color=colors[0],label=labels[0])
plt.plot(*expected_relative_increase(bbpssw_contour_data[1][0],bbpssw_contour_data[2][100],bbpssw_p_success_data[2],2),markers[1],markersize=2,color=colors[1],label=labels[1],linewidth=1)
plt.plot(*expected_relative_increase(three_to_one_contour_data[1][0],three_to_one_contour_data[2][100],three_to_one_p_success_data[2],3),markers[2],markersize=2,color=colors[2],label=labels[2])
plt.grid()
plt.legend()
plt.xlabel("Input state fidelity")
plt.ylabel("Expected relative increase of fidelity (%)")
plt.xticks(ticks)
plt.subplots_adjust(0.12,0.112,0.995,0.995)


titles.append("Expected increase at p0.99")
plt.figure("Expected increase at p0.99")
plt.axhline(0,color="black",linewidth=1)
plt.plot(*expected_relative_increase(dejmps_contour_data[1][0],dejmps_contour_data[2][90],dejmps_p_success_data[1],2),markers[0],markersize=2,color=colors[0],label=labels[0])
plt.plot(*expected_relative_increase(bbpssw_contour_data[1][0],bbpssw_contour_data[2][90],bbpssw_p_success_data[1],2),markers[1],markersize=2,color=colors[1],label=labels[1],linewidth=1)
plt.plot(*expected_relative_increase(three_to_one_contour_data[1][0],three_to_one_contour_data[2][90],three_to_one_p_success_data[1],3),markers[2],markersize=2,color=colors[2],label=labels[2])
plt.grid()
plt.legend()
plt.xlabel("Input state fidelity")
plt.ylabel("Expected relative increase of fidelity (%)")
plt.xticks(ticks)
plt.subplots_adjust(0.12,0.112,0.995,0.995)

figs = [n for n in plt.get_fignums()]
for n in figs:
    fig = plt.figure(n)
    fig.savefig(f"plots/{titles[n-1]}.eps", format='eps')

plt.show()
