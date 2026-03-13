import random
import time
from cqc.pythonLib import CQCConnection, qubit

def main():
    # Initialize the connection
    # We use a try-except block to help diagnose connection issues
    try:
        with CQCConnection("Alice") as Alice:
            num_bits = 100
            bits = [random.randint(0, 1) for _ in range(num_bits)]
            bases = [random.randint(0, 1) for _ in range(num_bits)]

            print(f"Alice: Generated {num_bits} bits and bases.")
            print("Alice: Waiting 5 seconds for Bob and Eve to be ready...")
            time.sleep(5)

            # Send qubits to Eve
            for i in range(num_bits):
                q = qubit(Alice)
                if bits[i] == 1:
                    q.X()
                if bases[i] == 1:
                    q.H()

                # Alice sends to Eve
                Alice.sendQubit(q, "Eve")
                # Small delay to avoid overwhelming the backend
                time.sleep(0.01)

            print("Alice: Sent all qubits to Eve.")

            # Wait a bit to ensure Bob has finished receiving and is ready for classical communication
            print("Alice: Waiting for Bob to finish measurements...")
            time.sleep(5)

            # Basis reconciliation: Alice sends her bases to Bob
            print("Alice: Sending bases to Bob...")
            Alice.sendClassical("Bob", bases)

            # Receive Bob's matching indices
            print("Alice: Waiting for matching indices from Bob...")
            msg = Alice.recvClassical()
            match_indices = list(msg)
            print(f"Alice: Received {len(match_indices)} matching indices from Bob.")

            sifted_key = [bits[i] for i in match_indices]

            # QBER Estimation: Alice sends the first half of the sifted key to Bob
            num_reveal = len(sifted_key) // 2
            reveal_values = sifted_key[:num_reveal]

            print(f"Alice: Sending {num_reveal} revealed bits to Bob...")
            Alice.sendClassical("Bob", reveal_values)

            # Receive QBER and decision from Bob
            print("Alice: Waiting for QBER and decision from Bob...")
            res_msg = Alice.recvClassical()
            data = list(res_msg)
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

    except Exception as e:
        print(f"Alice Error: {e}")

if __name__ == "__main__":
    main()
