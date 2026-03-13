import random
from cqc.pythonLib import CQCConnection, qubit

def main():
    # Initialize the connection
    with CQCConnection("Alice") as Alice:
        num_bits = 100
        bits = [random.randint(0, 1) for _ in range(num_bits)]
        bases = [random.randint(0, 1) for _ in range(num_bits)]

        print(f"Alice: Generated {num_bits} bits and bases.")

        # Send qubits to Eve
        for i in range(num_bits):
            q = qubit(Alice)
            if bits[i] == 1:
                q.X()
            if bases[i] == 1:
                q.H()

            # Alice sends to Eve
            Alice.sendQubit(q, "Eve")

        print("Alice: Sent all qubits to Eve.")

        # Basis reconciliation: Alice sends her bases to Bob
        # We need to send them as a list of bytes/integers
        Alice.sendClassical("Bob", bases)
        print("Alice: Sent bases to Bob.")

        # Receive Bob's matching indices
        # match_indices will be a list of indices where bases matched
        match_indices = list(Alice.recvClassical())
        print(f"Alice: Received {len(match_indices)} matching indices from Bob.")

        sifted_key = [bits[i] for i in match_indices]

        # QBER Estimation: Alice sends the first half of the sifted key to Bob
        # to compare and estimate error rate.
        num_reveal = len(sifted_key) // 2
        reveal_indices = match_indices[:num_reveal]
        reveal_values = sifted_key[:num_reveal]

        # Send revealed values to Bob
        Alice.sendClassical("Bob", reveal_values)
        print(f"Alice: Sent {num_reveal} revealed bits to Bob for QBER estimation.")

        # Receive QBER and decision from Bob
        data = list(Alice.recvClassical())
        qber = data[0] / 100.0
        decision = data[1] # 1 for OK, 0 for Abort

        final_key = sifted_key[num_reveal:]

        print("\n--- Alice Results ---")
        print(f"Sifted Key Size: {len(sifted_key)}")
        print(f"QBER: {qber:.2%}")
        if decision == 1:
            print(f"Final Key Agreement Status: SUCCESS")
            print(f"Final Key: {final_key}")
        else:
            print(f"Final Key Agreement Status: ABORTED (QBER > 11%)")

if __name__ == "__main__":
    main()
