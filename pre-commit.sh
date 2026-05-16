#!/bin/bash
# Local pre-commit hook to verify coverage of modified specs

# Get staged spec files
STAGED_SPECS=$(git diff --cached --name-only openspec/specs | grep '\.md$')

if [ -n "$STAGED_SPECS" ]; then
    echo "🔍 Verifying coverage for modified specifications..."
    python3 verify_coverage.py --check-modified
    RESULT=$?
    
    if [ $RESULT -ne 0 ]; then
        echo "❌ PRE-COMMIT FAILED: Modified specs are missing matching tests."
        echo "Please add the required test scenarios before committing."
        exit 1
    fi
    echo "✅ Specification coverage verified."
fi

exit 0
