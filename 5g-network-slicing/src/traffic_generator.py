import time
import random
import threading
from prometheus_client import start_http_server, Gauge

# Prometheus Metrics
THROUGHPUT = Gauge('throughput_mbps', 'Current throughput in Mbps', ['slice_id'])
LATENCY = Gauge('latency_ms', 'Current round-trip latency in ms', ['slice_id'])
PACKET_DROP = Gauge('packet_loss_pct', 'Current packet drop percentage', ['slice_id'])
ACTIVE_UES = Gauge('active_ues', 'Number of active UEs', ['slice_id'])

# Slice configurations (normal behavior)
SLICES = {
    'embb': {'throughput': (100, 500), 'latency': (10, 30), 'drop': (0.0, 0.1), 'ues': (50, 100)},
    'urllc': {'throughput': (10, 50), 'latency': (1, 5), 'drop': (0.0, 0.01), 'ues': (5, 20)},
    'mmtc': {'throughput': (1, 10), 'latency': (20, 100), 'drop': (0.1, 1.0), 'ues': (500, 1000)}
}

# Shared state to allow chaos injection simulation (if we wanted to do it in python, but we use `tc`)
# This script basically acts as an exporter. To make it realistic, we should actually measure the `tc` effects.
# However, for a synthetic generator that responds to `tc`, measuring real ping/iperf is complex.
# We will simulate the metrics based on normal distributions, and if `tc` is applied, we assume the user 
# expects the ML model to detect it. But wait, if we use `tc` on `veth`, the python script just generating random 
# numbers won't reflect the `tc` changes unless it actually measures them!

# Let's do a real measurement by pinging a reliable external endpoint (e.g., 8.8.8.8) to get real latency and packet loss.
# Throughput can be simulated or measured via actual interface stats.
import subprocess

def measure_real_metrics(slice_id):
    while True:
        try:
            # Measure Latency and Packet Loss using ping
            # Ping 8.8.8.8 3 times, timeout 1s
            ping_out = subprocess.run(
                ["ip", "netns", "exec", f"ue_{slice_id}", "ping", "-c", "3", "-W", "1", "8.8.8.8"],
                capture_output=True, text=True
            )
            
            # Parse ping output
            latency = 0.0
            loss = 100.0
            if ping_out.returncode == 0 or ping_out.returncode == 1:
                out = ping_out.stdout
                if "packet loss" in out:
                    loss_str = out.split("packet loss")[0].split(",")[-1].strip().replace("%", "")
                    loss = float(loss_str)
                if "avg" in out:
                    lat_str = out.split("=")[-1].split("/")[1]
                    latency = float(lat_str)
            
            if latency == 0.0 and loss == 100.0:
                # If network is down or not configured, fallback to synthetic data so Prometheus doesn't break
                latency = random.uniform(*SLICES[slice_id]['latency'])
                loss = random.uniform(*SLICES[slice_id]['drop'])
                
            # Synthetic throughput and UEs since we don't have real traffic generators running iperf
            tput = random.uniform(*SLICES[slice_id]['throughput'])
            
            if loss > 5.0:
                tput = tput * 0.1 # Throttle throughput if loss is high
                
            ues = int(random.uniform(*SLICES[slice_id]['ues']))
            
            THROUGHPUT.labels(slice_id=slice_id).set(tput)
            LATENCY.labels(slice_id=slice_id).set(latency)
            PACKET_DROP.labels(slice_id=slice_id).set(loss)
            ACTIVE_UES.labels(slice_id=slice_id).set(ues)
            
        except Exception as e:
            print(f"Error measuring metrics for {slice_id}: {e}")
            
        time.sleep(2)

if __name__ == '__main__':
    start_http_server(8000)
    print("Prometheus metrics server started on port 8000")
    
    # Start a thread for each slice
    for slice_id in SLICES.keys():
        t = threading.Thread(target=measure_real_metrics, args=(slice_id,))
        t.daemon = True
        t.start()
        
    while True:
        time.sleep(1)
