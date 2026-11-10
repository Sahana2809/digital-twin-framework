#!/bin/bash
# secure_tc_helper.sh
#
# Replaces `main`'s pattern of building raw `sudo ... | shell=True` strings
# in Python (dashboard.py, ml_anomaly_detector.py) with a single allow-listed
# entry point. Only the exact (slice, action) pairs below are accepted —
# arbitrary tc/iptables commands cannot be smuggled through this script.
#
# Install: copy to /usr/local/sbin/secure_tc_helper.sh, chmod 750, chown
# root:aiops. Pair with the sudoers rule in 99-aiops-tc-sudoers so the
# dashboard/detector's service account can run *only* this script as root,
# not an arbitrary shell command.

set -euo pipefail

SLICE="${1:-}"
ACTION="${2:-}"

VALID_SLICES=("embb" "urllc" "mmtc")
is_valid_slice() {
    for s in "${VALID_SLICES[@]}"; do
        [[ "$1" == "$s" ]] && return 0
    done
    return 1
}

if ! is_valid_slice "$SLICE"; then
    echo "Rejected: unknown slice '$SLICE'" >&2
    exit 1
fi

NS="ue_${SLICE}"

case "$ACTION" in
    inject-latency)
        CMD="tc qdisc add dev veth0 root netem delay 120ms"
        ;;
    inject-loss)
        CMD="tc qdisc add dev veth0 root netem loss 20%"
        ;;
    inject-congestion)
        CMD="tc qdisc add dev veth0 root tbf rate 1mbit burst 32kbit latency 400ms"
        ;;
    heal)
        CMD="tc qdisc del dev veth0 root 2>/dev/null || true"
        ;;
    *)
        echo "Rejected: unknown action '$ACTION'" >&2
        exit 1
        ;;
esac

ip netns exec "$NS" bash -c "$CMD"
