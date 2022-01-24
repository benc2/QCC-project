import numpy as np
from dejmps import dejmps_protocol_alice
from netqasm.sdk import EPRSocket
from netqasm.sdk.external import NetQASMConnection, Socket, get_qubit_state


def dm_fidelity(dm, flipped=False):
    phi_00 = np.array([1,0,0,1])/np.sqrt(2)
    if flipped:  # when netqasm changes qubit order
        phi_00 = np.array([0,1,1,0])/np.sqrt(2)
    return np.real(phi_00 @ dm @ phi_00)


def main(app_config=None):

    # Create a socket for classical communication
    socket = Socket("alice", "bob")

    # Create a EPR socket for entanglement generation
    epr_socket = EPRSocket("bob")

    # Initialize Alice's NetQASM connection
    alice = NetQASMConnection(app_name=app_config.app_name,
                              epr_sockets=[epr_socket])

    # Create Alice's context, initialize EPR pairs inside it and call Alice's DEJMPS method. Finally, print out whether or not Alice successfully created an EPR Pair with Bob.
    with alice:
        q1 = epr_socket.create()[0]
        alice.flush()
        f_init = dm_fidelity(get_qubit_state(q1, reduced_dm=False))
        q2 = epr_socket.create()[0]
        success = dejmps_protocol_alice(q1, q2, alice, socket)
        bob_success = socket.recv_structured().payload
        # print("Success?", success, bob_success)
        alice.flush()
        # print("Agree?", success == bob_success)
        f_out = dm_fidelity(get_qubit_state(q1, reduced_dm=False), flipped=True)
        # print(np.round(get_qubit_state(q1, reduced_dm=False), 2))
        print(int(success == bob_success), f_init, f_out)


if __name__ == "__main__":
    main()
