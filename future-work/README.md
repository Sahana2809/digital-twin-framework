# Future Work: Real-World Hardening Roadmap

This branch (`future-work/real-world-roadmap`) is **intentionally never merged into `main`**. It exists to explore how the 5G Smart Campus Digital Twin would need to change to survive contact with a real deployment — real orchestration, real edge hardware, real predictive AI, and real operational discipline — without disturbing the clean, working lab demo on `main`.

Each idea below has:
- **The problem** with the current (`main`) implementation
- **The real-world fix**
- **What's actually in this branch** — working code where it's buildable without special hardware/infra, or a detailed design writeup where it isn't

Nothing here is meant to be "finished" — it's a scoped prototype/proposal for each direction.

---

## 1. Platform & Orchestration

### 1.1 Cloud-Native Orchestration (Kubernetes)
**Problem:** `docker-compose` boots a fixed set of containers on one host. Real operators (AT&T, Jio, etc.) run 5G Cloud-Native Network Functions (CNFs) on Kubernetes for high availability, self-healing restarts, and elastic scaling — none of which `docker-compose` gives you.

**Fix:** Migrate Open5GS (NRF, AMF, SMF, 3× UPF) + MongoDB + Prometheus to a lightweight cluster (K3s/Minikube), and replace "the AIOps engine deletes a `tc` rule" with "the AIOps engine scales a Kubernetes Deployment" for load-driven problems (as opposed to fault-driven ones, which still use `tc`).

**In this branch:** [`k8s/`](k8s/) — Kubernetes manifests for the full core (Deployments + Services, one per NF), and [`k8s/aiops_scaler.py`](k8s/aiops_scaler.py), a working prototype that uses the Kubernetes Python client to watch Prometheus load metrics and scale the eMBB UPF Deployment's replica count up/down — a real operator pattern, not a bash script wrapping `kubectl`.

### 1.2 Multi-Host Realism
**Problem:** Everything assumes one Linux host with root — namespaces, veths, and UPFs all live on the same kernel. That's a single point of failure and nothing like how a RAN/Core split actually looks.

**Fix:** Split the deployment across multiple hosts/VMs (e.g., one "gNB edge" host running the UEs/namespaces, one "core" host running AMF/SMF/UPF), connected over real IP/GRE tunnels instead of local veths.

**In this branch:** [`NOTES_multi_host.md`](NOTES_multi_host.md) — design-only, since this needs real multi-VM infrastructure to validate.

---

## 2. Intelligence Layer

### 2.1 Predictive AI Engine (PyTorch LSTM)
**Problem:** The Random Forest classifier is reactive — it only fires after a threshold has already been breached, by which point the packet loss/latency spike already happened.

**Fix:** Replace point-in-time classification with sequence forecasting. An LSTM trained on a sliding window of Prometheus time-series can predict a congestion event a few seconds *before* it happens, letting the system preemptively widen bandwidth limits instead of reactively clearing them after the fact.

