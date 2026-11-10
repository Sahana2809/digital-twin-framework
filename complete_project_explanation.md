# Complete Project Explanation
## "A Digital Twin Framework for Chaos Engineering and AI-Driven Self-Healing in 5G Smart Campus Networks"

---

## 1. Project Directory Structure

```
5g-network-slicing/
├── Dockerfile.open5gs              # Builds the Open5GS container image
├── docker-compose.yml              # Orchestrates all 5G core containers + Prometheus
├── requirements.txt                # Python dependencies
├── config/
│   ├── open5gs-amf.yaml            # Access & Mobility Management Function config
│   ├── open5gs-smf.yaml            # Session Management Function config (slice routing)
│   ├── open5gs-upf1.yaml           # User Plane Function for eMBB slice
│   ├── open5gs-upf2.yaml           # User Plane Function for URLLC slice
│   ├── open5gs-upf3.yaml           # User Plane Function for mMTC slice
│   └── prometheus.yml              # Telemetry scraping configuration
├── scripts/
│   └── setup_network.sh            # Creates the Digital Twin via Linux namespaces
└── src/
    ├── traffic_generator.py        # Synthetic telemetry exporter (Prometheus metrics)
    ├── ml_anomaly_detector.py      # AI fault detection + autonomous self-healing engine
    └── dashboard.py                # Streamlit command center (visualization + chaos injection)
```

---

## 2. High-Level Architecture

The system is composed of **four layers** that interact in a closed loop:

