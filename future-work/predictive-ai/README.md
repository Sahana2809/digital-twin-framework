# Predictive AI Engine

## `lstm_forecaster.py`

A working PyTorch LSTM that forecasts an *incoming* anomaly from a 20-second
sliding window of telemetry, instead of `main`'s Random Forest, which only
classifies the current instant. See the module docstring for usage.

It's currently trained on synthetic ramp sequences (normal telemetry easing
into a fault signature over the last few samples of each window) — enough to
prove the architecture and the `predict_next()` hook work, but not yet
validated against a real network.

## Collecting real training data (for 2.2 in the roadmap)

To replace the synthetic sequences with something trustworthy:

1. Run the existing stack on `main` (`docker-compose up`, `setup_network.sh`,
   `traffic_generator.py`).
2. Write a small logger that polls the same Prometheus metrics
   `ml_anomaly_detector.py` already queries (`throughput_mbps`, `latency_ms`,
   `packet_loss_pct`, `active_ues`) every 2s and appends them to a CSV/parquet
   file, tagged with slice_id and timestamp.
3. While that logger runs, deliberately trigger each `dashboard.py` chaos
   button (URLLC latency, mMTC loss, eMBB congestion) multiple times, each for
   a few minutes, with normal-operation gaps in between.
4. Label each row with the fault that was *actually* active at that timestamp
   (you know this because you're the one clicking the buttons) — not a
   `random.uniform()` guess.
5. Slice that labeled time series into `SEQ_LEN`-sized windows and retrain
   `LSTMForecaster` on it instead of `generate_training_sequences()`.

This turns the model from "proves the ramp-detection idea works on data
designed to be learnable" into "proves it works on what `tc` actually does to
this specific network," which is the real bar for the predictive-healing
claim.
