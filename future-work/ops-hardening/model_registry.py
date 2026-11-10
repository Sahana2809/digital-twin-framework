"""
Model persistence/versioning for `ml_anomaly_detector.py`'s classifier.

On `main`, the Random Forest trains from scratch in memory every time the
detector process starts — no saved artifact, no version history, no way to
know which model made a given decision after the fact.

This saves each trained model to disk with a version tag, keeps a small
manifest of what was trained when (and on how much data), and loads the
latest version at startup instead of retraining blind on every boot.

Requires: joblib
"""

import json
import os
from datetime import datetime, timezone

import joblib

REGISTRY_DIR = "model_registry"
MANIFEST_PATH = os.path.join(REGISTRY_DIR, "manifest.json")


def _load_manifest():
    if not os.path.exists(MANIFEST_PATH):
        return {"versions": []}
    with open(MANIFEST_PATH, "r") as f:
        return json.load(f)


def _save_manifest(manifest):
    os.makedirs(REGISTRY_DIR, exist_ok=True)
    with open(MANIFEST_PATH, "w") as f:
        json.dump(manifest, f, indent=2)


def save_model(model, training_size, notes=""):
    manifest = _load_manifest()
    version = len(manifest["versions"]) + 1
    filename = f"model_v{version}.joblib"

    os.makedirs(REGISTRY_DIR, exist_ok=True)
    joblib.dump(model, os.path.join(REGISTRY_DIR, filename))

    manifest["versions"].append({
        "version": version,
        "filename": filename,
        "trained_at": datetime.now(timezone.utc).isoformat(),
        "training_size": training_size,
        "notes": notes,
    })
    _save_manifest(manifest)
    print(f"Saved model version {version} ({filename})")
    return version


def load_latest_model():
    manifest = _load_manifest()
    if not manifest["versions"]:
        return None, None
    latest = manifest["versions"][-1]
    model = joblib.load(os.path.join(REGISTRY_DIR, latest["filename"]))
    return model, latest


if __name__ == "__main__":
    from sklearn.ensemble import RandomForestClassifier
    import numpy as np

    # Smoke test: save a trivially-trained model, then load it back.
    X = np.random.rand(50, 5)
    y = np.random.randint(0, 4, 50)
    model = RandomForestClassifier(n_estimators=10).fit(X, y)

    save_model(model, training_size=len(X), notes="smoke test")
    loaded_model, metadata = load_latest_model()
    print(f"Loaded version {metadata['version']} trained at {metadata['trained_at']}")