```
┌──────────────────────────────────────────────────────────────────────┐
│                     LAYER 4: COMMAND CENTER                         │
│   dashboard.py (Streamlit)                                         │
│   - Visualizes real-time throughput, latency, packet loss           │
│   - Displays AIOps self-healing alerts                              │
│   - Provides Chaos Engineering buttons                              │
├──────────────────────────────────────────────────────────────────────┤
│                     LAYER 3: AIOps ENGINE                           │
│   ml_anomaly_detector.py                                           │
│   - Trains a Random Forest Classifier on synthetic fault profiles   │
│   - Polls Prometheus every 2 seconds for real-time slice metrics    │
│   - Detects anomalies and triggers autonomous self-healing          │
├──────────────────────────────────────────────────────────────────────┤
│                     LAYER 2: TELEMETRY PIPELINE                     │
│   traffic_generator.py → Prometheus                                │
│   - Measures real latency/loss via ping inside network namespaces   │
│   - Exports metrics in Prometheus exposition format (port 8000)     │
│   - Prometheus scrapes all endpoints every 2 seconds                │
├──────────────────────────────────────────────────────────────────────┤
│                     LAYER 1: 5G CORE + DIGITAL TWIN                 │
│   Open5GS (AMF, SMF, NRF, 3× UPF) + Linux Network Namespaces      │
│   - Three isolated slices: eMBB, URLLC, mMTC                       │
│   - Each slice has its own UPF, TUN interface, and namespace        │
│   - Policy-based routing enforces data-plane isolation              │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 3. Detailed File-by-File Explanation

---

### 3.1 `Dockerfile.open5gs`

**Purpose:** Builds a single Docker image containing all Open5GS network functions.

**How it works:**
- Starts from Ubuntu 22.04 as the base image.
- Installs networking utilities (`iptables`, `iproute2`, `iputils-ping`, `tcpdump`) that are needed for traffic inspection and namespace manipulation inside containers.
- Adds the MongoDB 6.0 GPG key and repository (required because Open5GS stores subscriber data and NF registrations in MongoDB).
- Adds the official Open5GS PPA (`ppa:open5gs/latest`) and installs the `open5gs` package, which provides all network function binaries (`open5gs-amfd`, `open5gs-smfd`, `open5gs-upfd`, `open5gs-nrfd`).
- The `CMD` defaults to `/bin/bash`, but each container in `docker-compose.yml` overrides this with the specific network function command.

**Why one image for all NFs:** In a production 5G core, each NF would be a separate microservice. Here we use one image to reduce build time and disk usage, and Docker Compose simply launches different binaries from the same image.

---

### 3.2 `docker-compose.yml`

**Purpose:** Orchestrates the entire 5G core network and monitoring stack as a set of Docker containers.

**Services deployed:**

| Service | Container Name | Role |
|---------|---------------|------|
| `mongodb` | mongodb | Stores subscriber profiles, NF registrations |
| `prometheus` | prometheus | Scrapes and stores time-series telemetry |
| `nrf` | open5gs-nrf | Network Repository Function — service discovery for all NFs |
| `amf` | open5gs-amf | Access & Mobility Management — handles UE registration, authentication |
| `smf` | open5gs-smf | Session Management — creates PDU sessions, selects UPF per slice |
| `upf1-embb` | open5gs-upf1-embb | User Plane for eMBB (Campus Labs) — high throughput |
| `upf2-urllc` | open5gs-upf2-urllc | User Plane for URLLC (Robotics) — low latency |
| `upf3-mmtc` | open5gs-upf3-mmtc | User Plane for mMTC (Smart Hostel IoT) — high device density |

**Key design decisions:**
- **`network_mode: host`** — All containers share the host's network stack. This is critical because the UPFs need to create TUN interfaces (`ogstun1`, `ogstun2`, `ogstun3`) directly on the host kernel, and the namespaces we create later need to route traffic through those TUN interfaces. If we used Docker bridge networking, the TUN interfaces would be trapped inside the container's isolated network and unreachable from the host namespaces.
- **`privileged: true`** on UPFs — The UPF containers need elevated privileges to create TUN/TAP devices and manipulate kernel routing tables.
- **`depends_on`** chains — Ensures MongoDB starts before NRF, NRF before AMF, AMF before SMF, and SMF before UPFs. This mirrors the real 5G boot sequence: NFs must register with NRF before they can discover each other.
- **Volume mounts** — Each container's configuration file is mounted from the `config/` directory into the standard Open5GS config path (`/etc/open5gs/`).

---

### 3.3 `config/open5gs-amf.yaml`

**Purpose:** Configures the Access and Mobility Management Function.

**Key sections explained:**

- **`sbi` (Service-Based Interface):** The AMF listens on `127.0.0.5:7777` for HTTP/2 communication with other NFs (NRF, SMF). This is how 5G NFs discover and talk to each other (unlike 4G which used diameter/GTP-C).
- **`ngap`:** The AMF listens on `127.0.0.5` for NGAP (Next Generation Application Protocol) connections from gNodeBs. In our simulation, we don't have a real gNodeB, but this is required for the AMF to start.
- **`metrics`:** Exposes Prometheus-compatible metrics on `127.0.0.5:9090`.
- **`guami` (Globally Unique AMF ID):** Identifies this AMF instance. Uses test PLMN `999/70` (reserved for testing by 3GPP).
- **`tai` (Tracking Area Identity):** Defines the geographic area this AMF serves. TAC 1 covers our entire campus.
- **`plmn_support` → `s_nssai`:** **This is the critical slicing configuration.** It declares that this AMF supports three network slices:
  - SST 1, SD 000001 → eMBB (enhanced Mobile Broadband)
  - SST 2, SD 000002 → URLLC (Ultra-Reliable Low-Latency Communication)
  - SST 3, SD 000003 → mMTC (massive Machine-Type Communication)
- **`security`:** Configures the integrity and ciphering algorithms. NIA2/NEA2 are the strongest (AES-based).

---

### 3.4 `config/open5gs-smf.yaml`

**Purpose:** Configures the Session Management Function — the brain that decides *which UPF handles which slice*.

**Key sections explained:**

- **`pfcp.client.upf`:** Lists the three UPF addresses:
  - `127.0.0.11` → UPF1 (eMBB)
  - `127.0.0.12` → UPF2 (URLLC)
  - `127.0.0.13` → UPF3 (mMTC)
  
  The SMF communicates with UPFs via PFCP (Packet Forwarding Control Protocol) to install forwarding rules.

- **`subnet`:** **This is the slice-to-UPF routing table.** Each entry maps an S-NSSAI to a specific IP subnet and DNN (Data Network Name):
  - SST 1 / SD 000001 → `10.45.1.1/16` (eMBB users get IPs from this range)
  - SST 2 / SD 000002 → `10.45.2.1/16` (URLLC users)
  - SST 3 / SD 000003 → `10.45.3.1/16` (mMTC devices)
  
  When a UE requests a PDU session with a specific S-NSSAI, the SMF looks up this table, selects the matching UPF, and establishes a GTP tunnel to it. This is how **data-plane isolation** is enforced — traffic from different slices never crosses paths.

---

### 3.5 `config/open5gs-upf1.yaml`, `upf2.yaml`, `upf3.yaml`

**Purpose:** Configure the three User Plane Functions — one dedicated to each slice.

**How they differ:**

| Config | PFCP Address | GTP-U Address | Subnet | TUN Device | Metrics Port |
|--------|-------------|--------------|--------|-----------|-------------|
| UPF1 (eMBB) | 127.0.0.11 | 127.0.0.11 | 10.1.1.0/24 | ogstun1 | 9091 |
| UPF2 (URLLC) | 127.0.0.12 | 127.0.0.12 | 10.2.1.0/24 | ogstun2 | 9092 |
| UPF3 (mMTC) | 127.0.0.13 | 127.0.0.13 | 10.3.1.0/24 | ogstun3 | 9093 |

- **`pfcp.server`:** The UPF listens here for forwarding rules from the SMF.
- **`gtpu.server`:** The UPF listens here for GTP-U (user-plane) tunneled packets from the gNodeB.
- **`session.subnet`:** The IP pool assigned to UEs connecting through this UPF.
- **`dev`:** The TUN interface name (`ogstun1`, `ogstun2`, `ogstun3`). When the UPF starts, it creates this TUN device on the host. All decapsulated user traffic exits through this interface.
- **`smf.pfcp.client`:** Points back to the SMF at `127.0.0.4` so the UPF can register itself.

**Why separate UPFs matter:** In most student projects, a single UPF handles all traffic. By deploying three UPFs, we achieve true **data-plane isolation**. Even if the eMBB slice is completely saturated, the URLLC slice's traffic flows through a completely different kernel interface (`ogstun2`), guaranteeing its low-latency performance.

---

### 3.6 `config/prometheus.yml`

**Purpose:** Configures Prometheus to scrape telemetry from all network functions and our traffic generator.

**Scrape targets:**

| Job Name | Target | What it Scrapes |
|----------|--------|----------------|
| open5gs-amf | 127.0.0.5:9090 | AMF metrics (registrations, connection counts) |
| open5gs-smf | 127.0.0.4:9090 | SMF metrics (session creations, slice routing) |
| open5gs-upf-embb | 127.0.0.11:9091 | UPF1 metrics (bytes forwarded, packets processed) |
| open5gs-upf-urllc | 127.0.0.12:9092 | UPF2 metrics |
| open5gs-upf-mmtc | 127.0.0.13:9093 | UPF3 metrics |
| synthetic-traffic | 127.0.0.1:8000 | Our custom traffic generator's per-slice KPIs |

**`scrape_interval: 2s`** — Every 2 seconds, Prometheus pulls fresh data from all targets. This fast interval is critical for real-time anomaly detection.

---

### 3.7 `scripts/setup_network.sh`

**Purpose:** Creates the **Digital Twin** — a virtual replica of the campus network topology using Linux network namespaces.

**Step-by-step logic:**

1. **Enable IP forwarding** (`sysctl -w net.ipv4.ip_forward=1`) — Allows the host kernel to route packets between different interfaces. Without this, traffic from namespaces would be dropped.

2. **For each slice (embb, urllc, mmtc):**
   
   a. **Cleanup** — Deletes any existing namespace, veth interface, or routing rule from a previous run. This makes the script idempotent (safe to run multiple times).
   
   b. **Create namespace** (`ip netns add ue_embb`) — A network namespace is a complete, isolated copy of the Linux networking stack. Processes inside it have their own interfaces, routing tables, and firewall rules. This simulates a physical UE device.
   
   c. **Create veth pair** (`ip link add veth_embb type veth peer name veth0 netns ue_embb`) — A veth (virtual ethernet) pair is like a virtual cable with two ends. One end (`veth_embb`) lives on the host; the other (`veth0`) lives inside the namespace. Any packet sent into one end comes out the other.
   
   d. **Assign IP addresses:**
   - Host side: `10.1.1.1/24` (for eMBB), `10.2.1.1/24` (URLLC), `10.3.1.1/24` (mMTC)
   - Namespace side: `10.1.1.2/24`, `10.2.1.2/24`, `10.3.1.2/24`
   
   e. **Set default route inside namespace** — All traffic from the namespace goes to the host-side veth IP (e.g., `10.1.1.1`).
   
   f. **Policy-based routing on the host** — This is the critical piece. A normal routing table would send all traffic out the same interface. Instead, we create a **dedicated routing table** for each slice:
   - Traffic from `10.1.1.0/24` → lookup table `101` → exit via `ogstun1`
   - Traffic from `10.2.1.0/24` → lookup table `102` → exit via `ogstun2`
   - Traffic from `10.3.1.0/24` → lookup table `103` → exit via `ogstun3`
   
   This forces each namespace's traffic through its designated UPF TUN interface.
   
   g. **NAT/Masquerade** — Rewrites the source IP of outgoing packets so replies can find their way back. Without this, responses from the internet would not know how to route back to our private `10.x.x.x` addresses.

**The result:** Three completely isolated virtual networks, each mapped to a specific 5G slice's User Plane Function. This is the "Digital Twin" of the campus.

---

### 3.8 `src/traffic_generator.py`

**Purpose:** Generates realistic per-slice network telemetry and exports it as Prometheus metrics on port 8000.

**How it works:**

1. **Defines four Prometheus Gauge metrics:** `throughput_mbps`, `latency_ms`, `packet_loss_pct`, `active_ues` — each labeled by `slice_id`.

2. **Defines baseline profiles** for each slice that reflect real-world 5G characteristics:
   - eMBB: 100–500 Mbps throughput, 10–30ms latency, 0–0.1% loss, 50–100 UEs
   - URLLC: 10–50 Mbps throughput, 1–5ms latency, 0–0.01% loss, 5–20 UEs
   - mMTC: 1–10 Mbps throughput, 20–100ms latency, 0.1–1.0% loss, 500–1000 UEs

3. **Spawns a thread per slice** that runs `measure_real_metrics()` every 2 seconds.

4. **Hybrid measurement approach:**
   - **Latency and packet loss** are measured **for real** by executing `ping -c 3 8.8.8.8` inside the namespace (`ip netns exec ue_embb ping ...`). This means:
     - Under normal conditions, you get real network latency.
     - When chaos is injected via `tc` (e.g., 120ms delay on `veth0`), the ping actually measures the injected delay. This makes the telemetry reflect the chaos injection truthfully.
   - **Throughput and UE count** are synthetic (randomly generated within the baseline range) because measuring real throughput would require running `iperf` sessions.
   - **Fallback:** If the namespace isn't configured yet (ping returns 100% loss), it falls back to synthetic data so Prometheus always has valid values.

5. **Loss-throughput coupling:** If measured packet loss exceeds 5%, throughput is throttled to 10% of normal. This simulates the real-world effect where high packet loss degrades TCP throughput.

**Why this design matters:** Most student projects just generate random numbers. By actually pinging from inside the namespace, our telemetry genuinely reflects chaos injection. When the dashboard injects 120ms latency, the traffic generator measures ~120ms latency, Prometheus stores it, the ML model sees it, and triggers self-healing. The entire pipeline is truthful.

---

### 3.9 `src/ml_anomaly_detector.py`

**Purpose:** The AIOps engine that detects network anomalies in real-time and autonomously heals the network.

**Phase 1: Training (lines 31–63)**

The model is trained on synthetic data because we don't have months of historical campus telemetry. The function `generate_training_data()` creates 2100 labeled samples:

| Class | Label | Count | Characteristics |
|-------|-------|-------|----------------|
| Normal Operation | 0 | 1500 (500×3 slices) | Each slice at its healthy baseline |
| eMBB Congestion | 1 | 200 | Low throughput (5–50), high latency (100–300ms), high loss (5–15%) |
| URLLC Latency Spike | 2 | 200 | Latency 50–150ms (far above URLLC's normal 1–5ms) |
| mMTC Packet Dropout | 3 | 200 | Near-zero throughput, very high loss (10–30%) |

Each sample has 5 features:
- `throughput_mbps` — Current data rate
- `latency_ms` — Round-trip delay
- `packet_loss_pct` — Percentage of dropped packets
- `slice_id_encoded` — Numeric ID (0=eMBB, 1=URLLC, 2=mMTC)
- `active_ues` — Number of connected devices

A **Random Forest Classifier** with 100 decision trees is trained on this data. Random Forest works by building 100 independent decision trees, each trained on a random subset of the data, and taking a majority vote for the final prediction. It is robust against overfitting and handles non-linear decision boundaries well.

**Phase 2: Live Inference Loop (lines 95–123)**

Every 2 seconds, the script:
1. Queries the Prometheus HTTP API for the latest values of all four metrics.
2. For each slice, constructs a feature vector (DataFrame) matching the training format.
3. Runs `model.predict(features)` — this takes microseconds.
4. If the prediction is NOT 0 (Normal), it logs an alert AND triggers self-healing.

**Phase 3: Self-Healing (lines 80–87)**

The `heal_slice()` function is the key innovation that separates this project from a basic anomaly detector:
- It executes: `sudo ip netns exec ue_{slice_id} tc qdisc del dev veth0 root`
- This command enters the affected namespace and **removes all traffic control rules** from its virtual interface.
- This directly reverses whatever chaos was injected (whether it was latency, packet loss, or bandwidth throttling).
- The function logs whether the healing succeeded or failed.

**Cooldown mechanism (line 119):** A 10-second cooldown prevents the healer from firing repeatedly for the same slice. Without this, it would trigger every 2 seconds while Prometheus still shows stale anomalous data.

---

### 3.10 `src/dashboard.py`

**Purpose:** A Streamlit web application serving as the Network Operations Command Center.

**Layout:**
- **Left sidebar:** Chaos Engineering control panel
- **Main area (75% width):** Real-time telemetry charts
- **Right column (25% width):** AIOps self-healing alert log

**Sidebar — Chaos Engineering Buttons:**

Each button executes a Linux `tc` (Traffic Control) command inside a specific namespace using `subprocess.run()`:

| Button | Command | Effect |
|--------|---------|--------|
| Inject URLLC Latency | `tc qdisc add dev veth0 root netem delay 120ms` | Adds 120ms artificial delay to every packet in the URLLC namespace |
| Inject mMTC Packet Loss | `tc qdisc add dev veth0 root netem loss 20%` | Randomly drops 20% of packets in the mMTC namespace |
| Inject eMBB Congestion | `tc qdisc add dev veth0 root tbf rate 1mbit burst 32kbit latency 400ms` | Throttles eMBB bandwidth to 1 Mbps (vs normal 100–500 Mbps) |
| Heal Network | `tc qdisc del dev veth0 root` (on all 3) | Clears all injected faults, manual override |

**Main Area — Telemetry:**

The `update_dashboard()` function:
1. Fetches the latest metrics from Prometheus via HTTP API.
2. Appends them to `st.session_state.history` (a DataFrame stored in Streamlit's session state, keeping the last 150 data points).
3. Renders three columns of `st.metric()` widgets showing the latest throughput, latency, and packet loss for each slice.
4. Renders two Plotly time-series line charts (Throughput and Latency) colored by slice name.

**Right Column — AIOps Log:**

Reads the `alerts.log` file written by `ml_anomaly_detector.py` and displays the last 15 entries as `st.error()` blocks. This creates a live scrolling feed of anomaly detections and self-healing events.

**Auto-refresh:** The script calls `update_dashboard()`, sleeps 2 seconds, then calls `st.rerun()` which re-executes the entire script from top to bottom. This creates a 2-second refresh cycle.

---

## 4. Complete Data Flow (End-to-End)

Here is the exact chain of events when you click "Inject URLLC Latency" on the dashboard:

```
1. Dashboard button click
   └→ subprocess executes: tc qdisc add dev veth0 root netem delay 120ms
      (inside namespace ue_urllc)

