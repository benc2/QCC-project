from bbpssw import bbpssw_protocol_bob
from netqasm.sdk import EPRSocket
from netqasm.sdk.external import NetQASMConnection, Socket, get_qubit_state

def main(app_config=None):
    # Create a socket for classical communication
    socket=Socket("bob","alice")




    # Create a EPR socket for entanglement generation
    epr_socket=EPRSocket("alice") #, min_fidelity=50)

    # Initialize Bob's NetQASM connection
    bob = NetQASMConnection(
        app_name=app_config.app_name,
        epr_sockets=[epr_socket]
    )

    # Create Bob's context, initialize EPR pairs inside it and call Bob's BBPSSW method. Finally, print out whether or not Bob successfully created an EPR Pair with Alice.
    with bob:
        q1 = epr_socket.recv(number = 1)[0]
        bob.flush()
        q2 = epr_socket.recv()[0]
        if bbpssw_protocol_bob(q1, q2, bob, socket):
            print("Bob keeps q1")
        else:
            print("Bob destroys q1")

if __name__ == "__main__":
    main()
