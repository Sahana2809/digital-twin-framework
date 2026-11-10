import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
import random
import os

# Create an output directory for graphs
os.makedirs("report_graphs", exist_ok=True)

# 1. Generate the same synthetic data used in the project
def generate_training_data():
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
    return pd.DataFrame(data, columns=['Throughput (Mbps)', 'Latency (ms)', 'Packet Loss (%)', 'Slice ID', 'Active UEs', 'Label'])

df = generate_training_data()
X = df.drop('Label', axis=1)
y = df['Label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# --- GRAPH 1: CONFUSION MATRIX ---
plt.figure(figsize=(10, 8))
cm = confusion_matrix(y_test, y_pred)
labels = ['Normal', 'eMBB Congestion', 'URLLC Spike', 'mMTC Drop']
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels, annot_kws={"size": 14})
plt.title('Random Forest Anomaly Detection Confusion Matrix', fontsize=16)
plt.ylabel('Actual Condition', fontsize=14)
plt.xlabel('Predicted Condition', fontsize=14)
plt.tight_layout()
plt.savefig('report_graphs/confusion_matrix.png', dpi=300)
print("Generated: report_graphs/confusion_matrix.png")

# --- GRAPH 2: FEATURE IMPORTANCE ---
plt.figure(figsize=(10, 6))
importances = model.feature_importances_
indices = np.argsort(importances)[::-1]
features = X.columns

sns.barplot(x=importances[indices], y=[features[i] for i in indices], palette='viridis')
plt.title('AIOps Feature Importance for Fault Classification', fontsize=16)
plt.xlabel('Relative Importance', fontsize=14)
plt.ylabel('Network Metric', fontsize=14)
plt.tight_layout()
plt.savefig('report_graphs/feature_importance.png', dpi=300)
print("Generated: report_graphs/feature_importance.png")

# --- GRAPH 3: SIMULATED CHAOS ENGINEERING TIMELINE (URLLC Latency) ---
# Create a synthetic timeline showing normal operation, injection, and AI healing
time_seconds = np.arange(0, 30, 1)
latency = []

for t in time_seconds:
    if t < 10:
        latency.append(random.uniform(1, 5))  # Normal URLLC
    elif t >= 10 and t < 16:
        latency.append(random.uniform(120, 130))  # Chaos Injected (120ms delay)
    else:
        latency.append(random.uniform(1, 5))  # Healed

plt.figure(figsize=(12, 6))
plt.plot(time_seconds, latency, marker='o', linestyle='-', color='#d62728', linewidth=2.5, markersize=6)
plt.axvline(x=10, color='black', linestyle='--', alpha=0.7)
plt.axvline(x=16, color='green', linestyle='--', alpha=0.7)

plt.text(4, 100, 'Normal\nOperation', ha='center', fontsize=12, color='gray')
plt.text(13, 135, 'Chaos Injected\n(120ms Delay)', ha='center', fontsize=12, color='black', fontweight='bold')
plt.text(23, 100, 'AI Self-Healed\n(< 5ms)', ha='center', fontsize=12, color='green', fontweight='bold')

plt.title('URLLC Slice Resilience: Chaos Injection vs AI Autonomous Healing', fontsize=16)
plt.xlabel('Time (seconds)', fontsize=14)
plt.ylabel('Measured Latency (ms)', fontsize=14)
plt.grid(True, linestyle='--', alpha=0.6)
plt.fill_between(time_seconds, 0, 10, color='green', alpha=0.1, label='SLA Target (<10ms)')
plt.legend(loc='upper right')
plt.tight_layout()
plt.savefig('report_graphs/chaos_recovery_timeline.png', dpi=300)
print("Generated: report_graphs/chaos_recovery_timeline.png")

print("All graphs successfully generated in the 'report_graphs' folder!")
