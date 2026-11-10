import streamlit as st
import pandas as pd
import requests
import time
import os
import subprocess
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="5G Digital Twin & Chaos Engineering Command Center", layout="wide")

PROMETHEUS_URL = "http://localhost:9090"
ALERTS_LOG = "alerts.log"

st.title("🌐 5G Smart Campus Digital Twin & Chaos Engineering Dashboard")
st.markdown("Monitor the 5G Network Slicing Digital Twin in real-time, inject chaos faults, and observe AI-driven Self-Healing.")

def fetch_metric(metric_name):
    try:
        response = requests.get(f"{PROMETHEUS_URL}/api/v1/query", params={'query': metric_name})
        results = response.json().get('data', {}).get('result', [])
        data = {}
        for res in results:
            slice_id = res['metric'].get('slice_id', 'unknown')
            val = float(res['value'][1])
            data[slice_id] = val
        return data
    except Exception as e:
        return {}

# ----------------- CHAOS ENGINEERING PANEL -----------------
st.sidebar.header("⚠️ Chaos Engineering")
st.sidebar.markdown("Inject real-world telecom failures into specific network slices.")

def run_tc_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
        st.sidebar.success(f"Executed: `{command}`")
    except subprocess.CalledProcessError as e:
        st.sidebar.error(f"Failed to execute command: {e}")

if st.sidebar.button("Inject URLLC Latency (120ms)"):
    cmd = "sudo ip netns exec ue_urllc tc qdisc add dev veth0 root netem delay 120ms"
    run_tc_command(cmd)

if st.sidebar.button("Inject mMTC Packet Loss (20%)"):
    cmd = "sudo ip netns exec ue_mmtc tc qdisc add dev veth0 root netem loss 20%"
    run_tc_command(cmd)

if st.sidebar.button("Inject eMBB Congestion (Throttling)"):
    cmd = "sudo ip netns exec ue_embb tc qdisc add dev veth0 root tbf rate 1mbit burst 32kbit latency 400ms"
    run_tc_command(cmd)

st.sidebar.markdown("---")

if st.sidebar.button("🩹 Heal Network (Clear Rules)"):
    run_tc_command("sudo ip netns exec ue_urllc tc qdisc del dev veth0 root 2>/dev/null || true")
    run_tc_command("sudo ip netns exec ue_mmtc tc qdisc del dev veth0 root 2>/dev/null || true")
    run_tc_command("sudo ip netns exec ue_embb tc qdisc del dev veth0 root 2>/dev/null || true")
    st.sidebar.success("Network healed. All slices returned to normal operation.")


# ----------------- REAL-TIME METRICS -----------------
col1, col2 = st.columns([3, 1])

# Initialize session state for storing historical data
if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=['timestamp', 'slice', 'throughput', 'latency', 'loss', 'ues'])

# Create placeholders
metrics_placeholder = col1.empty()
alerts_placeholder = col2.empty()

def update_dashboard():
    # Fetch Data
    tput = fetch_metric('throughput_mbps')
    lat = fetch_metric('latency_ms')
    loss = fetch_metric('packet_loss_pct')
    ues = fetch_metric('active_ues')
    
    timestamp = datetime.now()
    
    new_rows = []
    for slice_id in ['embb', 'urllc', 'mmtc']:
        if slice_id in tput:
            new_rows.append({
                'timestamp': timestamp,
                'slice': slice_id.upper(),
                'throughput': tput.get(slice_id, 0),
                'latency': lat.get(slice_id, 0),
                'loss': loss.get(slice_id, 0),
                'ues': ues.get(slice_id, 0)
            })
    
    if new_rows:
        new_df = pd.DataFrame(new_rows)
        st.session_state.history = pd.concat([st.session_state.history, new_df]).tail(150) # Keep last 150 points
    
    # Render Metrics UI
    with metrics_placeholder.container():
        st.subheader("Real-Time Telemetry")
        
        c1, c2, c3 = st.columns(3)
        slices = ['EMBB', 'URLLC', 'MMTC']
        cols = [c1, c2, c3]
        
        for i, s_id in enumerate(slices):
            latest = st.session_state.history[st.session_state.history['slice'] == s_id].tail(1)
            if not latest.empty:
                cols[i].metric(f"{s_id} Throughput", f"{latest['throughput'].values[0]:.1f} Mbps")
                cols[i].metric(f"{s_id} Latency", f"{latest['latency'].values[0]:.1f} ms")
                cols[i].metric(f"{s_id} Pkt Drop", f"{latest['loss'].values[0]:.1f} %")
        
        st.markdown("---")
        
        # Charts
        if not st.session_state.history.empty:
            fig_tput = px.line(st.session_state.history, x='timestamp', y='throughput', color='slice', title='Throughput (Mbps)')
            fig_lat = px.line(st.session_state.history, x='timestamp', y='latency', color='slice', title='Latency (ms)')
            
            ch1, ch2 = st.columns(2)
            ch1.plotly_chart(fig_tput, use_container_width=True)
            ch2.plotly_chart(fig_lat, use_container_width=True)

    # Render Alerts UI
    with alerts_placeholder.container():
        st.subheader("🚨 AIOps & Self-Healing Log")
        st.markdown("*(AI-Driven Anomaly Detection & Autonomous Recovery)*")
        if os.path.exists(ALERTS_LOG):
            with open(ALERTS_LOG, 'r') as f:
                alerts = f.readlines()[-15:] # Last 15 alerts
            
            if alerts:
                for alert in reversed(alerts):
                    st.error(alert.strip())
            else:
                st.success("Network Operating Normally.")
        else:
            st.info("Waiting for anomaly detector...")

# Auto-refresh loop (using Streamlit's experimental rerun or a simple while loop if run via standard python isn't ideal for streamlit, 
# but Streamlit runs top-to-bottom. We use a rerun hack)
update_dashboard()
time.sleep(2)
st.rerun()
