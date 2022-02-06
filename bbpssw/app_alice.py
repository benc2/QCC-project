from bbpssw import bbpssw_protocol_alice
from netqasm.sdk import EPRSocket
from netqasm.sdk.external import NetQASMConnection, Socket, get_qubit_state
import numpy as np

def main(app_config=None):
    # Create a socket for classical communication
    socket = Socket("alice","bob")

    # Create a EPR socket for entanglement generation
    epr_socket = EPRSocket("bob",min_fidelity=80)

    # Initialize Alice's NetQASM connection
    alice = NetQASMConnection(
        app_name=app_config.app_name,
        epr_sockets=[epr_socket]
    )

    # Create Alice's context, initialize EPR pairs inside it and call Alice's BBPSSW method. Finally, print out whether or not Alice successfully created an EPR Pair with Bob.
    with alice:
        q1 = epr_socket.create(1)[0]
        alice.flush()
        original_dm = get_qubit_state(q1, reduced_dm=False)
        alice.flush()
        q2 = epr_socket.create(1)[0]

        success = bbpssw_protocol_alice(q1, q2, alice, socket)

        dm = get_qubit_state(q1, reduced_dm=False)
        alice.flush()

        phi00 = np.array([1, 0, 0, 1]) / np.sqrt(2)
        F_in = phi00.T @ original_dm @ phi00
        F_out = phi00.T @ dm @ phi00
        if success:
            print("Success! Alice keeps q1")
        else:
            print("Failure! Alice discards q1")
        print(f"The input fidelity was {np.real(F_in)}")
        print(f"The output fidelity is {np.real(F_out)}")
        return

if __name__ == "__main__":
    main()
