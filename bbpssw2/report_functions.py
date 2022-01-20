from multiprocessing import Pool
import os
from time import sleep

def prepare_network_at_given_link_fidelity(link_fidelity):
    fidelity_parameter = (4 * link_fidelity - 1) / 3
    # Load the networl.yaml and the template file
    fin = open("network_template.yaml", "rt")
    fout = open("network.yaml", "wt")

    # Update the fidelity in network.yaml
    for line in fin:
        # read replace the string and write to output file
        fout.write(line.replace('    fidelity: 1.0', '    fidelity: ' + str(fidelity_parameter)))
    fin.close()
    fout.close()

def n_attempts_with_given_fidelity(n,fidelity):
    prepare_network_at_given_link_fidelity(fidelity)

    # Run netqasm simulation and store the result as an array
    pool = Pool(processes=n)
    rg = range(n)
    while True:
        try:
            output,dummy = zip(*pool.map(attempt_purification, rg))

            break
        except IndexError:
            print("Retry")
        except ValueError:
            print("Retry")
    return output

def attempt_purification(i=0):
    sleep(i/3)
    d = os.popen('netqasm simulate --formalism dm --log-to-files FALSE').read().split("\n")
    print(f"Attempt {i} finished with fidelity {d[2]}")
    return d[0]=="True",float(d[2])

def determine_required_purification_tree_length(start_fidelity , target_fidelity):
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
