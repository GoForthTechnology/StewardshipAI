## 1. Audit Tooling Upgrades

- [x] 1.1 Modify `verify_coverage.py` to add a `--ci` flag for non-zero exit codes.
- [x] 1.2 Implement baseline tracking in `verify_coverage.py` using a `.coverage_baseline` file.
- [x] 1.3 Add a `--check-modified` flag to `verify_coverage.py` to support targeted local audits.

## 2. CI/CD Pipeline Restructuring

- [x] 2.1 Split `.github/workflows/deploy.yml` into `verify` and `deploy` jobs.
- [x] 2.2 Implement the `verify` job with parallel steps for backend tests, frontend tests, and traceability audit.
- [x] 2.3 Configure the `deploy` job to explicitly depend on the success of the `verify` job.
- [x] 2.4 Add GitHub Action caching for `pip` and `npm` to optimize build times.

## 3. Local Workflow & Guardrails

- [x] 3.1 Initialize a `.coverage_baseline` with the current 81.6% coverage.
- [x] 3.2 Create a local pre-commit script to run `verify_coverage.py` on changed spec files.
- [x] 3.3 Add instructions to `README.md` on how to update the coverage baseline.

## 4. Verification

- [x] 4.1 Trigger a push to `main` and verify the `verify` job runs and blocks `deploy`.
- [x] 4.2 Temporarily lower a test name to verify the audit gate fails the pipeline.
- [x] 4.3 Verify the pre-commit hook prevents committing a new requirement without a matching test.
