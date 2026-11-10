"""
Persistent alert/event storage using the `mongodb` container that's already
deployed in `docker-compose.yml` on `main` but currently unused.

Replaces `alerts.log` (flat file, gone on restart) and the dashboard's
in-memory `st.session_state.history` (gone on every rerun) with a durable
collection that survives restarts and can be queried/reported on.

Requires: pymongo
"""

from datetime import datetime, timezone

from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "digital_twin"
COLLECTION = "alerts"


def get_collection():
    client = MongoClient(MONGO_URI)
    return client[DB_NAME][COLLECTION]


def log_event(slice_id, event_type, message, metrics=None):
    """event_type: 'anomaly_detected' | 'healing_attempt' | 'healing_verified' | 'healing_escalated'"""
    doc = {
        "timestamp": datetime.now(timezone.utc),
        "slice_id": slice_id,
        "event_type": event_type,
        "message": message,
        "metrics": metrics or {},
    }
    get_collection().insert_one(doc)


def recent_events(limit=15):
    return list(get_collection().find().sort("timestamp", -1).limit(limit))


def events_for_slice(slice_id, limit=50):
    return list(get_collection().find({"slice_id": slice_id}).sort("timestamp", -1).limit(limit))


if __name__ == "__main__":
    # Smoke test: write one event, read it back.
    log_event("urllc", "anomaly_detected", "URLLC Latency Spike detected", {"latency_ms": 142.3})
    for event in recent_events(5):
        print(event)
