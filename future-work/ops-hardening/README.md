# Operational Hardening

Three independent hardening steps for `main`'s detector/dashboard, each
runnable/testable on its own:

- [`heal_with_verification.py`](heal_with_verification.py) — re-checks
  Prometheus after healing and escalates instead of assuming success.
- [`mongo_alert_store.py`](mongo_alert_store.py) — persists alerts/events to
  the already-deployed-but-unused `mongodb` container instead of a flat log
  file and in-memory Streamlit state.
- [`model_registry.py`](model_registry.py) — saves/versions/loads the trained
  classifier with `joblib` instead of retraining blind on every boot.
- [`secure_tc_helper.sh`](secure_tc_helper.sh) +
  [`99-aiops-tc-sudoers`](99-aiops-tc-sudoers) — a closed set of
  (slice, action) commands a constrained sudoers rule can authorize, instead
  of `subprocess.run(f"sudo ...", shell=True)` built from arbitrary strings.

## How `dashboard.py` / `ml_anomaly_detector.py` would call the secure helper

Replace, e.g., this on `main` (`dashboard.py`):

```python
cmd = "sudo ip netns exec ue_urllc tc qdisc add dev veth0 root netem delay 120ms"
subprocess.run(cmd, shell=True, check=True)
```

with:

```python
subprocess.run(
    ["sudo", "/usr/local/sbin/secure_tc_helper.sh", "urllc", "inject-latency"],
    check=True,
)
```

No `shell=True`, no string built from slice names at runtime, and sudo only
ever authorizes this one script with this one argument pair — not an open
`sudo tc`/`sudo iptables`.
