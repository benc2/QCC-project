import numpy as np
from netqasm.sdk import EPRSocket
from netqasm.sdk.external import NetQASMConnection, Socket, get_qubit_state
from netqasm.sdk.toolbox.sim_states import qubit_from, to_dm, get_fidelity


def main(app_config=None):
    # following the original DEJMPS paper https://arxiv.org/pdf/quant-ph/9604039.pdf
    log_config = app_config.log_config

    # Create a socket to recv classical information
    socket = Socket("receiver", "sender", log_config=log_config)

    # Create a EPR socket for entanglement generation
    epr_socket = EPRSocket("sender")
    # epr_socket2 = EPRSocket("sender", 2)

    # Initialize the connection
    receiver = NetQASMConnection(
        app_name=app_config.app_name,
        log_config=log_config,
        epr_sockets=[epr_socket]
    )
    with receiver:
        epr1, epr2 = epr_socket.recv(number=2)  # receive the 2 qubits from Alice
        print("Bob received the qubits from Alice")
        # receiver.flush()
        # print("flushed")

        epr1.rot_X(3)  # in units of pi/2, 3pi/2 = -pi/2 mod 2pi
        epr2.rot_X(3)
        epr1.cnot(epr2)
        print("Bob applied his gates")
        receiver_outcome = int(epr2.measure())
        print(f"Bob measured {receiver_outcome}")
        # Get the corrections
        sender_outcome = socket.recv_structured().payload
        print(f"Bob received outcome {sender_outcome} from Alice")
        if sender_outcome == receiver_outcome:
            print(f"Success! Alice and Bob both measured {sender_outcome}")
        else:
            print(f"Failure! Alice measured {sender_outcome }, but Bob both measured {receiver_outcome}")
        # if m2 == 1:
        #     print("`receiver` will perform X correction")
        #     epr.X()
        # if m1 == 1:
        #     print("`receiver` will perform Z correction")
        #     epr.Z()

        receiver.flush()
        # Get the qubit state
        # NOTE only possible in simulation, not part of actual application
        # dm = get_qubit_state(epr1)
        # print(f"`receiver` recieved the teleported state {dm}")

        # Reconstruct the original qubit to compare with the received one
        # NOTE only to check simulation results, normally the Sender does not
        # need to send the phi and theta values!
        # msg = socket.recv_silent()  # don't log this
        # phi, theta = eval(msg)
        #
        # original = qubit_from(phi, theta)
        # original_dm = to_dm(original)
        # fidelity = get_fidelity(original, dm)

        # return {
        #     "original_state": original_dm.tolist(),
        #     "correction1": "Z" if m1 == 1 else "None",
        #     "correction2": "X" if m2 == 1 else "None",
        #     "received_state": dm.tolist(),
        #     "fidelity": fidelity
        # }


if __name__ == "__main__":
    main()