**In this branch:** [`predictive-ai/lstm_forecaster.py`](predictive-ai/lstm_forecaster.py) — a working PyTorch LSTM that trains on synthetic sliding-window sequences (same slice signatures as `main`'s classifier, but as time-ordered sequences rather than single points) and exposes a `predict_next()` used to trigger *preemptive* healing.

### 2.2 Train on Real Telemetry, Not Synthetic Ranges
**Problem:** `main`'s training data is `random.uniform()` calls tuned to be perfectly separable — the model never has to work hard, and it's never validated against what `tc`-induced faults *actually* look like on the wire.

**Fix:** Log real Prometheus telemetry while deliberately running the chaos-injection buttons, label those windows by the fault that was actually injected, and train on that recorded dataset instead of hand-rolled ranges.

**In this branch:** [`predictive-ai/README.md`](predictive-ai/README.md) explains the data-collection protocol; [`ops-hardening/model_registry.py`](ops-hardening/model_registry.py) (below) is what you'd retrain/version against once that dataset exists.

### 2.3 Model Persistence & Versioning
**Problem:** The model is trained from scratch, in memory, every time the detector process starts — there's no saved artifact, no version history, no way to know which model made a given decision.

**Fix:** Persist trained models to disk with `joblib`, tag each with a version/timestamp, and load the latest at startup instead of retraining blind every boot.

**In this branch:** [`ops-hardening/model_registry.py`](ops-hardening/model_registry.py) — working save/load/versioning helper.

---

## 3. Edge Integration

### 3.1 Physical Edge-to-Cloud Integration (IoT)
**Problem:** The mMTC slice's "IoT traffic" is synthetic ping traffic inside a namespace — there's no actual physical device at the edge, so the "closed loop" never touches real hardware.

**Fix:** Bridge an ESP32 (reading real sensor data — accelerometer/temperature) over MQTT into the `ue_mmtc` namespace's traffic path, so a real packet-loss event on that slice is something a physical device actually experiences and reports.

**In this branch:** [`edge-integration/esp32_mmtc_node.ino`](edge-integration/esp32_mmtc_node.ino) — the ESP32 sketch (publishes sensor readings + a heartbeat over MQTT), and [`edge-integration/mqtt_bridge.py`](edge-integration/mqtt_bridge.py) — a working MQTT subscriber that forwards ESP32 messages into the `ue_mmtc` namespace and exposes a `heartbeat_gap_seconds` Prometheus metric the anomaly detector can key off. **I don't have the physical ESP32/sensors to test this end-to-end** — the code is written and self-consistent, but [`edge-integration/README.md`](edge-integration/README.md) documents the wiring/setup needed to actually validate it on hardware.

---

## 4. Operational Hardening

### 4.1 Verify-and-Escalate Healing (Closed-Loop Feedback)
**Problem:** `heal_slice()` in `main` fires `tc qdisc del` and assumes it worked — there's no check that the anomaly actually cleared.

**Fix:** Re-measure after healing; if the anomaly persists, escalate (log a distinct "healing failed" alert) instead of silently moving on.

**In this branch:** [`ops-hardening/heal_with_verification.py`](ops-hardening/heal_with_verification.py) — a drop-in replacement for `ml_anomaly_detector.py`'s healing function that re-polls Prometheus after the fix and escalates on failure.

### 4.2 Persistent Alert/Event Storage
**Problem:** Alerts live in a flat `alerts.log` file and Streamlit's in-memory session state — both vanish on restart. Meanwhile the `mongodb` container in `docker-compose.yml` is already running and completely unused.

**Fix:** Write anomaly/healing events to MongoDB so history survives restarts and can be queried/reported on.

**In this branch:** [`ops-hardening/mongo_alert_store.py`](ops-hardening/mongo_alert_store.py) — working `pymongo`-based writer/reader for the alert collection.

### 4.3 Securing Control Actions
**Problem:** Both the dashboard and the detector shell out with `subprocess.run(..., shell=True)` to arbitrary `sudo tc`/`iptables` strings built from Python. A web app with unrestricted `sudo` shell access to the host is not something you'd expose in a real deployment.

**Fix:** Replace ad-hoc `shell=True` + `sudo` with a narrow, allow-listed helper script that only accepts a closed set of (namespace, action) pairs, invoked via `subprocess.run([...])` (no shell), authorized through a `sudoers` rule scoped to that exact script.

**In this branch:** [`ops-hardening/secure_tc_helper.sh`](ops-hardening/secure_tc_helper.sh) + [`ops-hardening/99-aiops-tc-sudoers`](ops-hardening/99-aiops-tc-sudoers) — the constrained helper and the matching sudoers entry, plus a short note on how `dashboard.py`/`ml_anomaly_detector.py` would call it instead of raw shell strings.

---

## Status summary

| Idea | Status |
|---|---|
| Kubernetes migration + AIOps scaler | Working prototype |
| Multi-host realism | Design doc only |
| LSTM predictive engine | Working prototype (synthetic data) |
| Real-telemetry training | Protocol documented |
| Model versioning | Working helper |
| ESP32/MQTT edge bridge | Code written, **untested on hardware** |
| Verify-and-escalate healing | Working prototype |
| Mongo alert persistence | Working prototype |
| Secured control actions | Working helper + sudoers config |
