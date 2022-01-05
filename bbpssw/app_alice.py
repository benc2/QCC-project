from bbpssw import bbpssw_protocol_alice
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

    # Create Alice's context, initialize EPR pairs inside it and call Alice's BBPSSW method. Finally, print out whether or not Alice successfully created an EPR Pair with Bob.
    with alice:
        q1, q2 = epr_socket.create(2)
        # We moeten een Psi_- staat hebben, maar die wordt daarna omgezet naar een Phi_+ staat. Ik denk dat create() een Phi_+ maakt? dus dan hoeven we niks om te zetten. Maar helemaal zeker weet ik het niet
        alice.flush()
        print(f"Alice has created two epr pairs")
        success = bbpssw_protocol_alice(q1, q2, alice, socket)
        if success:
            print("Alice has kept the second qubit.")
        else:
            print("Alice has discarded the second qubit")
if __name__ == "__main__":
    main()
