# Physical Edge-to-Cloud Integration

**Status: code written, untested on physical hardware** — I don't have an
ESP32 or the sensor board to run this end-to-end, so treat this as a
self-consistent starting point, not a validated integration.

## What's here

- [`esp32_mmtc_node.ino`](esp32_mmtc_node.ino) — Arduino sketch for an ESP32:
  reads an MPU6050 accelerometer/temperature sensor and publishes readings +
  a heartbeat over MQTT every 2 seconds (matching `traffic_generator.py`'s
  scrape cadence on `main`).
- [`mqtt_bridge.py`](mqtt_bridge.py) — a Python MQTT subscriber that:
  1. Exposes `heartbeat_gap_seconds{slice_id="mmtc"}` as a Prometheus metric —
     if the slice is dropping packets, this gap grows, and
     `ml_anomaly_detector.py` can be pointed at it like any other metric.
  2. Relays each sensor payload into the `ue_mmtc` namespace as a real UDP
     packet, so the "IoT traffic" physically transits the slice's
     veth → UPF → tunnel path instead of only existing on the MQTT side.

## Hardware setup (needed to actually validate this)

1. **Board:** any ESP32 dev board (e.g., ESP32-WROOM-32).
2. **Sensor:** MPU6050 accelerometer/gyro breakout, wired over I2C
   (SDA → GPIO21, SCL → GPIO22, VCC → 3.3V, GND → GND on most boards).
3. **Libraries** (Arduino IDE / PlatformIO): `PubSubClient`,
   `Adafruit_MPU6050`, `Adafruit_Sensor`.
4. Fill in `WIFI_SSID`, `WIFI_PASSWORD`, and `MQTT_BROKER` (the IP of the
   machine running `mqtt_bridge.py`) in `esp32_mmtc_node.ino`.
5. Run an MQTT broker (e.g., `mosquitto`) on the bridge host, then run
   `mqtt_bridge.py` alongside the existing `traffic_generator.py`.
6. To prove the closed loop: inject the mMTC packet-loss chaos button in
   `dashboard.py`, confirm `heartbeat_gap_seconds` rises on the real device's
   heartbeat (not synthetic data), and confirm the anomaly detector reacts to
   it the same way it reacts to the existing synthetic mMTC metrics.
