# Disease Detection Model

## Status

**Deterministic demo/prototype. Not field validated.**

## Current implementation

- Architecture definition: PyTorch MobileNetV2 in `model.py`.
- Nominal classes: `Healthy`, `Leaf Blight`, `Rust`.
- Active inference: `inference.py`.
- Image validation: Pillow.
- Trained weights: none loaded by the active inference path.
- Output: deterministic `Leaf Blight` demo result with a fixed confidence field.

The current inference code intentionally does not run an untrained MobileNetV2 network. It validates the uploaded image and returns deterministic demo output so the API/UI flow is reproducible.

## Limitations

This implementation is not a crop-disease diagnosis system.

Do not use it for:

- field diagnosis;
- pesticide/fungicide selection;
- treatment dosage;
- yield-loss estimation;
- claims of model accuracy.

A production disease model would require an appropriately licensed dataset, trained checkpoints, holdout evaluation, calibration, field validation, and documented model monitoring.

See [the disease model card](../../docs/model-card/DISEASE_MODEL_CARD.md).
