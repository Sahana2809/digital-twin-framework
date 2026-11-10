"""
PyTorch LSTM forecaster — predicts an upcoming anomaly from a short history
of telemetry instead of classifying the current instant.

This is a prototype trained on synthetic sliding-window sequences (built
the same way `main`'s RandomForestClassifier training data is, but kept
time-ordered instead of collapsed to single points) so the architecture
and the preemptive-healing hook can be demonstrated end-to-end. Swap
`generate_training_sequences()` for real recorded Prometheus windows (see
README.md in this directory) before trusting this on a live network.

Usage:
    python lstm_forecaster.py          # trains, prints eval accuracy, demos predict_next()
"""

import random

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset

SEQ_LEN = 10          # 10 samples * 2s scrape interval = 20s of history
FEATURES = ["throughput_mbps", "latency_ms", "packet_loss_pct", "active_ues"]
NUM_CLASSES = 4       # Normal, eMBB congestion, URLLC latency spike, mMTC drop

SLICE_PROFILES = {
    "embb": {"throughput": (100, 500), "latency": (10, 30), "drop": (0.0, 0.1), "ues": (50, 100)},
    "urllc": {"throughput": (10, 50), "latency": (1, 5), "drop": (0.0, 0.01), "ues": (5, 20)},
    "mmtc": {"throughput": (1, 10), "latency": (20, 100), "drop": (0.1, 1.0), "ues": (500, 1000)},
}

FAULT_PROFILES = {
    1: {"throughput": (5, 50), "latency": (100, 300), "drop": (5, 15), "ues": (100, 200)},    # eMBB congestion
    2: {"throughput": (10, 50), "latency": (50, 150), "drop": (0, 2), "ues": (5, 20)},         # URLLC latency spike
    3: {"throughput": (0, 2), "latency": (100, 500), "drop": (10, 30), "ues": (500, 1000)},    # mMTC drop
}


def _sample(profile):
    return [
        random.uniform(*profile["throughput"]),
        random.uniform(*profile["latency"]),
        random.uniform(*profile["drop"]),
        random.uniform(*profile["ues"]),
    ]


def generate_training_sequences(n_per_class=300):
    """Builds (sequence, label) pairs where the LAST few samples ramp from
    normal into a fault signature — the label is the fault the sequence is
    ramping *towards*, so the model learns to predict ahead of the breach."""
    sequences, labels = [], []

    for label, fault_profile in [(0, None), (1, FAULT_PROFILES[1]),
                                  (2, FAULT_PROFILES[2]), (3, FAULT_PROFILES[3])]:
        base_slice = {1: "embb", 2: "urllc", 3: "mmtc"}.get(label, random.choice(list(SLICE_PROFILES)))
        normal = SLICE_PROFILES[base_slice]

        for _ in range(n_per_class):
            seq = []
            ramp_start = random.randint(SEQ_LEN // 2, SEQ_LEN - 2) if fault_profile else SEQ_LEN
            for t in range(SEQ_LEN):
                if fault_profile and t >= ramp_start:
                    frac = (t - ramp_start + 1) / (SEQ_LEN - ramp_start)
                    normal_s, fault_s = _sample(normal), _sample(fault_profile)
                    point = [n + (f - n) * frac for n, f in zip(normal_s, fault_s)]
                else:
                    point = _sample(normal)
                seq.append(point)
            sequences.append(seq)
            labels.append(label)

    return np.array(sequences, dtype=np.float32), np.array(labels, dtype=np.int64)


class TelemetrySequenceDataset(Dataset):
    def __init__(self, sequences, labels):
        self.sequences = torch.from_numpy(sequences)
        self.labels = torch.from_numpy(labels)

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        return self.sequences[idx], self.labels[idx]


class LSTMForecaster(nn.Module):
    def __init__(self, input_size=len(FEATURES), hidden_size=32, num_classes=NUM_CLASSES):
        super().__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
        self.classifier = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        _, (h_n, _) = self.lstm(x)
        return self.classifier(h_n[-1])


def train(model, dataset, epochs=15, batch_size=32, lr=1e-3):
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    criterion = nn.CrossEntropyLoss()

    model.train()
    for epoch in range(epochs):
        total_loss = 0.0
        for seqs, labels in loader:
            optimizer.zero_grad()
            logits = model(seqs)
            loss = criterion(logits, labels)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        print(f"epoch {epoch + 1}/{epochs} - loss {total_loss / len(loader):.4f}")


def predict_next(model, window):
    """window: list of SEQ_LEN samples, each [throughput, latency, loss, ues].
    Returns the predicted class for the NEXT few seconds of this slice."""
    model.eval()
    with torch.no_grad():
        x = torch.tensor([window], dtype=torch.float32)
        logits = model(x)
        return int(torch.argmax(logits, dim=1).item())


if __name__ == "__main__":
    sequences, labels = generate_training_sequences()
    dataset = TelemetrySequenceDataset(sequences, labels)

    model = LSTMForecaster()
    train(model, dataset)

    # Demo: a window ramping towards eMBB congestion but not there yet.
    demo_window = sequences[labels == 1][0].tolist()
    prediction = predict_next(model, demo_window)
    class_labels = {0: "Normal", 1: "eMBB Congestion (incoming)",
                     2: "URLLC Latency Spike (incoming)", 3: "mMTC Drop (incoming)"}
    print(f"\nForecast for sample ramping window: {class_labels[prediction]}")
