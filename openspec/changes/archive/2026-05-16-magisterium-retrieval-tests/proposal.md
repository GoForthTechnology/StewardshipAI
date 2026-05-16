## Why

The `magisterium-retrieval` capability currently has 0% test coverage and incomplete implementation. While the plumbing for multi-corpus retrieval exists, the system lacks the specific theological-practical synthesis logic and automated verification needed to ensure that doctrinal questions are correctly grounded in the Magisterium corpus and practical advice in the Stewardship corpus.

## What Changes

- Implement theological vs. practical query routing logic to prioritize specific corpora based on query intent.
- Implement weight-based or instruction-based grounding to ensure synthesis prioritizes the correct sources.
- **NEW TESTS**: Add comprehensive test scenarios to verify:
    - Multi-corpus routing (correct corpus IDs sent to retrieval API).
    - Theological grounding (responses grounded in Magisterium documents).
    - Practical grounding (responses grounded in Stewardship documents).

## Capabilities

### New Capabilities
- None

### Modified Capabilities
- `magisterium-retrieval`: Implementing existing unfulfilled requirements for multi-corpus synthesis and hierarchical grounding.

## Impact

- `rag_agent.py`: Logic for query routing and context synthesis.
- `test_rag_agent.py`: New verification scenarios.
- `api.py`: Potential updates to pass more granular corpus intent if needed (likely handled in agent).
