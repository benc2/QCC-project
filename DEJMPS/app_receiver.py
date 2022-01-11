from netqasm.sdk import EPRSocket
from netqasm.sdk.external import NetQASMConnection, Socket, get_qubit_state
from netqasm.sdk.toolbox.sim_states import qubit_from, to_dm, get_fidelity
from netqasm.sdk.classical_communication.message import StructuredMessage

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
    success = False
    N = 3
    epr_list = epr_socket.recv(number=N+1)
    for i in range(N):
        print("begin of loop Bob")
        with receiver:
            print("Before receive")
            print(f"Bob: success={success}")
            # if not success:
            #     epr1 = epr_socket.recv()[0]
            epr1 = epr_list[0]
            epr2 = epr_list[i+1]
            print("After receive")
            receiver.flush()
            # epr2 = epr_socket.recv()[0]
            print("Bob has received the EPR pairs")
            # receiver.flush()


            # print(f"Bob received outcome {sender_outcome} from Alice")
            epr1.rot_X(3)  # in units of pi/2, 3pi/2 = -pi/2 mod 2pi
            epr2.rot_X(3)
            epr1.cnot(epr2)
            print("Bob applied his gates")
            receiver.flush()
            receiver_outcome = epr2.measure()
            receiver.flush()
            print(f"Bob measured {receiver_outcome}")
            sender_outcome = socket.recv_structured().payload
            receiver.flush()
            print(f"Bob received outcome {sender_outcome} from Alice")

        success = sender_outcome == receiver_outcome
        if success:
            print(f"Success! Alice and Bob both measured {sender_outcome}")
        else:
            print(f"Failure! Alice measured {sender_outcome }, but Bob measured {receiver_outcome}")

            # receiver.flush()
        socket.send_structured(StructuredMessage("Success?", success))
        receiver.flush()
        print("End of loop Bob")
        print("Bob tries to free")
        # epr2.free()
        # receiver.flush()
        # if not success:
        #     epr1.free()
        # receiver.flush()

if __name__ == "__main__":
    main()
