# Design Note: Multi-Host Realism

**Status: design only — needs real multi-VM infrastructure to validate, not something a single dev machine can honestly prototype.**

## Problem

On `main`, the entire "network" lives on one Linux kernel: the Open5GS containers, the three UE network namespaces, and all the veth/`tc`/`iptables` plumbing connecting them are all on one host. That's a single point of failure and doesn't reflect how a real deployment splits the Radio Access Network (RAN) side from the Core.

## Target topology

```
┌─────────────────────┐        GRE / IPsec tunnel        ┌─────────────────────┐
│   "Edge" host        │ ───────────────────────────────▶│   "Core" host        │
│  (gNB-adjacent)       │                                  │  (datacenter/cloud)  │
│                       │                                  │                      │
│  ue_embb ─┐           │                                  │  NRF                 │
│  ue_urllc ─┼─ veth ───┼── GRE tunnel per slice ──────────┼─ AMF                 │
│  ue_mmtc ─┘           │                                  │  SMF                 │
│                       │                                  │  UPF x3 (one/slice)  │
└─────────────────────┘                                  └─────────────────────┘
```

- The **edge host** keeps the three network namespaces (`ue_embb`, `ue_urllc`, `ue_mmtc`) and the chaos-injection `tc` rules — this is the part that's physically "at the campus."
- The **core host** runs NRF/AMF/SMF/UPF — this is the part a real operator would run in a regional datacenter.
- Each slice's namespace traffic is carried over its own GRE (or IPsec, for anything claiming to be production) tunnel to keep the same per-slice isolation that today's `ogstunN` routing provides locally, just stretched across a WAN link instead of a loopback.

## What changes in the existing code

- `scripts/setup_network.sh` splits into `setup_network_edge.sh` (namespaces + GRE tunnel endpoints only) and relies on the core host's UPFs being reachable at a routable address instead of `ogstunN` being on the same box.
- `docker-compose.yml` / the [Kubernetes manifests](k8s/) move to running only on the core host; the edge host runs nothing but `setup_network_edge.sh` and the chaos-injection tooling.
- `traffic_generator.py` and `ml_anomaly_detector.py` need to agree on which host they run on — telemetry collection (pings from inside the namespaces) stays on the edge host, while Prometheus/the detector can live on either side as long as the port is routable.

## Why this isn't prototyped here

Everything above is real infrastructure work — provisioning two VMs/hosts, standing up a GRE or IPsec tunnel between them, and re-verifying that policy-based routing still forces slice isolation across a WAN hop. Faking it with two Docker containers on one host wouldn't actually test the thing that matters (a real network hop with real latency/loss in between), so it's left as a scoped design rather than code that only pretends to validate the idea.
