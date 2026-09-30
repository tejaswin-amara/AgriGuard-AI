# Model Card — Crop Disease Inference

> **Status:** Deterministic demo model; not field validated.

## Intended purpose

Demonstrate the end-to-end path from image upload through API validation, disease inference, RAG retrieval, and advisory presentation.

## Current implementation

- Framework: PyTorch / TorchVision
- Architecture definition: MobileNetV2
- Class slots: 3
- Labels: `Healthy`, `Leaf Blight`, `Rust`
- Active weights: **none**
- Active inference mode: **deterministic demo**
- Image validation: Pillow
- API upload limit: 10 MB
- Accepted formats: JPEG, PNG, WebP

The active inference implementation does not execute the MobileNetV2 network. It validates the supplied image and returns a deterministic `Leaf Blight` result.

## Confidence semantics

The current source returns a fixed demo value of `0.85`. This is a demonstration field, **not a calibrated probability or validated model confidence**.

## Training data

No training pipeline or trained checkpoint is shipped for the current disease inference path.

Although a service-level provenance field contains the text `PlantVillage Public Leaf Dataset`, the repository does not currently provide evidence that the active model was trained or evaluated on that dataset.

## Evaluation

No valid real-world metrics are available.

Do not report accuracy, recall, precision, F1, calibration, or field performance for this implementation.

## Intended use

- software demonstration;
- API contract testing;
- UI/E2E evaluation;
- RAG integration demonstration.

## Out of scope

- diagnosis of crop disease;
- pesticide or fungicide prescription;
- yield-loss estimation;
- field-treatment decisions;
- claims about model performance in production.

## Safety and limitations

Any disease result must be treated as a prototype placeholder. The correct escalation path for real agricultural decisions is qualified local agronomic/extension advice and, where appropriate, field or laboratory assessment.

