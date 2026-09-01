# Model Card: Crop Disease Classification

**Status: Demo/Prototype**

## Purpose
To classify crop leaf images into disease categories, providing early warning to smallholder farmers.

## Architecture
- **Planned**: A PyTorch CNN (e.g., MobileNetV2 or EfficientNet) using transfer learning.
- **Current Implementation**: The architecture is set up in `models/disease/model.py` using MobileNetV2, but the inference script (`inference.py`) currently returns a **deterministic mock result** to ensure a consistent evaluator experience without loading untrained weights.

## Training Data
None at this time. The model is a structural stub.

## Evaluation & Metrics
No metrics available. Any future metrics must be produced by actual evaluation on a real dataset.

## Intended Use
Demonstrating the technical pipeline for the 1M1B AI for Sustainability project.

## Out-of-Scope Use
Actual agricultural diagnosis.

## Responsible AI Considerations
The model is explicitly labeled as a demo in the UI to prevent reliance on its outputs.
