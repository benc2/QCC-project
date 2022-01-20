from bbpssw import bbpssw_protocol_bob
from netqasm.sdk import EPRSocket
from netqasm.sdk.external import NetQASMConnection, Socket, get_qubit_state
import numpy as np
def main(app_config=None):
    # Create a socket for classical communication
    socket=Socket("bob","alice")

    N= 3


    # Create a EPR socket for entanglement generation
    epr_socket=EPRSocket("alice") #, min_fidelity=50)

    # Initialize Bob's NetQASM connection
    bob = NetQASMConnection(
        app_name=app_config.app_name,
        epr_sockets=[epr_socket],
        max_qubits=2**(N+2)
    )

    # Create Bob's context, initialize EPR pairs inside it and call Bob's BBPSSW method. Finally, print out whether or not Bob successfully created an EPR Pair with Alice.
    with bob:
        q1 = epr_socket.recv(number = 1)[0]
        bob.flush()
        q1.measure()
        bob.flush()
        eprs = epr_socket.recv(2**N)
        bob.flush()
        while len(eprs)>=2:

            better_eprs = []
            socket.recv()

            socket.send(f"Yes, I'm ready Alice, most certainly!")
            for i in range(1):#int(np.floor(len(eprs)/2))):

                if bbpssw_protocol_bob(eprs[2*i], eprs[2*i+1], bob, socket):
                    # print(f"Round {n+1}, qubit pair {i}, Bob keeps q1")
                    better_eprs.append(eprs[2*i])
                    pass
                else:
                    eprs[2 * i].measure()
                    bob.flush()
                    # print(f"Round {n+1}, qubit pair {i}, Bob destroys q1")
                    pass

            eprs = better_eprs
            bob.flush()

        success = len(eprs)>0
        if len(eprs)>1:
            print("Bob is destroying qubits")
            k= 1
            while k<len(eprs):
                eprs[k].measure()
                k+=1
        bob.flush()
        socket.send("Hey Alice, I destroyed the superfluous qubits.")
        socket.recv()

if __name__ == "__main__":
    main()
