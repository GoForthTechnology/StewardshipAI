import os
import re
import sys
import argparse
import subprocess

BASELINE_FILE = '.coverage_baseline'

def get_scenarios(check_modified=False):
    scenarios = []
    spec_dir = 'openspec/specs'
    if not os.path.exists(spec_dir):
        return []
    
    modified_files = []
    if check_modified:
        try:
            # Get list of modified files in git (staged and unstaged)
            output = subprocess.check_output(['git', 'status', '--porcelain', spec_dir], text=True)
            for line in output.splitlines():
                # Format: XY path/to/file
                path = line[3:].strip()
                if path.endswith('.md'):
                    modified_files.append(os.path.abspath(path))
        except Exception as e:
            print(f"Warning: Could not get modified files from git: {e}")
            check_modified = False

    for root, dirs, files in os.walk(spec_dir):
        for file in files:
            if file.endswith('.md'):
                path = os.path.join(root, file)
                abs_path = os.path.abspath(path)
                
                if check_modified and abs_path not in modified_files:
                    continue
                    
                capability = os.path.relpath(root, spec_dir)
                with open(path, 'r') as f:
                    for line in f:
                        match = re.search(r'^#### Scenario:\s*(.*)', line)
                        if match:
                            scenarios.append({
                                'capability': capability,
                                'scenario': match.group(1).strip(),
                                'file': path
                            })
    return scenarios

def check_coverage(scenarios):
    test_files = []
    # Collect potential test files
    for root, dirs, files in os.walk('.'):
        if 'node_modules' in root or '.git' in root or 'dist' in root:
            continue
        for file in files:
            if file.endswith('.spec.ts') or (file.startswith('test_') and file.endswith('.py')):
                test_files.append(os.path.join(root, file))
    
    coverage_results = []
    for s in scenarios:
        found = False
        scenario_name = s['scenario']
        # Escape special characters for regex
        pattern = re.escape(scenario_name)
        
        for t_file in test_files:
            with open(t_file, 'r', errors='ignore') as f:
                content = f.read()
                if re.search(pattern, content):
                    found = True
                    break
        
        coverage_results.append({
            **s,
            'covered': found
        })
    
    return coverage_results

def print_report(results):
    print("\n=== OpenSpec Traceability Audit ===\n")
    
    capabilities = {}
    for r in results:
        cap = r['capability']
        if cap not in capabilities:
            capabilities[cap] = {'total': 0, 'covered': 0}
        capabilities[cap]['total'] += 1
        if r['covered']:
            capabilities[cap]['covered'] += 1
            
    total_scenarios = len(results)
    total_covered = sum(1 for r in results if r['covered'])
    coverage_percent = (total_covered/total_scenarios*100) if total_scenarios > 0 else 0
    
    print(f"Overall Coverage: {total_covered}/{total_scenarios} ({coverage_percent:.1f}%)\n")
    
    print(f"{'Capability':<30} | {'Coverage':<10} | {'Status'}")
    print("-" * 55)
    
    for cap, stats in sorted(capabilities.items()):
        percent = (stats['covered'] / stats['total']) * 100
        status = "✅" if percent == 100 else "❌" if percent == 0 else "🟡"
        print(f"{cap:<30} | {stats['covered']:>3}/{stats['total']:<4} | {status} {percent:>5.1f}%")

    missing = [r for r in results if not r['covered']]
    if missing:
        print("\n--- Missing Coverage Details ---")
        current_cap = ""
        for m in missing:
            if m['capability'] != current_cap:
                current_cap = m['capability']
                print(f"\n[{current_cap}]")
            print(f"  - Scenario: {m['scenario']}")
            
    return coverage_percent

def load_baseline():
    if os.path.exists(BASELINE_FILE):
        with open(BASELINE_FILE, 'r') as f:
            try:
                return float(f.read().strip())
            except ValueError:
                return 0.0
    return 0.0

def save_baseline(percent):
    with open(BASELINE_FILE, 'w') as f:
        f.write(f"{percent:.1f}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='OpenSpec Traceability Audit Tool')
    parser.add_argument('--ci', action='store_true', help='Fail if coverage is below baseline')
    parser.add_argument('--check-modified', action='store_true', help='Only check modified spec files')
    parser.add_argument('--update-baseline', action='store_true', help='Update the baseline coverage file')
    
    args = parser.parse_args()

    scenarios = get_scenarios(check_modified=args.check_modified)
    if not scenarios:
        if args.check_modified:
            print("No modified scenarios found.")
            sys.exit(0)
        else:
            print("No scenarios found in openspec/specs/")
            sys.exit(1)
        
    results = check_coverage(scenarios)
    current_coverage = print_report(results)
    
    baseline = load_baseline()
    
    if args.update_baseline:
        save_baseline(current_coverage)
        print(f"\nBaseline updated to {current_coverage:.1f}%")
        sys.exit(0)

    if args.check_modified:
        if current_coverage < 100.0:
            print("\n❌ FAILED: Modified specifications are not fully covered by tests!")
            sys.exit(1)
        else:
            print("\n✅ PASSED: All modified specifications are covered.")
            sys.exit(0)

    if args.ci:
        print(f"\nBaseline Coverage: {baseline:.1f}%")
        print(f"Current Coverage:  {current_coverage:.1f}%")
        
        if current_coverage < baseline:
            print("\n❌ FAILED: Coverage dropped below baseline!")
            sys.exit(1)
        else:
            print("\n✅ PASSED: Coverage is maintained or improved.")
            if current_coverage > baseline:
                print("Suggestion: Run with --update-baseline to set a new high-water mark.")
            sys.exit(0)
