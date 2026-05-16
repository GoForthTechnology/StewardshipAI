#!/bin/bash

# StewardshipAI - All Tests Runner
# This script orchestrates backend unit tests, OpenSpec coverage audits, 
# RAG integration verification, and frontend unit tests.

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================================================${NC}"
echo -e "${BLUE}           StewardshipAI Comprehensive Test Suite               ${NC}"
echo -e "${BLUE}================================================================${NC}"

# 1. Backend Unit Tests
echo -e "\n${YELLOW}[1/4] Running Backend Unit Tests (pytest)...${NC}"
if ! python3 -m pytest --version &> /dev/null; then
    echo -e "${RED}Error: pytest not found. Please install requirements.txt${NC}"
    BACKEND_EXIT=1
else
    # Run pytest on all test_*.py files
    python3 -m pytest
    BACKEND_EXIT=$?
fi

# 2. OpenSpec Traceability Audit
echo -e "\n${YELLOW}[2/4] Running OpenSpec Coverage Audit...${NC}"
python3 verify_coverage.py
COVERAGE_EXIT=$?

# 3. RAG Integration Verification
echo -e "\n${YELLOW}[3/4] Running RAG & Filter Verification...${NC}"
echo -e "${BLUE}(Note: These require active GCP credentials and a valid RAG corpus)${NC}"
python3 verify_rag.py
RAG_EXIT=$?
python3 verify_filters.py
FILTERS_EXIT=$?

# 4. Frontend Unit Tests
echo -e "\n${YELLOW}[4/4] Running Frontend Unit Tests...${NC}"
if [ -d "frontend" ]; then
    cd frontend
    if [ ! -d "node_modules" ]; then
        echo -e "${YELLOW}node_modules not found in frontend/. Attempting npm install...${NC}"
        npm install --silent
    fi
    
    # For Angular + Vitest, 'npm test' is the standard entry point.
    npm test -- --run
    FRONTEND_EXIT=$?
    cd ..
else
    echo -e "${RED}Error: frontend directory not found.${NC}"
    FRONTEND_EXIT=1
fi

# Final Summary
echo -e "\n${BLUE}================================================================${NC}"
echo -e "${BLUE}                       Test Summary                             ${NC}"
echo -e "${BLUE}================================================================${NC}"

report_status() {
    if [ $1 -eq 0 ]; then
        echo -e "$2: ${GREEN}PASSED${NC}"
    else
        echo -e "$2: ${RED}FAILED${NC}"
    fi
}

report_status $BACKEND_EXIT "Backend Unit Tests"
report_status $COVERAGE_EXIT "OpenSpec Coverage Audit"
report_status $RAG_EXIT "RAG Verification"
report_status $FILTERS_EXIT "Filter Verification"
report_status $FRONTEND_EXIT "Frontend Unit Tests"

echo -e "${BLUE}================================================================${NC}"

# Combined Exit Code
if [ $BACKEND_EXIT -eq 0 ] && [ $COVERAGE_EXIT -eq 0 ] && [ $RAG_EXIT -eq 0 ] && [ $FILTERS_EXIT -eq 0 ] && [ $FRONTEND_EXIT -eq 0 ]; then
    echo -e "${GREEN}Overall Result: ALL TESTS PASSED${NC}"
    exit 0
else
    echo -e "${RED}Overall Result: SOME TESTS FAILED${NC}"
    exit 1
fi
