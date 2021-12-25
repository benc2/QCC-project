from netqasm.sdk import EPRSocket
from netqasm.sdk.external import NetQASMConnection, Socket, get_qubit_state
from netqasm.sdk.toolbox.sim_states import qubit_from, to_dm, get_fidelity


def main(app_config=None):
    log_config = app_config.log_config

    # Create a socket to recv classical information
    socket = Socket("receiver", "sender", log_config=log_config)

    # Create a EPR socket for entanglement generation
    epr_socket = EPRSocket("sender")

    # Initialize the connection
    receiver = NetQASMConnection(
        app_name=app_config.app_name,
        log_config=log_config,
        epr_sockets=[epr_socket]
    )
    with receiver:
        epr1, epr2 = epr_socket.recv(number=2)
        print("Bob has received the EPR pairs")
        receiver.flush()


        # print(f"Bob received outcome {sender_outcome} from Alice")
        epr1.rot_X(3)  # in units of pi/2, 3pi/2 = -pi/2 mod 2pi
        epr2.rot_X(3)
        epr1.cnot(epr2)
        print("Bob applied his gates")
        receiver.flush()
        receiver_outcome = epr2.measure()
        receiver.flush()
        sender_outcome = socket.recv_structured().payload
        receiver.flush()
        print(f"Bob received outcome {sender_outcome} from Alice")
        print(f"Bob measured {receiver_outcome}")

    if sender_outcome == receiver_outcome:
        print(f"Success! Alice and Bob both measured {sender_outcome}")
    else:
        print(f"Failure! Alice measured {sender_outcome }, but Bob measured {receiver_outcome}")


if __name__ == "__main__":
    main()
