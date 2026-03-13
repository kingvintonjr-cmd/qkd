# SimulaQron Distributed Setup Instructions

To run this simulation across your three virtual machines, follow these steps to configure SimulaQron with the provided `nodes.json`.

## 0. File Distribution

Copy all project files (`alice.py`, `bob.py`, `eve.py`, `nodes.json`) to the same directory on **all three virtual machines**. This ensures that each node has access to the network configuration and its respective protocol script.

## 1. Configure SimulaQron on each VM

On each of the three VMs (Alice, Eve, Bob), you need to tell SimulaQron about the network topology.

### Option A: Using the CLI (Recommended)
Run the following commands on **all** VMs to ensure they all share the same network map:

```bash
simulaqron nodes add alice --hostname 192.168.56.11
simulaqron nodes add eve --hostname 192.168.56.12
simulaqron nodes add bob --hostname 192.168.56.13
```

### Option B: Using the `nodes.json` file
Alternatively, you can start SimulaQron by pointing it to the `nodes.json` file:

```bash
simulaqron start --nodes nodes.json
```

## 2. Running the Simulation

Start the processes in the following order. **Note:** Bob and Eve must be running and ready to receive before Alice starts sending.

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

## 4. Troubleshooting "Code Not Running"

If you encounter errors or the scripts hang:

1. **Check SimulaQron Backend**: Ensure the SimulaQron backend is running on all VMs. You can start it with `simulaqron start`.
2. Connectivity: Verify that VMs can ping each other. alice must be able to reach eve, and eve must be able to reach bob.
3. **Reset Backend**: If a previous run crashed, try `simulaqron stop` then `simulaqron start` on all nodes to clear the state.
4. **Firewall**: Ensure ports `8801` (CQC) and `8802` (Virtual Node) are open on your private network.

## 3. Verify Output
- **Alice** and **Bob** will output their sifted key size and the calculated QBER.
- If the QBER is ≤ 11%, they will output "SUCCESS" and the final key.
- If the QBER is > 11% (likely due to Eve's 50% interception), they will output "ABORTED".
