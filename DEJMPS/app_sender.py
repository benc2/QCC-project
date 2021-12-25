from netqasm.sdk import Qubit, EPRSocket
from netqasm.sdk.external import NetQASMConnection, Socket
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

    print("Starting (1 iteration of) DEJMPS protocol")

    # Initialize the connection to the backend
    sender = NetQASMConnection(
        app_name=app_config.app_name,
        log_config=log_config,
        epr_sockets=[epr_socket]
    )
    sender.flush()
    with sender:
        # Create EPR pairs
        epr1, epr2 = epr_socket.create(number=2)  # note: in the paper, Eve makes the pairs and they are not
        print("Alice has created the EPR pairs")  # necessarily EPR pairs
        sender.flush()
        epr1.rot_X(1)  # in units of pi/2
        epr2.rot_X(1)
        epr1.cnot(epr2)
        print("Alice applied her gates")
        sender.flush()
        sender_outcome = epr2.measure()
        sender.flush()  # flush only for print
        print(f"Alice measured {sender_outcome}")

    # Send the correction information

    socket.send_structured(StructuredMessage("Corrections", sender_outcome))
    print(f"Alice sent her outcome {sender_outcome} to Bob")
    sender.flush()


if __name__ == "__main__":
    main()
