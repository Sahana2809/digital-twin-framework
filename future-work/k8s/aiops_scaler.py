"""
AIOps load-based scaler for the eMBB UPF Deployment.

This is the Kubernetes-native counterpart to `ml_anomaly_detector.py`'s
fault healing on `main`: where a `tc qdisc del` fixes an *injected fault*,
this script fixes *organic load growth* by scaling the eMBB UPF Deployment
up or down, the way a real operator's CNF orchestration would.

Run alongside the existing `traffic_generator.py` exporter. Requires the
`kubernetes` Python package and a valid kubeconfig (in-cluster config is
used automatically when run as a Pod with the `aiops-scaler` ServiceAccount
referenced in prometheus.yaml).
"""

import time

import requests
from kubernetes import client, config

PROMETHEUS_URL = "http://prometheus.digital-twin.svc:9090"
NAMESPACE = "digital-twin"
DEPLOYMENT = "open5gs-upf-embb"

SCALE_UP_THROUGHPUT_MBPS = 400   # sustained load near the slice's ceiling
SCALE_DOWN_THROUGHPUT_MBPS = 100  # comfortably idle
MIN_REPLICAS = 1
MAX_REPLICAS = 5
COOLDOWN_SECONDS = 60


def load_kube_config():
    try:
        config.load_incluster_config()
    except config.ConfigException:
        config.load_kube_config()


def fetch_embb_throughput():
    resp = requests.get(
        f"{PROMETHEUS_URL}/api/v1/query",
        params={"query": 'throughput_mbps{slice_id="embb"}'},
        timeout=5,
    )
    results = resp.json()["data"]["result"]
    if not results:
        return None
    return float(results[0]["value"][1])


def current_replicas(apps_api):
    dep = apps_api.read_namespaced_deployment(DEPLOYMENT, NAMESPACE)
    return dep.spec.replicas


def scale_to(apps_api, replicas):
    apps_api.patch_namespaced_deployment_scale(
        DEPLOYMENT,
        NAMESPACE,
        {"spec": {"replicas": replicas}},
    )
    print(f"Scaled {DEPLOYMENT} to {replicas} replica(s)")


def main():
    load_kube_config()
    apps_api = client.AppsV1Api()
    last_scale_time = 0.0

    while True:
        time.sleep(5)

        throughput = fetch_embb_throughput()
        if throughput is None:
            continue

        now = time.time()
        if now - last_scale_time < COOLDOWN_SECONDS:
            continue

        replicas = current_replicas(apps_api)

        if throughput >= SCALE_UP_THROUGHPUT_MBPS and replicas < MAX_REPLICAS:
            scale_to(apps_api, replicas + 1)
            last_scale_time = now
        elif throughput <= SCALE_DOWN_THROUGHPUT_MBPS and replicas > MIN_REPLICAS:
            scale_to(apps_api, replicas - 1)
            last_scale_time = now


if __name__ == "__main__":
    main()