2. Traffic Generator (runs every 2s)
   └→ Executes: ip netns exec ue_urllc ping -c 3 8.8.8.8
   └→ Ping packets now traverse veth0 which has 120ms added delay
   └→ Measured latency: ~130ms (120ms injected + ~10ms real)
   └→ Updates Prometheus gauge: latency_ms{slice_id="urllc"} = 130

3. Prometheus scrapes traffic generator (every 2s)
   └→ Stores: latency_ms{slice_id="urllc"} = 130 at timestamp T

4. ML Anomaly Detector polls Prometheus (every 2s)
   └→ Fetches: throughput=25, latency=130, loss=0.5, slice=1, ues=12
   └→ Random Forest predicts: Class 2 (URLLC Latency Spike)
   └→ Logs: "🚨 ANOMALY on URLLC: URLLC Latency Spike detected!"
   └→ Calls heal_slice("urllc")

5. Self-Healing
   └→ Executes: tc qdisc del dev veth0 root (inside ue_urllc)
   └→ Removes the 120ms delay rule
   └→ Logs: "✅ SELF-HEALING SUCCESS: Cleared congestion rules for URLLC slice."

6. Next Traffic Generator cycle (2s later)
   └→ Ping now measures ~3ms (normal URLLC latency)
   └→ Prometheus stores normal value
   └→ ML model predicts: Class 0 (Normal Operation)
   └→ No alert fired

