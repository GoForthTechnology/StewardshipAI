import os
import re
import sys

def get_scenarios():
    scenarios = []
    spec_dir = 'openspec/specs'
    if not os.path.exists(spec_dir):
        return []
    
    for root, dirs, files in os.walk(spec_dir):
        for file in files:
            if file.endswith('.md'):
                path = os.path.join(root, file)
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
    
    print(f"Overall Coverage: {total_covered}/{total_scenarios} ({ (total_covered/total_scenarios*100) if total_scenarios > 0 else 0:.1f}%)\n")
    
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

if __name__ == "__main__":
    scenarios = get_scenarios()
    if not scenarios:
        print("No scenarios found in openspec/specs/")
        sys.exit(0)
        
    results = check_coverage(scenarios)
    print_report(results)
