# Threat Model
This document defines the high-level threat model for AgriGuard AI.

## Key Considerations
- Data Privacy: Minimize PII collected from farmers.
- Model Integrity: Models are demos and must not be blindly trusted for field dosing or real-world diagnostics.
- Service Abuse: Need to rate limit endpoints.
