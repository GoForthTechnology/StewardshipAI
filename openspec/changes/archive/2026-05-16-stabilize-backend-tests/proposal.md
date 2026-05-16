## Why

The backend test suite is currently unstable and failing in the CI/CD environment due to environmental conflicts, incorrect async mocking patterns, and stale assertions. This instability undermines the "Traceability Firewall" and prevents reliable deployment. We need to standardize the testing environment and mocking strategy to ensure consistent and reliable verification of the AI Core.

## What Changes

- **Mocking Strategy Standard**: Implement a robust `AsyncIterator` and `AsyncMock` strategy that correctly handles `async for` loops and generator-based responses.
- **Environment Isolation**: Standardize how dummy GCP credentials and configuration are injected during tests to avoid conflicts between local and CI environments.
- **Instruction Alignment**: Synchronize test assertions with the latest agent system instructions to prevent false negatives.
- **Test Runner Reliability**: Refactor `IsolatedAsyncioTestCase` usage to avoid type mismatches and ensure clean setup/teardown of tracer providers and log handlers.

## Capabilities

### New Capabilities
- `test-stability`: Defines requirements for reliable and isolated backend testing, including mocking standards and environmental hygiene.

### Modified Capabilities
- `quality-enforcement`: Update requirements to include "Clean Environment Verification" as part of the Quality Gate.

## Impact

- **Backend Tests**: `test_api.py`, `test_rag_agent.py`, and `test_quality.py` will be significantly refactored.
- **CI/CD Pipeline**: `.github/workflows/deploy.yml` will be simplified to rely on test-level environmental isolation.
- **Audit Tooling**: Minor updates to ensure the audit tool correctly identifies the updated scenario names.
