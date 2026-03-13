import random
import time
from cqc.pythonLib import CQCConnection, qubit

def main():
    # Initialize the connection
    try:
        with CQCConnection("eve") as Eve:
            num_bits = 100

            print(f"Eve: Ready to intercept {num_bits} qubits.")

            intercept_count = 0
            for i in range(num_bits):
                # Intercept qubit from Alice
                q = Eve.recvQubit()

                # 50% chance to eavesdrop
                if random.random() < 0.5:
                    intercept_count += 1
                    # Choose random basis
                    basis = random.randint(0, 1)
                    if basis == 1:
                        q.H()

                    # Measure qubit
                    res = q.measure()

                    # Re-prepare qubit to resend to Bob
                    q_resend = qubit(Eve)
                    if res == 1:
                        q_resend.X()
                    if basis == 1:
                        q_resend.H()

                    # Send to bob
                    Eve.sendQubit(q_resend, "bob")
                else:
                    # Just forward the qubit without measurement
                    Eve.sendQubit(q, "bob")

            print(f"Eve: Intercepted and measured {intercept_count} qubits.")
            print("Eve: Forwarded all qubits to Bob.")

    except Exception as e:
        print(f"Eve Error: {e}")

if __name__ == "__main__":
    main()
