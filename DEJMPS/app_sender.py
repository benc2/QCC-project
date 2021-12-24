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
    # epr_socket2 = EPRSocket("receiver", 2)

    print("Starting DEJMPS protocol")

    # Initialize the connection to the backend
    sender = NetQASMConnection(
        app_name=app_config.app_name,
        log_config=log_config,
        epr_sockets=[epr_socket]
    )
    with sender:
        # Create a qubit to teleport
        q = Qubit(sender)
        set_qubit_state(q, phi, theta)

        # Create EPR pairs
        epr1, epr2 = epr_socket.create(number=2)  # create 2 EPR pairs
        print("Created EPR pairs")
        # Teleport
        epr1.rot_X(1)  # in units of pi/2
        epr2.rot_X(1)
        epr1.cnot(epr2)
        print("Alice applied her gates")
        # sender.flush()
        sender_outcome = int(epr2.measure())
        print(f"Alice measured {sender_outcome}")

    # app_logger.log(f"m1 = {m1}")
    # app_logger.log(f"m2 = {m2}")
    # print(f"`sender` measured the following teleportation corrections: m1 = {m1}, m2 = {m2}")
    # print("`sender` will send the corrections to `receiver`")
    print(f"Alice measured {sender_outcome}")

    socket.send_structured(StructuredMessage("Corrections", sender_outcome))

    # socket.send_silent(str((phi, theta)))

    # return {
    #     "m1": m1,
    #     "m2": m2
    # }


if __name__ == "__main__":
    main()
