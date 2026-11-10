import re

with open("wmn_lab_report_sahana_extended.md", "r", encoding="utf-8") as f:
    content = f.read()

# Dictionary mapping image filename to its descriptive caption
captions = {
    "exp1.png": "Signal strength for Friis model (-64 dBm)",
    "exp1(1).png": "Signal strength for Log-Distance model (-75 dBm)",
    "exp1(2).png": "Signal strength for ITU model (-72 dBm)",
    "figure1exp1.png": "Bar chart comparing signal strength across different propagation models",
    "figure2exp1.png": "Dashboard summarizing Wireless Propagation Models Performance",
    "figure3exp1.png": "Bar chart showing performance scores for propagation models",
    "figure5exp1.png": "Bar chart with propagation model comparison scores",
    "experiment2.png": "Mininet-WiFi Wireless Traffic Analysis Dashboard",
    "exp3.png": "Wireless Scanning Performance Dashboard",
    "experiment3.png": "CLI output for active vs passive WiFi scanning",
    "exp4.png": "CLI output showing handover latency and RSSI difference",
    "exp5.png": "Open5GS WebUI dashboard showing subscriber search",
    "exp5(1).png": "Editing subscriber configuration in Open5GS WebUI",
    "exp6.png": "Configuring Network Slicing S-NSSAI in Open5GS WebUI",
    "exp7.png": "CLI output showing successful NG Setup and gNB connection",
    "exp7(1).png": "CLI output showing successful UE Registration and PDU Session setup",
    "exp8.png": "Starting Open5GS WebUI server using npm run dev",
    "exp9.png": "CLI output showing active Open5GS daemon services"
}

# Replace the generic alt text with the specific caption
for img, caption in captions.items():
    # We look for something like ![Experiment X Figure](img) and replace it with ![caption](img)
    # The regex needs to handle the exact markdown we inserted earlier.
    pattern = r'!\[.*?\]\(' + re.escape(img) + r'\)'
    replacement = f'![{caption}]({img})'
    content = re.sub(pattern, replacement, content)

with open("wmn_lab_report_sahana_extended.md", "w", encoding="utf-8") as f:
    f.write(content)
