"""
Code Review Mini-Agent - Detailed Demonstration
Shows the full workflow of the code review agent
"""

import sys
sys.path.insert(0, '.')

from app.workflows.code_review import setup_code_review_tools, create_code_review_workflow
from app.core import Graph, WorkflowRunner

print('\n' + '='*70)
print('  CODE REVIEW MINI-AGENT - DETAILED DEMONSTRATION')
print('='*70 + '\n')

# Setup tools
setup_code_review_tools()

# Create workflow
schema = create_code_review_workflow()
graph = Graph(schema)

# Sample code with quality issues
sample_code = '''
def calculate_sum(numbers):
    total = 0
    for num in numbers:
        total = total + num
    return total

def nested_loop_example():
    result = []
    for i in range(10):
        for j in range(10):
            for k in range(10):
                result.append(i * j * k)
    return result

# TODO: Refactor this
def complex_function():
    # FIXME: This is slow
    pass
'''

print('Code to Review:')
print('-' * 70)
print(sample_code)
print('-' * 70 + '\n')

print('Workflow Execution:\n')

runner = WorkflowRunner(graph)
result = runner.run({'code': sample_code})

print('\n' + '='*70)
print('WORKFLOW ANALYSIS RESULTS')
print('='*70 + '\n')

final_state = result['final_state']

print('1. FUNCTION EXTRACTION')
print('   Functions Found:', final_state.get('functions', []))
print('   Total Count:', final_state.get('function_count', 0))

print('\n2. COMPLEXITY ANALYSIS')
print('   Complexity Score:', final_state.get('complexity_score', 0))
print('   Avg Lines per Function:', final_state.get('avg_lines_per_function', 0))
print('   Nested Loops:', final_state.get('nested_loops', 0))

print('\n3. ISSUE DETECTION')
print('   Total Issues:', final_state.get('issue_count', 0))
print('   Issues Found:')
for issue in final_state.get('detected_issues', []):
    print(f'     • {issue}')

print('\n4. QUALITY ASSESSMENT')
quality_score = final_state.get('quality_score', 0)
print('   Quality Score:', quality_score, '/ 100')
print('   Status:', 'APPROVED ✓' if quality_score >= 80 else 'NEEDS IMPROVEMENT ✗')

print('\n5. RECOMMENDATIONS')
print('   Suggestions:')
suggestions = final_state.get('suggestions', [])
if suggestions:
    for suggestion in suggestions:
        print(f'     • {suggestion}')
else:
    print('     • Code quality is good!')

print('\n' + '='*70)
print('EXECUTION SUMMARY')
print('='*70)
print(f'Total Workflow Steps: {len(result["execution_logs"])}')
print(f'Total Execution Time: {sum(log.duration_ms for log in result["execution_logs"]):.2f}ms')

print('\nStep Breakdown:')
for i, log in enumerate(result['execution_logs'], 1):
    if log.status == 'completed':
        print(f'  {i}. {log.node_name:<20} ✓ {log.duration_ms:.2f}ms')

print('\n' + '='*70)
print('WORKFLOW PATTERN DEMONSTRATION')
print('='*70)

print('''
This workflow demonstrates:

1. SEQUENTIAL PIPELINE
   Extract → Complexity → Issues → Suggest
   
   Each node reads the state and adds analysis

2. CONDITIONAL BRANCHING
   After Suggest, check: quality_score >= 80?
   
   YES → Exit workflow (code is good)
   NO  → Loop back to Issues (continue refinement)

3. LOOPING MECHANISM
   Loop until quality_score >= 80 or max iterations
   
   This is how the workflow iteratively improves

RESULT: The code review agent automatically:
  ✓ Analyzes Python code structure
  ✓ Detects code quality issues
  ✓ Calculates quality metrics
  ✓ Provides actionable suggestions
  ✓ Uses conditional routing and looping
''')

print('='*70)
print('✓ Code Review Agent demonstration completed!')
print('='*70 + '\n')
