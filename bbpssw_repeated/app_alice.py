from bbpssw import bbpssw_protocol_alice
from netqasm.sdk import EPRSocket
from netqasm.sdk.external import NetQASMConnection, Socket, get_qubit_state
import numpy as np

def main(app_config=None):
    # Create a socket for classical communication
    socket = Socket("alice","bob")
    N = 2
    # Create a EPR socket for entanglement generation
    epr_socket = EPRSocket("bob",min_fidelity=80)

    # Initialize Alice's NetQASM connection
    alice = NetQASMConnection(
        app_name=app_config.app_name,
        epr_sockets=[epr_socket],
        max_qubits=2 ** (N+2)
    )

    # Create Alice's context, initialize EPR pairs inside it and call Alice's BBPSSW method. Finally, print out whether or not Alice successfully created an EPR Pair with Bob.
    with alice:
        q1 = epr_socket.create(1)[0]
        # q1.rot_X(angle=1)
        info =q1.entanglement_info
        alice.flush()
        # print(info)
        original_dm = get_qubit_state(q1, reduced_dm=False)
        # print(original_dm)
        alice.flush()
        q1.measure()
        alice.flush()
        eprs = epr_socket.create(2**N)
        # q2.rot_X(angle=1)
        for n in range(N):
            better_eprs = []
            socket.send(f"Hey Bob, I'm starting round {n+1}. Aryou ready to measure?")
            socket.recv()
            for i in range(int(np.floor(len(eprs)/2))):

                if bbpssw_protocol_alice(eprs[2*i], eprs[2* i + 1], alice, socket):
                    print(f"Round {n+1}, qubit pair {i}, Alice keeps q1")
                    better_eprs.append(eprs[2 * i])
                    pass
                else:
                    eprs[2  * i].measure()
                    print(f"Round {n+1}, qubit pair {i}, Alice discards q1")

            eprs = better_eprs
            alice.flush()
            print(f"There are {len(eprs)} pairs left")
        success = len(eprs)>0
        # success = bbpssw_protocol_alice(q1, q2, alice, socket)
        # if bbpssw_protocol_alice(q1, q2, alice, socket):
        #     pass
        #     # print("Alice keeps q1")
        #
        #
        # else:
        #     # print("Alice discards q1")
        #
        k= 1
        while k<len(eprs):
            eprs[k].measure()
            k+=1
        alice.flush()
        socket.recv()
        if success:

            dm = get_qubit_state(eprs[0], reduced_dm=False)

            alice.flush()

            # print(dm)
            phi00 = np.array([1, 0, 0, 1]) / np.sqrt(2)
            F_in = phi00.T @ original_dm @ phi00
            F_out = phi00.T @ dm @ phi00
            print(success)
            print(np.real(F_in))
            print(np.real(F_out))

        else:
            print("Too bad, failure.")

        socket.send("")


if __name__ == "__main__":
    main()
