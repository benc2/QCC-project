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

    print("`sender` will start to teleport a qubit to `receiver`")

    # Initialize the connection to the backend
    sender = NetQASMConnection(
        app_name=app_config.app_name,
        log_config=log_config,
        epr_sockets=[epr_socket]
    )
    with sender:
        # Create a qubit to teleport
        q = Qubit(sender)

        # set_qubit_state(q, phi, theta)
        epr= Qubit(sender)
        sender.flush()
        q.cnot(epr)
        # q.cnot(epr)
        # q.cnot(epr)
        # q.cnot(epr)

        # epr.X()
        # epr.X()
        sender.flush()
        dm = get_qubit_state(q, reduced_dm=False)
        dm2 = get_qubit_state(epr, reduced_dm=False)
        sender.flush()
        socket.send("")
        # Create EPR pairs
        for ii in range(1):
            epr.measure()
            sender.flush()
            epr = epr_socket.create()[0]

            sender.flush()
            sender.flush()
            # print(ii)100
            socket.send("")

        # Teleport
        q.cnot(epr)
        q.H()
        m1 = q.measure()
        m2 = epr.measure()

    # Send the correction information
    m1, m2 = int(m1), int(m2)

    app_logger.log(f"m1 = {m1}")
    app_logger.log(f"m2 = {m2}")
    # print(f"`sender` measured the following teleportation corrections: m1 = {m1}, m2 = {m2}")
    # print("`sender` will send the corrections to `receiver`")

    socket.send_structured(StructuredMessage("Corrections", (m1, m2)))

    socket.send_silent(str((phi, theta)))
    phi = np.array([1, 0, 0, 0])
    print(phi.T @ dm @ phi)
    print(dm)
    print(dm2)

    return {
        "m1": m1,
        "m2": m2
    }


if __name__ == "__main__":
    main()
