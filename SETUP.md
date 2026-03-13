# SimulaQron Distributed Setup Instructions

To run this simulation across your three virtual machines, follow these steps to configure SimulaQron with the provided `nodes.json`.

## 1. Configure SimulaQron on each VM

On each of the three VMs (Alice, Eve, Bob), you need to tell SimulaQron about the network topology.

### Option A: Using the CLI (Recommended)
Run the following commands on **all** VMs to ensure they all share the same network map:

```bash
simulaqron nodes add --name Alice --ip 192.168.56.11
simulaqron nodes add --name Eve --ip 192.168.56.12
simulaqron nodes add --name Bob --ip 192.168.56.13
```

### Option B: Using the `nodes.json` file
Alternatively, you can start SimulaQron by pointing it to the `nodes.json` file:

```bash
simulaqron start --nodes nodes.json
```

## 2. Running the Simulation

Start the processes in the following order:

1. **On the Bob VM (192.168.56.13):**
   ```bash
   python3 bob.py
   ```

2. **On the Eve VM (192.168.56.12):**
   ```bash
   python3 eve.py
   ```

3. **On the Alice VM (192.168.56.11):**
   ```bash
   python3 alice.py
   ```

## 3. Verify Output
- **Alice** and **Bob** will output their sifted key size and the calculated QBER.
- If the QBER is ≤ 11%, they will output "SUCCESS" and the final key.
- If the QBER is > 11% (likely due to Eve's 50% interception), they will output "ABORTED".
