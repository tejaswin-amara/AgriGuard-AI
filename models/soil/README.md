# Soil Health Model

## Status

**Synthetic-data prototype. Not field validated.**

## Current implementation

The model uses XGBoost classification over five inputs:

- nitrogen;
- phosphorus;
- potassium;
- pH;
- moisture.

The training script generates **1,000 synthetic samples** with a fixed random seed of 42. Labels are assigned from heuristic thresholds rather than laboratory measurements.

### Classes

- `Optimal`
- `High Risk (pH imbalance)`
- `Suboptimal (Stress)`

## Generate the model

From the repository root:

```bash
python models/soil/train.py
```

This creates:

```text
models/soil/soil_model_synthetic.pkl
```

The generated artifact is not intended to be committed to Git.

## Inference

`inference.py` loads the generated artifact when it exists. If the artifact is missing, the current code uses a deterministic demo fallback.

## Limitations

The model is not suitable for:

- fertilizer prescriptions;
- soil laboratory diagnosis;
- calibrated agronomic recommendations;
- field performance claims.

Real deployment requires representative laboratory/field measurements, documented units and sampling procedures, validation data, geographic/crop coverage, and domain review.

See [the soil model card](../../docs/model-card/SOIL_MODEL_CARD.md).
