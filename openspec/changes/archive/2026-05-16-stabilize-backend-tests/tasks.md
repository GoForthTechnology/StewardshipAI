## 1. Test Infrastructure Improvements

- [x] 1.1 Implement a robust `_AsyncIterator` helper in a shared test utility location (or within test files).
- [x] 1.2 Refactor `test_api.py` to move environmental defaults to the absolute top of the file.
- [x] 1.3 Refactor `test_rag_agent.py` to move environmental defaults to the absolute top of the file.

## 2. Mock Refactoring

- [x] 2.1 Fix `AsyncMock` iteration in `test_api.py` using the new `_AsyncIterator`.
- [x] 2.2 Fix `AsyncMock` iteration in `test_rag_agent.py` using the new `_AsyncIterator`.
- [x] 2.3 Ensure `GCPRagAgent` is always initialized within a `google.auth.default` patch context.

## 3. Assertion & Pipeline Synchronization

- [x] 3.1 Update stale instruction assertions in `test_rag_agent.py` to match `rag_agent.py`.
- [x] 3.2 Remove manual `env:` overrides from the `verify` job in `.github/workflows/deploy.yml`.
- [x] 3.3 Verify 100% test pass rate locally and in CI.

## 4. Verification & Audit

- [x] 4.1 Update the `.coverage_baseline` if the stabilization refactor changes the percentage.
- [x] 4.2 Run `python3 verify_coverage.py --ci` to ensure the firewall is green.
