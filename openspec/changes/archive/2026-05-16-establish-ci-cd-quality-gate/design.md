## Context

The Stewardship AI Portal currently has a deployment-focused CI/CD pipeline. Recent "Test-First" efforts have achieved 81.6% scenario coverage, but there is no mechanism to prevent this number from dropping during rapid development on the `main` branch. We need to formalize a gate that ensures every scenario in `openspec/specs` is reflected in the codebase before a deployment occurs.

## Goals / Non-Goals

**Goals:**
- Upgrade `verify_coverage.py` to support exit codes for CI integration.
- Restructure GitHub Actions to include a `verify` job that blocks the `deploy` job.
- Implement a baseline tracking mechanism to prevent coverage regression.
- Add backend and frontend unit tests to the CI pipeline.

**Non-Goals:**
- Implementing a full PR-based workflow (we will maintain the single-branch `main` push strategy).
- Adding integration tests that require live GCP resources (keep tests mocked for speed).
- Automating Terraform `apply` (out of scope for this specific quality gate).

## Decisions

### Decision 1: `verify_coverage.py` CI Mode
- **Rationale**: The script will be updated to accept a `--ci` flag. In this mode, it will not only print the report but also calculate the coverage delta. If `current_coverage < baseline_coverage`, it will exit with `1`.
- **Alternatives**: Using a third-party coverage tool (Rejected because they don't understand OpenSpec scenarios).

### Decision 2: Baseline Storage
- **Rationale**: Store a `.coverage_baseline` file in the repository root. This file will be updated only when coverage *increases*.
- **Alternatives**: Querying the previous Git commit for the report (Rejected for complexity/reliability in CI).

### Decision 3: Parallelized Verify Job
- **Rationale**: The `verify` job will run backend (`pytest`) and frontend (`npm test`) in parallel to minimize pipeline latency. The `deploy` job will wait for both (and the audit) to pass.

### Decision 4: Local Git Hooks
- **Rationale**: Use `husky` (or a simple shell script in `.git/hooks`) to run `python3 verify_coverage.py --check-modified` during pre-commit. This ensures that if you change a spec file, you must have the test ready before you can even commit.

## Risks / Trade-offs

- **[Risk] Pipeline Latency** → **Mitigation**: Use aggressive caching for `node_modules` and Python dependencies in GitHub Actions.
- **[Risk] Flaky Frontend Tests** → **Mitigation**: Ensure Vitest environment is stable and use `ci` flag for non-interactive execution.
- **[Risk] Forgot to Update Baseline** → **Mitigation**: The `verify_coverage.py` tool will automatically suggest updating the baseline if coverage increases.
