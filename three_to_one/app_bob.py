from three_to_one import three_to_one_protocol_bob
from netqasm.sdk import EPRSocket
from netqasm.sdk.external import NetQASMConnection, Socket, get_qubit_state

def main(app_config=None):
    
    # Create a socket for classical communication
    socket = Socket("alice","bob")

    # Create a EPR socket for entanglement generation
    epr_socket = EPRSocket("alice")

    # Initialize Bob's NetQASM connection
    bob = NetQASMConnection(
        app_name=app_config.app_name,
        epr_sockets=[epr_socket]
    )

    # Create Bob's context, initialize EPR pairs inside it and call Bob's 3->1 method. Finally, print out whether or not Bob successfully created an EPR Pair with Alice.
    with bob:
        epr1, epr2, epr3 = EPRSocket.recv()[0]
        bob.flush()

        success = three_to_one_protocol_bob(epr1,epr2,epr3,bob,socket)

        if success:
            print("Bob has kept the third qubit.")
        else:
            print("Bob has discarded the third qubit")

if __name__ == "__main__":
    main()
