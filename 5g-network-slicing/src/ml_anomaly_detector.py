import time
import requests
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from datetime import datetime
import os
import random
import subprocess
import warnings

# Silence harmless Scikit-Learn warnings
warnings.filterwarnings("ignore", category=UserWarning)

PROMETHEUS_URL = "http://localhost:9090"
ALERTS_LOG = "alerts.log"

def fetch_metric(metric_name):
    try:
        response = requests.get(f"{PROMETHEUS_URL}/api/v1/query", params={'query': metric_name})
        results = response.json()['data']['result']
        data = {}
        for res in results:
            slice_id = res['metric'].get('slice_id', 'unknown')
            val = float(res['value'][1])
            data[slice_id] = val
        return data
    except Exception as e:
        return {}

def generate_training_data():
    """Generates synthetic data to train the Random Forest Classifier"""
    data = []
    
    # Normal Operation (0)
    for _ in range(500):
        data.append([random.uniform(100, 500), random.uniform(10, 30), random.uniform(0, 0.1), 0, random.randint(50, 100), 0]) # eMBB
        data.append([random.uniform(10, 50), random.uniform(1, 5), random.uniform(0, 0.01), 1, random.randint(5, 20), 0]) # URLLC
        data.append([random.uniform(1, 10), random.uniform(20, 100), random.uniform(0.1, 1.0), 2, random.randint(500, 1000), 0]) # mMTC
        
    # eMBB Congestion (1)
    for _ in range(200):
        data.append([random.uniform(5, 50), random.uniform(100, 300), random.uniform(5, 15), 0, random.randint(100, 200), 1])
        
    # URLLC Latency Spike (2)
    for _ in range(200):
        data.append([random.uniform(10, 50), random.uniform(50, 150), random.uniform(0, 2), 1, random.randint(5, 20), 2])
        
    # mMTC Packet Drop Dropout (3)
    for _ in range(200):
        data.append([random.uniform(0, 2), random.uniform(100, 500), random.uniform(10, 30), 2, random.randint(500, 1000), 3])
        
    df = pd.DataFrame(data, columns=['throughput_mbps', 'latency_ms', 'packet_loss_pct', 'slice_id_encoded', 'active_ues', 'label'])
    return df

print("Generating synthetic data and training ML model...")
df = generate_training_data()
X = df[['throughput_mbps', 'latency_ms', 'packet_loss_pct', 'slice_id_encoded', 'active_ues']]
y = df['label']

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)
print("Model training complete.")

slice_map = {'embb': 0, 'urllc': 1, 'mmtc': 2}
class_labels = {
    0: 'Normal Operation',
    1: 'eMBB Slice Congestion',
    2: 'URLLC Latency Spike',
    3: 'mMTC Packet Drop Dropout'
}

def log_alert(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    alert = f"[{timestamp}] {message}\n"
    print(alert.strip())
    with open(ALERTS_LOG, 'a') as f:
        f.write(alert)

def heal_slice(slice_id):
    """Executes closed-loop automation to heal the network slice"""
    command = f"sudo ip netns exec ue_{slice_id} tc qdisc del dev veth0 root 2>/dev/null || true"
    try:
        subprocess.run(command, shell=True, check=True)
        log_alert(f"✅ SELF-HEALING SUCCESS: Cleared congestion rules for {slice_id.upper()} slice.")
    except Exception as e:
        log_alert(f"❌ SELF-HEALING FAILED for {slice_id.upper()}: {str(e)}")

# Clear old alerts
if os.path.exists(ALERTS_LOG):
    os.remove(ALERTS_LOG)

last_healed = {'embb': 0, 'urllc': 0, 'mmtc': 0}

print("Starting live Digital Twin inference and Self-Healing loop...")
while True:
    time.sleep(2)
    
    tput = fetch_metric('throughput_mbps')
    lat = fetch_metric('latency_ms')
    loss = fetch_metric('packet_loss_pct')
    ues = fetch_metric('active_ues')
    
    for slice_id in slice_map.keys():
        if slice_id in tput and slice_id in lat and slice_id in loss and slice_id in ues:
            
            # Format as DataFrame to prevent warnings and match training data exactly
            features = pd.DataFrame([[
                tput[slice_id],
                lat[slice_id],
                loss[slice_id],
                slice_map[slice_id],
                ues[slice_id]
            ]], columns=['throughput_mbps', 'latency_ms', 'packet_loss_pct', 'slice_id_encoded', 'active_ues'])
            
            prediction = model.predict(features)[0]
            current_time = time.time()
            
            if prediction != 0 and (current_time - last_healed[slice_id] > 10):
                log_alert(f"🚨 ANOMALY on {slice_id.upper()}: {class_labels[prediction]} detected! TPUT={tput[slice_id]:.1f}, LAT={lat[slice_id]:.1f}, LOSS={loss[slice_id]:.1f}%")
                log_alert(f"⚙️ TRIGGERING AI SELF-HEALING for {slice_id.upper()}...")
                heal_slice(slice_id)
                last_healed[slice_id] = current_time