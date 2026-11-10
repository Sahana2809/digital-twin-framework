"""
MQTT -> Prometheus bridge for the ESP32 mMTC edge node.

Subscribes to the ESP32's sensor + heartbeat topics and exposes a
`heartbeat_gap_seconds` Prometheus gauge for slice_id="mmtc" — if the
mMTC namespace is suffering real packet loss (injected via `tc` or
genuinely occurring), this gap grows, which `ml_anomaly_detector.py`
can treat exactly like any other mMTC metric.

This also republishes each sensor reading into the ue_mmtc namespace as a
UDP packet, so the "real" traffic physically transits the slice's veth/UPF
path rather than only existing on the MQTT side.

Requires: paho-mqtt, prometheus_client
"""

import json
import socket
import subprocess
import time

import paho.mqtt.client as mqtt
from prometheus_client import Gauge, start_http_server

MQTT_BROKER = "0.0.0.0"
MQTT_PORT = 1883
TOPIC_SENSOR = "campus/mmtc/sensor"
TOPIC_HEARTBEAT = "campus/mmtc/heartbeat"

NAMESPACE = "ue_mmtc"
RELAY_HOST = "10.3.1.1"   # host-side veth IP for the mmtc slice (see setup_network.sh)
RELAY_PORT = 9100

HEARTBEAT_GAP = Gauge("heartbeat_gap_seconds", "Seconds since last ESP32 heartbeat", ["slice_id"])
SENSOR_TEMP = Gauge("edge_sensor_temp_c", "Latest ESP32 temperature reading", ["device_id"])

_last_heartbeat = {"t": None}


def relay_into_namespace(payload_bytes):
    """Sends the sensor payload through the mmtc namespace so it's real
    traffic on the slice, not just a side-channel MQTT message."""
    try:
        subprocess.run(
            ["ip", "netns", "exec", NAMESPACE, "python3", "-c",
             f"import socket; s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM); "
             f"s.sendto({payload_bytes!r}, ('{RELAY_HOST}', {RELAY_PORT}))"],
            timeout=2,
        )
    except Exception as exc:
        print(f"Failed to relay into {NAMESPACE}: {exc}")


def on_message(client, userdata, msg):
    if msg.topic == TOPIC_HEARTBEAT:
        _last_heartbeat["t"] = time.time()
        return

    if msg.topic == TOPIC_SENSOR:
        try:
            data = json.loads(msg.payload)
            SENSOR_TEMP.labels(device_id=data.get("device_id", "unknown")).set(data.get("temp_c", 0.0))
        except json.JSONDecodeError:
            pass
        relay_into_namespace(msg.payload)


def watch_heartbeat_gap():
    while True:
        time.sleep(2)
        if _last_heartbeat["t"] is None:
            continue
        HEARTBEAT_GAP.labels(slice_id="mmtc").set(time.time() - _last_heartbeat["t"])


def main():
    start_http_server(8010)
    print("Bridge metrics server started on port 8010")

    client = mqtt.Client()
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT)
    client.subscribe(TOPIC_SENSOR)
    client.subscribe(TOPIC_HEARTBEAT)

    import threading
    threading.Thread(target=watch_heartbeat_gap, daemon=True).start()

    client.loop_forever()


if __name__ == "__main__":
    main()
