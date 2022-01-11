import numpy as np
from netqasm.sdk import Qubit, EPRSocket
from netqasm.sdk.external import NetQASMConnection, Socket, get_qubit_state
from netqasm.sdk.toolbox import set_qubit_state
from netqasm.logging.output import get_new_app_logger
from netqasm.sdk.classical_communication.message import StructuredMessage

def main(app_config=None, phi=0., theta=0.):
    log_config = app_config.log_config
    app_logger = get_new_app_logger(app_name="sender", log_config=log_config)

    # Create a socket to send classical information
    socket = Socket("sender", "receiver", log_config=log_config)

    # Create a EPR socket for entanglement generation
    epr_socket = EPRSocket("receiver")

    print("Starting DEJMPS protocol")

    # Initialize the connection to the backend
    sender = NetQASMConnection(
        app_name=app_config.app_name,
        log_config=log_config,
        epr_sockets=[epr_socket]
    )
    N = 3
    epr_list = epr_socket.create(number=N+1)
    success = False
    for i in range(N):
        sender.flush()
        print(f"iteration {i+1}")
        with sender:
            # Create EPR pairs
            print(f"Alice: success={success}")
            # if not success:
            #     epr1 = epr_socket.create()[0]  # note: in the paper, Eve makes the pairs
            # print("Alice sent first pair")
            # sender.flush()
            # original_dm = get_qubit_state(epr1, reduced_dm=False)
            # epr2 = epr_socket.create()[0]

            epr1 = epr_list[0]
            original_dm = get_qubit_state(epr1, reduced_dm=False)
            epr2 = epr_list[i+1]
            print("After receive")
            sender.flush()
            print("Alice has created the EPR pairs")
            sender.flush()
            epr1.rot_X(1)  # in units of pi/2
            epr2.rot_X(1)
            epr1.cnot(epr2)
            print("Alice applied her gates")
            sender.flush()
            sender_outcome = epr2.measure()
            sender.flush()  # flush only for print
            print(f"Alice measured {sender_outcome}")
            dm = get_qubit_state(epr1, reduced_dm=False)

            # Send the correction information

            socket.send_structured(StructuredMessage("Corrections", sender_outcome))
            print(f"Alice sent her outcome {sender_outcome} to Bob")
            sender.flush()

            phi00 = np.array([1, 0, 0, 1]) / np.sqrt(2)
            F_in = phi00.T @ original_dm @ phi00
            F_out = phi00.T @ dm @ phi00
            print(f"F_in: {np.real(F_in)}, F_out: {np.real(F_out)}")
            success = socket.recv_structured().payload
            if not success:
                quit()
            sender.flush()
            print("Alice tries to free")
            # epr2.free()
            # sender.flush()
            # if not success:
            #     print("Not free")
            #     epr1.free()
            #     print("Free")
            # print("flush?")
            # sender.flush()
            # print("flush!")

if __name__ == "__main__":
    main()
