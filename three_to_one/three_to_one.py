import math
from netqasm.sdk.classical_communication.message import StructuredMessage


def three_to_one_protocol_alice(q1, q2, q3, alice, socket):
    """
    Implements Alice's side of the BBPSSW distillation protocol.
    This function should perform the gates and measurements for 3->1 using
    qubits q1 and q2, then send the measurement outcome to Bob and determine
    if the distillation was successful.
    
    :param q1: Alice's qubit from the first entangled pair
    :param q2: Alice's qubit from the second entangled pair
    :param q3: Alice's qubit from the third entangled pair
    :param alice: Alice's NetQASMConnection
    :param socket: Alice's classical communication socket to Bob
    :return: True/False indicating if protocol was successful
    """

    outcome1, outcome2 = three_to_one_gates_and_measurement_alice(q1, q2, q3)

    alice.flush()
    print("Alice flushed and got outcomes", outcome1, outcome2)
    # Write below the code to send measurement result to Bob, receive measurement result from Bob and check if protocol was successful
    socket.send_structured(StructuredMessage("My measurement results from qubit 1 and 2 are", (outcome1, outcome2)))
    outcome1_bob, outcome2_bob = socket.recv_structured().payload

    if[outcome1,outcome2]==[outcome1_bob,outcome2_bob]:
        return True
    else:
        return False


def three_to_one_gates_and_measurement_alice(q1, q2, q3):
    """
    Performs the gates and measurements for Alice's side of the 3->1 protocol
    :param q1: Alice's qubit from the first entangled pair
    :param q2: Alice's qubit from the second entangled pair
    :param q3: Alice's qubit from the third entangled pair
    :return: A pair of integer 0/1 indicating Alice's measurement outcomes from measuring the qubits
    """
    q3.cnot(q2)
    q1.cnot(q3)
    print("Alice has applied gates")
    #bell measureent of q1 and q2
    q1.cnot(q2)
    outcome1 = q1.measure()
    outcome2 = q2.measure()
    print("Alice has applied measurements")
    return outcome1, outcome2



def three_to_one_protocol_bob(q1, q2, q3, bob, socket):
    """
    Implements Bob's side of the 3->1 distillation protocol.
    This function should perform the gates and measurements for 3->1 using
    qubits q1 and q2, then send the measurement outcome to Alice and determine
    if the distillation was successful.
    
    :param q1: Bob's qubit from the first entangled pair
    :param q2: Bob's qubit from the second entangled pair
    :param q3: Bob's qubit from the third entangled pair
    :param bob: Bob's NetQASMConnection
    :param socket: Alice's classical communication socket to Bob
    :return: True/False indicating if protocol was successful
    """

    outcome1, outcome2 = three_to_one_gates_and_measurement_bob(q1, q2,q3)  #Why was q3 here not in the template???????

    bob.flush()
    print("Bob has flushed and got outcomes",outcome1,outcome2)
    outcome1_alice, outcome2_alice = socket.recv_structured().payload

    # Write below the code to send measurement result to Alice, receive measurement results from Alice and check if protocol was successful
    socket.send_structured(StructuredMessage("My measurement results from qubit 1 and 2 are", (outcome1, outcome2)))
    if [outcome1, outcome2] == [outcome1_alice, outcome2_alice]:
        return True
    else:
        return False

def three_to_one_gates_and_measurement_bob(q1, q2,q3):   #Why was q3 here not in the template???????
    """
    Performs the gates and measurements for Bob's side of the 3->1 protocol
    :param q1: Bob's qubit from the first entangled pair
    :param q2: Bob's qubit from the second entangled pair
    :param q3: Bob's qubit from the third entangled pair
    :return: A pair of integer 0/1 indicating Bob's measurement outcomes from measuring the qubits
    """
    q3.cnot(q2)
    q1.cnot(q3)
    print("Bob has applied gates")
    #bell measureent of q1 and q2
    q1.cnot(q2)
    outcome1 = q1.measure()
    outcome2 = q2.measure()
    print("Bob has applied measurements")

    return outcome1, outcome2
