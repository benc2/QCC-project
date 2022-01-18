from report_functions import determine_required_purification_tree_length, n_attempts_with_given_fidelity
import numpy as np

# Set a start fidelity (=link fidelity) and target fidelity in range (0.25,1)

start_fidelity = 0.8
target_fidelity = 0.9

step_fidelities = determine_required_purification_tree_length(start_fidelity,target_fidelity)
tree_length = len(step_fidelities)
print(tree_length)
print(step_fidelities)
prepared_qubits = []
for ii, fidelity in enumerate(step_fidelities):
    prepared_qubits.append([])
    # print(prepared_qubits)

measurements = []
while len(measurements) < 100:
    epr_pairs_consumed = 0

    qubit_register = np.zeros(tree_length)
    level = 0

    while qubit_register[tree_length - 1] == 0:
        if not prepared_qubits[level]:
            prepared_qubits[level] = list(n_attempts_with_given_fidelity(8, step_fidelities[level]))
        # print(f"Creating a level {level} epr-pair")
        pair = prepared_qubits[level].pop()
        epr_pairs_consumed += 1  # Every time an epr-pair is used, we discard at least one qubit.
        if pair:
            # print("Succeeded")
            qubit_register[level] += 1
        else:
            # print("Failed")
            # sleep(1)
            epr_pairs_consumed += 1  # On failure we discard another one.
        if level > 0:
            qubit_register[level - 1] = 0
        if qubit_register[level] == 2:
            level += 1
        else:
            level = 0

        print(
            f"{len(measurements) + 1}. {pair}. Consumed {epr_pairs_consumed} epr pairs, register state: {qubit_register}")

    measurements.append(epr_pairs_consumed)
    print(
        f"{len(measurements)} pairs have been created. Average number of used/discarded pairs: {np.mean(measurements)}, St. dev: {np.std(measurements)}")