7. Dashboard auto-refreshes
   └→ Latency chart shows spike and immediate recovery
   └→ AIOps log shows the detection → healing → success sequence
```

---

## 5. Key Research Concepts Covered

| Concept | How It's Implemented |
|---------|---------------------|
| **5G Network Slicing** | Three S-NSSAIs (eMBB/URLLC/mMTC) routed to dedicated UPFs via SMF config |
| **Digital Twin** | Linux network namespaces create a virtual replica of campus zones |
| **Chaos Engineering** | Linux `tc` (netem/tbf) injects real faults into the virtual network |
| **Streaming Telemetry** | Prometheus scrapes real-time metrics every 2 seconds |
| **AI/ML Fault Detection** | Random Forest Classifier trained on 2100 synthetic fault profiles |
| **Autonomous Self-Healing** | Closed-loop automation: detect anomaly → execute remediation → verify recovery |
| **AIOps** | ML-driven operations replacing human network engineers |
| **Open5GS** | Production-grade open-source 5G Standalone core (3GPP Release 17) |

---

## 6. How to Present the Demo

### Step 1: Show the Architecture Diagram
Draw or present the 4-layer architecture from Section 2 above.

### Step 2: Show Normal Operation
Open the dashboard. Show all three slices operating within healthy parameters. Point out the real-time charts updating every 2 seconds.

### Step 3: Inject Chaos
Click "Inject URLLC Latency (120ms)." Explain: *"We are simulating a fiber cut or radio interference affecting the robotics lab slice."*

### Step 4: Watch the AI Detect the Fault
Point to the AIOps log. Within 4–6 seconds, you will see:
```
🚨 ANOMALY on URLLC: URLLC Latency Spike detected! TPUT=25.3, LAT=132.4, LOSS=0.5%
⚙️ TRIGGERING AI SELF-HEALING for URLLC...
✅ SELF-HEALING SUCCESS: Cleared congestion rules for URLLC slice.
```

### Step 5: Watch the Network Heal Itself
Point to the latency chart. The URLLC line will spike and then immediately drop back to baseline. No human intervention was needed.

### Step 6: Emphasize the Closed Loop
*"This is not just monitoring. This is a fully autonomous self-healing network. The AI detected the fault, diagnosed which slice was affected, identified the specific failure type, and executed the remediation — all within 6 seconds, without any human engineer."*
