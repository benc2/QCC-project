from three_to_one import three_to_one_protocol_alice
from netqasm.sdk import EPRSocket
from netqasm.sdk.external import NetQASMConnection, Socket

def main(app_config=None):

    # Create a socket for classical communication

    socket = Socket("alice","bob")

    # Create a EPR socket for entanglement generation
    epr_socket = EPRSocket("bob")


    # Initialize Alice's NetQASM connection
    alice = NetQASMConnection(
        app_name=app_config.app_name,
        epr_sockets=[epr_socket]
    )
    # Create Alice's context, initialize EPR pairs inside it and call Alice's 3->1 method. Finally, print out whether or not Alice successfully created an EPR Pair with Bob.
    with alice:
        epr1 = epr_socket.create()[0]
        alice.flush()
        print(f"Alice has created the first EPR pair")
        epr2 = epr_socket.create()[0]
        alice.flush()
        print(f"Alice has created the second EPR pair")
        epr3 = epr_socket.create()[0]
        alice.flush()
        print(f"Alice has created the third EPR pair")
        #depolarize (step 1)
        pass
        #alice performs her gates
        success = three_to_one_protocol_alice(epr1,epr2,epr3,alice,socket)


    if success:
        print("Alice has kept the third qubit.")
    else:
        print("Alice has discarded the third qubit")

    return False

if __name__ == "__main__":
    main()
