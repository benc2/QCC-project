import math

import numpy as np
from netqasm.sdk.classical_communication.message import StructuredMessage
from netqasm.sdk.toolbox import set_qubit_state


def bbpssw_protocol_alice(q1, q2, alice, socket, last = True):
    """
    Implements Alice's side of the BBPSSW distillation protocol.
    This function should perform the gates and measurements for BBPSSW using
    qubits q1 and q2, then send the measurement outcome to Bob and determine
    if the distillation was successful.
    
    :param q1: Alice's qubit from the first entangled pair
    :param q2: Alice's qubit from the second entangled pair
    :param alice: Alice's NetQASMConnection
    :param socket: Alice's classical communication socket to Bob
    :return: True/False indicating if protocol was successful
    """
    a = bbpssw_gates_and_measurement_alice(q1, q2)
    alice.flush()
    a = int(a)
    # Write below the code to send measurement result to Bob, receive measurement result from Bob and check if protocol was successful
    socket.send_structured(StructuredMessage("Hey Bob I measured",a))
    b = socket.recv_structured().payload
    perform_random_rotation_alice(q1, socket, last)
    alice.flush()
    return a == b


def bbpssw_gates_and_measurement_alice(q1, q2):
    """
    Performs the gates and measurements for Alice's side of the BBPSSW protocol
    :param q1: Alice's qubit from the first entangled pair
    :param q2: Alice's qubit from the second entangled pair
    :return: Integer 0/1 indicating Alice's measurement outcome
    """
    q1.cnot(q2)
    m = q2.measure()
    return m


def bbpssw_protocol_bob(q1, q2, bob, socket):
    """
    Implements Bob's side of the BBPSSW distillation protocol.
    This function should perform the gates and measurements for BBPSSW using
    qubits q1 and q2, then send the measurement outcome to Alice and determine
    if the distillation was successful.
    
    :param q1: Bob's qubit from the first entangled pair
    :param q2: Bob's qubit from the second entangled pair
    :param bob: Bob's NetQASMConnection
    :param socket: Alice's classical communication socket to Bob
    :return: True/False indicating if protocol was successful
    """
    b = bbpssw_gates_and_measurement_bob(q1, q2)
    bob.flush()
    b = int(b)
    # Write below the code to send measurement result to Alice, receive measurement result from Alice and check if protocol was successful
    socket.send_structured(StructuredMessage("Hey Alice, I measured",b))
    a = socket.recv_structured().payload
    perform_random_rotation_bob(q1,socket)
    bob.flush()
    return a == b


def bbpssw_gates_and_measurement_bob(q1, q2):
    """
    Performs the gates and measurements for Bob's side of the BBPSSW protocol
    :param q1: Bob's qubit from the first entangled pair
    :param q2: Bob's qubit from the second entangled pair
    :return: Integer 0/1 indicating Bob's measurement outcome
    """
    q1.cnot(q2)
    # q2.H()
    m = q2.measure()

    return m

def perform_random_rotation_alice(q1,socket, last):
    if last:
        theta =0
        phi = 0
    else:
        theta = np.random.uniform(0,np.pi)
        phi = np.random.uniform(0,2*np.pi)
        q1.H()
        # set_qubit_state(q1,phi,theta)
        # q1.rot_Z(angle=phi)
        # q1.rot_X(angle=theta)
    socket.send_structured(StructuredMessage("Theta and phi:",(theta,phi)))


def perform_random_rotation_bob(q1,socket):
    theta ,    phi =     socket.recv_structured().payload
    # q1.rot_Z(angle=phi)
    # q1.rot_X(angle=theta)