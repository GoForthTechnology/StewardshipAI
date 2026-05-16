## Context

The recent implementation of the "Traceability Firewall" revealed underlying instabilities in the backend test suite. Environmental variables were bleeding across test boundaries, and the mocking of asynchronous generators was causing `TypeError` in the CI environment. Additionally, strict assertions on system instructions became brittle as the instructions evolved.

## Goals / Non-Goals

**Goals:**
- Fix `TypeError: 'async_generator' object is not iterable` in all backend tests.
- Decouple CI pipeline from local environment variables.
- Update test assertions to match the actual agent instructions.
- Ensure 100% pass rate for backend tests in GitHub Actions.

**Non-Goals:**
- Adding new feature functionality.
- Changing the underlying RAG logic.

## Decisions

### Decision 1: Custom `AsyncIterator` Wrapper
- **Rationale**: Instead of relying on `AsyncMock`'s default `__aiter__` (which is often misconfigured in different Python versions), we will use a dedicated `_AsyncIterator` class in our test utilities.
- **Implementation**:
  ```python
  class _AsyncIterator:
      def __init__(self, items):
          self.items = iter(items)
      def __aiter__(self):
          return self
      async def __anext__(self):
          try:
              return next(self.items)
          except StopIteration:
              raise StopAsyncIteration
  ```

### Decision 2: Early Environment Patching
- **Rationale**: We will move `os.environ` defaults to the very top of each test file, *before* importing any application modules. This ensures that `get_config()` always has valid (if dummy) data to validate against.

### Decision 3: "Contains" over "Equals" for Instructions
- **Rationale**: Brittle instructions (full string comparison) cause unnecessary failures. We will transition to `assertIn` for key phrases that define the contract (e.g., "FORBID... greetings") rather than asserting the entire instruction block.

## Risks / Trade-offs

- **[Risk] Hidden Initialization Bugs** → **Mitigation**: By providing dummy env vars, we might miss a bug where a real variable is missing. We will mitigate this by ensuring the "Verify" stage in CI remains as clean as possible.
- **[Risk] Mock Drift** → **Mitigation**: We will continue to use the OpenSpec audit to ensure our mocks still accurately represent the scenarios we are testing.
