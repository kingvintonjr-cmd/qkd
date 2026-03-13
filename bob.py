import random
import time
from cqc.pythonLib import CQCConnection, qubit

def main():
    # Initialize the connection
    try:
        with CQCConnection("Bob") as Bob:
            num_bits = 100
            bases = [random.randint(0, 1) for _ in range(num_bits)]
            results = []

            print(f"Bob: Ready to receive {num_bits} qubits.")

            # Receive qubits from Eve
            for i in range(num_bits):
                q = Bob.recvQubit()

                # Measure in Bob's chosen basis
                if bases[i] == 1:
                    q.H()

                res = q.measure()
                results.append(res)

            print("Bob: Received and measured all qubits.")

            # Basis reconciliation: Receive Alice's bases
            print("Bob: Waiting for bases from Alice...")
            msg = Bob.recvClassical()
            alice_bases = list(msg)
            print("Bob: Received bases from Alice.")

            # Find indices where bases match
            match_indices = [i for i in range(num_bits) if bases[i] == alice_bases[i]]
            print(f"Bob: Found {len(match_indices)} matching bases.")

            # Send match indices to Alice
            print("Bob: Sending matching indices to Alice...")
            Bob.sendClassical("Alice", match_indices)

            sifted_key = [results[i] for i in match_indices]

            # QBER Estimation: Receive revealed bits from Alice
            print("Bob: Waiting for revealed bits from Alice...")
            msg_reveal = Bob.recvClassical()
            alice_reveal_values = list(msg_reveal)
            num_reveal = len(alice_reveal_values)
            bob_reveal_values = sifted_key[:num_reveal]

            # Calculate errors
            errors = 0
            for a, b in zip(alice_reveal_values, bob_reveal_values):
                if a != b:
                    errors += 1

            qber = errors / num_reveal if num_reveal > 0 else 0
            decision = 1 if qber <= 0.11 else 0

            # Send QBER result and decision back to Alice
            print(f"Bob: Sending QBER ({qber:.2%}) and decision to Alice...")
            Bob.sendClassical("Alice", [int(qber * 100), decision])

            final_key = sifted_key[num_reveal:]

            print("\n--- Bob Results ---")
            print(f"Sifted Key Size: {len(sifted_key)}")
            print(f"QBER: {qber:.2%}")
            if decision == 1:
                print(f"Final Key Agreement Status: SUCCESS")
                print(f"Final Key: {final_key}")
            else:
                print(f"Final Key Agreement Status: ABORTED (QBER > 11%)")

    except Exception as e:
        print(f"Bob Error: {e}")

if __name__ == "__main__":
    main()
