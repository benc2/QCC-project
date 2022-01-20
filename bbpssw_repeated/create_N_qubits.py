number_of_qubits = 2 ** 5
qubits = "    qubits:\n"
for n in range(number_of_qubits):
    qubits += f"      - id: {n}\n        t1: 0\n        t2: 0\n"


    fin = open("network_template.yaml", "rt")
    fout = open("network_with_qubits_template.yaml", "wt")

    # Update the fidelity in network.yaml
    for line in fin:
        # read replace the string and write to output file
        fout.write(line.replace('    qubits:', qubits))
    fin.close()
    fout.close()

