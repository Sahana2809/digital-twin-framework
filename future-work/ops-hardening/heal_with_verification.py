"""
Drop-in replacement for `ml_anomaly_detector.py`'s `heal_slice()` on `main`.

`main`'s version fires `tc qdisc del` and assumes it worked. This version
re-polls Prometheus after the fix and distinguishes "healing worked" from
"healing failed" (escalation) instead of silently treating both as success.

Wire this into ml_anomaly_detector.py by replacing its heal_slice() with
heal_slice_and_verify() below and swapping its single log_alert() call on
anomaly detection for the richer flow here.
"""

import time

import requests

PROMETHEUS_URL = "http://localhost:9090"
VERIFY_DELAY_SECONDS = 5       # give tc + the network a moment to settle
VERIFY_RETRIES = 3

NORMAL_THRESHOLDS = {
    # (metric, max_acceptable_value) per slice; anything above means "still broken"
    "embb": {"packet_loss_pct": 2.0, "latency_ms": 60},
    "urllc": {"packet_loss_pct": 2.0, "latency_ms": 20},
    "mmtc": {"packet_loss_pct": 5.0, "latency_ms": 150},
}


def fetch_metric(metric_name, slice_id):
    try:
        response = requests.get(
            f"{PROMETHEUS_URL}/api/v1/query",
            params={"query": f'{metric_name}{{slice_id="{slice_id}"}}'},
            timeout=5,
        )
        results = response.json()["data"]["result"]
        return float(results[0]["value"][1]) if results else None
    except Exception:
        return None


def is_slice_healthy(slice_id):
    thresholds = NORMAL_THRESHOLDS[slice_id]
    for metric, limit in thresholds.items():
        value = fetch_metric(metric, slice_id)
        if value is None or value > limit:
            return False
    return True


def run_heal_command(slice_id):
    import subprocess
    command = f"sudo ip netns exec ue_{slice_id} tc qdisc del dev veth0 root 2>/dev/null || true"
    subprocess.run(command, shell=True, check=True)


def heal_slice_and_verify(slice_id, log_alert):
    """Returns True if the slice measurably recovered, False if it escalated."""
    run_heal_command(slice_id)

    for attempt in range(1, VERIFY_RETRIES + 1):
        time.sleep(VERIFY_DELAY_SECONDS)
        if is_slice_healthy(slice_id):
            log_alert(f"✅ SELF-HEALING VERIFIED: {slice_id.upper()} back within normal thresholds "
                       f"(attempt {attempt}/{VERIFY_RETRIES}).")
            return True
        log_alert(f"⚠️ Healing attempt {attempt}/{VERIFY_RETRIES} for {slice_id.upper()} "
                   f"did not clear the anomaly, retrying...")
        run_heal_command(slice_id)

    log_alert(f"❌ SELF-HEALING FAILED: {slice_id.upper()} still unhealthy after "
              f"{VERIFY_RETRIES} attempts — ESCALATING to human operator.")
    # Real escalation hook: page on-call, open a ticket, etc. Left as a seam
    # rather than guessing at a specific paging integration here.
    return False
