/*
 * ESP32 mMTC edge node.
 *
 * Reads a sensor (MPU6050 accelerometer by default — swap for whatever's on
 * hand) and publishes readings over MQTT, plus a heartbeat on its own topic.
 * The Python side (mqtt_bridge.py) forwards these into the ue_mmtc namespace
 * and watches the heartbeat gap, so a real packet-loss event on the mMTC
 * slice shows up as this device's messages actually failing to arrive.
 *
 * Untested on physical hardware — written against the standard
 * Adafruit_MPU6050 + PubSubClient APIs. Wiring/library notes in README.md.
 */

#include <WiFi.h>
#include <PubSubClient.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

const char* WIFI_SSID = "YOUR_WIFI_SSID";
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";
const char* MQTT_BROKER = "YOUR_BRIDGE_HOST";   // host running mqtt_bridge.py
const int MQTT_PORT = 1883;
const char* DEVICE_ID = "esp32-mmtc-01";

const char* TOPIC_SENSOR = "campus/mmtc/sensor";
const char* TOPIC_HEARTBEAT = "campus/mmtc/heartbeat";

const unsigned long PUBLISH_INTERVAL_MS = 2000;  // match traffic_generator.py's cadence

WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);
Adafruit_MPU6050 mpu;
unsigned long lastPublish = 0;

void connectWifi() {
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected: " + WiFi.localIP().toString());
}

void connectMqtt() {
  mqttClient.setServer(MQTT_BROKER, MQTT_PORT);
  while (!mqttClient.connected()) {
    Serial.println("Connecting to MQTT broker...");
    if (mqttClient.connect(DEVICE_ID)) {
      Serial.println("MQTT connected");
    } else {
      delay(1000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  Wire.begin();

  if (!mpu.begin()) {
    Serial.println("MPU6050 not found - check wiring");
  }

  connectWifi();
  connectMqtt();
}

void loop() {
  if (!mqttClient.connected()) {
    connectMqtt();
  }
  mqttClient.loop();

  unsigned long now = millis();
  if (now - lastPublish >= PUBLISH_INTERVAL_MS) {
    lastPublish = now;

    sensors_event_t accel, gyro, temp;
    mpu.getEvent(&accel, &gyro, &temp);

    char payload[160];
    snprintf(payload, sizeof(payload),
             "{\"device_id\":\"%s\",\"accel_x\":%.3f,\"accel_y\":%.3f,\"accel_z\":%.3f,\"temp_c\":%.2f}",
             DEVICE_ID, accel.acceleration.x, accel.acceleration.y, accel.acceleration.z, temp.temperature);

    mqttClient.publish(TOPIC_SENSOR, payload);
    mqttClient.publish(TOPIC_HEARTBEAT, DEVICE_ID);
  }
}
